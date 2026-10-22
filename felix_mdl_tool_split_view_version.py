"""Repair the FELIX Vensim model and translate it into a PySD model.

The default workflow reads the damaged source model, applies deterministic
repairs, validates the result, and invokes PySD. The source file is never
overwritten. Run ``python felix_mdl_tool.py --help`` for CLI options.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import warnings
from dataclasses import dataclass, field
from pathlib import Path


# ---------------------------------------------------------------------------
# 1. Default file locations
#
# Inputs:
#   - DEFAULT_SOURCE: damaged MDL copied into this project directory.
#   - DEFAULT_REFERENCE: complete MDL used only to restore missing subscript
#     ranges and equation blocks; it does not replace the source wholesale.
# Output:
#   - DEFAULT_OUTPUT: repaired MDL; it must not overwrite the source.
# ---------------------------------------------------------------------------

HERE = Path(__file__).resolve().parent
DEFAULT_SOURCE = HERE / "FeliX3_ISE_v26_original_need_repaired.mdl"
DEFAULT_REFERENCE = HERE / "input" / "FeliX3_ISE_v26_reference_before_repaired.mdl"
DEFAULT_OUTPUT = HERE / "output" / "native_split_views" / "FeliX3_ISE_v26_final_fixed.mdl"


# ---------------------------------------------------------------------------
# 2. MDL parsing
#
# Equation repairs retain the source sketch. The translation-only output
# additionally normalizes unsupported arrow geometry, with a change log.
# ---------------------------------------------------------------------------

SKETCH_MARKER = "Sketch information - do not modify anything except names"
RANGE_HEAD = re.compile(
    r'^(?P<head>"[^"]+"|[A-Za-z][A-Za-z0-9 _]*)\s*:\s*$', re.MULTILINE
)
LHS = re.compile(
    r'^(?P<name>"[^"]+"|[A-Za-z][^\[=\n]*?)\s*'
    r'(?:\[(?P<sub>[^\]]*)\])?\s*=',
    re.MULTILINE,
)
NUMBER = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?"
LOOKUP_PAIR = re.compile(
    rf"\(\s*({NUMBER})\s*(?:\\\s*)?,\s*(?:\\\s*)?({NUMBER})\s*\)"
)


def read_text(path: Path) -> str:
    """Read an MDL as UTF-8 while tolerating isolated invalid bytes."""
    return path.read_text(encoding="utf-8", errors="replace")


def split_equations_and_sketch(text: str) -> tuple[str, str]:
    """Return the equation and sketch sections as separate strings."""
    pos = text.find(SKETCH_MARKER)
    if pos < 0:
        return text, ""
    line_start = text.rfind("\n", 0, pos) + 1
    return text[:line_start], text[line_start:]


def next_block_start(text: str, start: int) -> int:
    """Find the start of the next equation or subscript-range block."""
    positions = []
    for pattern in (LHS, RANGE_HEAD):
        match = pattern.search(text, start + 1)
        if match:
            positions.append(match.start())
    return min(positions) if positions else len(text)


def range_blocks(equations: str) -> list[tuple[str, str]]:
    """Extract ``Range: ... |`` blocks."""
    blocks = []
    for match in RANGE_HEAD.finditer(equations):
        end = equations.find("|", match.end())
        if end < 0:
            continue
        end += 1
        if end < len(equations) and equations[end] == "\n":
            end += 1
        blocks.append((match.group("head").strip(), equations[match.start() : end]))
    return blocks


def equation_blocks(equations: str) -> list[tuple[str, str | None, str]]:
    """Extract ``(variable name, subscript slice, equation block)`` tuples."""
    blocks = []
    for match in LHS.finditer(equations):
        subscript = match.group("sub")
        if subscript is not None:
            subscript = subscript.strip()
        blocks.append(
            (
                match.group("name").strip(),
                subscript,
                equations[match.start() : next_block_start(equations, match.start())],
            )
        )
    return blocks


def equation_key(name: str, subscript: str | None) -> str:
    return f"{name}[{subscript}]" if subscript else name


# ---------------------------------------------------------------------------
# 3. Repair rules
# ---------------------------------------------------------------------------


@dataclass
class RepairReport:
    """Record changes made by each repair rule."""

    ranges_restored: list[str] = field(default_factory=list)
    equations_restored: list[str] = field(default_factory=list)
    lookup_points: int = 0
    aliases_expanded: dict[str, int] = field(default_factory=dict)


def restore_reference_content(
    equations: str, reference: str, report: RepairReport
) -> str:
    """Restore missing ranges and equations from the complete reference MDL."""
    existing_ranges = {name for name, _ in range_blocks(equations)}
    missing_ranges = [
        (name, block)
        for name, block in range_blocks(reference)
        if name not in existing_ranges
    ]
    report.ranges_restored = [name for name, _ in missing_ranges]

    if missing_ranges:
        inserted = "\n".join(block.rstrip() for _, block in missing_ranges) + "\n\n"
        if equations.startswith("{UTF-8}"):
            first_line, rest = equations.split("\n", 1)
            equations = first_line + "\n\n" + inserted + rest
        else:
            equations = inserted + equations

    existing_equations = {
        equation_key(name, sub) for name, sub, _ in equation_blocks(equations)
    }
    missing_equations = []
    for name, sub, block in equation_blocks(reference):
        key = equation_key(name, sub)
        if key not in existing_equations:
            missing_equations.append((key, block))

    report.equations_restored = [key for key, _ in missing_equations]
    if missing_equations:
        appendix = "\n\n".join(block.rstrip() for _, block in missing_equations)
        equations = equations.rstrip() + "\n\n" + appendix + "\n"
    return equations


def repair_inverse_normal_lookup(
    equations: str, _reference: str, report: RepairReport
) -> str:
    """Recompute probabilities from z-scores to make the lookup monotonic."""
    marker = "Inverse table for standard normal distribution("
    if marker not in equations:
        raise RuntimeError(
            "Inverse-normal lookup not found; the source model may be a "
            "different version."
        )

    start = equations.index(marker)
    end = equations.index("\n\t~\tDmnl", start)
    block = equations[start:end]
    # Skip the Vensim lookup-coordinate declaration.
    data_start = block.index("],") + 2

    def replace_pair(match: re.Match[str]) -> str:
        z_text = match.group(2)
        z = float(z_text)
        probability = 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))
        return f"({probability:.15g},{z_text})"

    repaired_points, count = LOOKUP_PAIR.subn(replace_pair, block[data_start:])
    if count < 250:
        raise RuntimeError(
            "Unexpected inverse-normal lookup size: "
            f"expected at least 250 points, found {count}."
        )

    report.lookup_points = count
    repaired_block = block[:data_start] + repaired_points
    return equations[:start] + repaired_block + equations[end:]


# PySD merges multiple Vensim slices of one variable into a single function.
# Expanding these aliases prevents the generated function from calling itself.
ALIAS_RULES = (
    (
        "labor",
        r'(Labor Force Participation Fraction Variation\[female,\s*"(?:60-64|30-34|35-39|40-44|45-49|50-54)"\]\s*=\s*)'
        r'Labor Force Participation Fraction Variation\[female,\s*"(?:55-59|25-29)"\]',
        r"\g<1>0",
        6,
    ),
    (
        "birth_gender",
        r"(Birth Gender Fraction\[female\]\s*=\s*)1\s*-\s*Birth Gender Fraction\[male\]",
        r"\g<1>1-(Birth Gender Fraction Init + SMOOTH3(STEP(Birth Gender Fraction Variation-Birth Gender Fraction Init,Current year),SSP Demographic Variation Time))",
        1,
    ),
    (
        "eggs",
        r"(Production rate of animal food\[Eggs\]\s*=\s*)Production rate of animal food\[CropMeat\]\s*\*\s*Meat to Eggs Multiplier",
        r"\g<1>MIN(Desired food production in tonnes[CropMeat],sum(Feed Availability[PlantFood!]/Unit feed used for meat production))*Meat to Eggs Multiplier",
        1,
    ),
    (
        "fertilizer",
        r"(N fertilizer shares2\[VegFruits\]\s*=\s*)1\s*-\s*\(N fertilizer shares2\[Grains\]\s*\+\s*N fertilizer shares2\[Pulses\]\s*\+\s*N fertilizer shares2\[\s*\\?\s*OtherCrops\]\s*\+\s*N fertilizer shares2\[PasMeat\]\)",
        r"\g<1>1-(N fertilizer shares Data[Grains]*(1+STEP(SA N fertilizer shares[Grains]-1,2020))+N fertilizer shares Data[Pulses]+N fertilizer shares Data[OtherCrops]*(1+STEP(SA N fertilizer shares[OtherCrops]-1,2020))+0.047)",
        1,
    ),
)


def expand_slice_aliases(
    equations: str, _reference: str, report: RepairReport
) -> str:
    """Expand known slice aliases and verify every expected match count."""
    for name, pattern, replacement, expected in ALIAS_RULES:
        equations, count = re.subn(
            pattern, replacement, equations, flags=re.IGNORECASE
        )
        report.aliases_expanded[name] = count
        if count != expected:
            raise RuntimeError(
                f"Slice rule {name!r} matched {count} times; expected "
                f"{expected}. Check whether the model text has changed."
            )
    return equations


# Repair rules run in this order and share the same function signature.
PATCH_PIPELINE = (
    restore_reference_content,
    repair_inverse_normal_lookup,
    expand_slice_aliases,
)


# ---------------------------------------------------------------------------
# 4. Build and validation
# ---------------------------------------------------------------------------


def validate_repaired_model(text: str) -> None:
    """Run lightweight checks before writing the repaired model."""
    equations, _ = split_equations_and_sketch(text)
    keys = {equation_key(name, sub) for name, sub, _ in equation_blocks(equations)}
    required = {
        "Population",
        "Population by Gender[Gender]",
        "Birth Rate[Gender]",
        "Production rate of animal food[CropMeat]",
        "Reference Food Waste and Loss[FoodCategories]",
        "Annual Total Crop Demand for APs[PlantFood]",
    }
    missing = sorted(required - keys)
    if missing:
        raise RuntimeError(
            "Required equations are still missing after repair: "
            + ", ".join(missing)
        )

    # Parse the repaired lookup again and confirm strict x-axis monotonicity.
    marker = "Inverse table for standard normal distribution("
    start = equations.index(marker)
    end = equations.index("\n\t~\tDmnl", start)
    block = equations[start:end]
    lookup_data = block[block.index("],") + 2 :]
    pairs = [(float(x), float(y)) for x, y in LOOKUP_PAIR.findall(lookup_data)]
    if len(pairs) < 250 or any(b[0] <= a[0] for a, b in zip(pairs, pairs[1:])):
        raise RuntimeError(
            "The repaired inverse-normal lookup x-axis is not strictly increasing."
        )


def repair_model(source_text: str, reference_text: str) -> tuple[str, RepairReport]:
    """Repair in-memory MDL text for use in notebooks and tests."""
    equations, sketch = split_equations_and_sketch(source_text)
    reference_equations, _ = split_equations_and_sketch(reference_text)

    report = RepairReport()
    for patch in PATCH_PIPELINE:
        equations = patch(equations, reference_equations, report)
    repaired = equations + sketch
    validate_repaired_model(repaired)
    return repaired, report


def patch_smooth_scalar_init(py_path: Path) -> int:
    """Patch PySD's scalar initialization for a dimensioned ``SMOOTH``.

    PySD generates an ``xarray.DataArray`` with scalar data and one declared
    dimension for this model's climate-event memory. Explicit broadcasting is
    retained for compatibility; xarray 2026.7.0 already handles this case.
    """
    text = py_path.read_text(encoding="utf-8")

    # Match both single-line and multiline generated forms:
    #   lambda: xr.DataArray(
    #       climate_events_in_memory(),
    #       {"Education": _subscript_dict["Education"]},
    #       ["Education"],
    #   ),
    pattern = re.compile(
        r"lambda:\s*xr\.DataArray\(\s*"
        r"(climate_events_in_memory)\(\)\s*,\s*"
        r"\{([^}]+)\}\s*,\s*"
        r"\[([^\]]+)\]\s*,?\s*\)",
        re.MULTILINE,
    )

    def replacer(m: re.Match) -> str:
        dim_key = re.search(
            r'_subscript_dict\[["\']?([A-Za-z_][A-Za-z0-9_]*)["\']?\]',
            m.group(2),
        )
        if not dim_key:
            return m.group(0)
        dim_name = dim_key.group(1)
        return (
            f"lambda: xr.DataArray(\n"
            f"        np.broadcast_to(\n"
            f"            {m.group(1)}(),\n"
            f"            (len(_subscript_dict[\"{dim_name}\"]),),\n"
            f"        ),\n"
            f"        {{{m.group(2)}}},\n"
            f"        [{m.group(3)}],\n"
            f"    )"
        )

    original_text = text
    text, count = pattern.subn(replacer, text)
    if count:
        py_path.with_suffix('.py.before_smooth.txt').write_text(original_text, encoding='utf-8')
        py_path.write_text(text, encoding="utf-8")
        print(f"Patched {count} dimensioned SMOOTH scalar initialization(s).")
    return count


def normalize_sketch_arrows(text: str) -> tuple[str, list[dict]]:
    """Keep equations/view membership; normalize multi-point arrows for PySD.

    PySD 3.14.3 sketch.peg accepts one point per arrow. These coordinates
    affect geometry only, not the variable definitions used to assign views.
    This produces a translation copy, not a Vensim layout round-trip.
    """
    equations, sketch = split_equations_and_sketch(text)
    lines = sketch.splitlines(keepends=True)
    changes = []
    for index, line in enumerate(lines):
        if line.lstrip().startswith('1,'):
            normalized = re.sub(
                r'(\|\(-?\d+,-?\d+\)\|)(?:\(-?\d+,-?\d+\)\|)+',
                r'\1', line)
            if normalized != line:
                changes.append({'sketch_line': index + 1,
                                'before': line.rstrip(), 'after': normalized.rstrip()})
                lines[index] = normalized
    result = equations + ''.join(lines)
    if split_equations_and_sketch(result)[0] != equations:
        raise RuntimeError('Sketch normalization unexpectedly changed equations.')
    return result, changes


def translate_with_pysd(mdl_path: Path) -> Path:
    """Translate an MDL with PySD and return the generated Python path."""
    try:
        import pysd
    except ImportError as exc:
        raise RuntimeError(
            "PySD is not installed in the current environment. Use --mdl-only "
            "to generate only the repaired MDL."
        ) from exc

    # Count repetitive structural warnings without flooding the terminal.
    # Translate first, patch generated modules next, initialize only afterwards.
    # Persist warnings even if translation fails.
    caught = []
    try:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            model = pysd.read_vensim(mdl_path, split_views=True, initialize=False)
    finally:
        mdl_path.with_suffix('.warnings.json').write_text(json.dumps([
            {'category': w.category.__name__, 'message': str(w.message)}
            for w in caught], ensure_ascii=False, indent=2), encoding='utf-8')
    if caught:
        print(
            f"PySD emitted {len(caught)} structural warning(s); "
            f"saved in {mdl_path.with_suffix('.warnings.json').name}."
        )
    py_path = Path(model.py_model_file).resolve()
    if not py_path.is_file():
        raise RuntimeError(f"PySD did not generate the expected file: {py_path}")
    return py_path

def build(
    source: Path, reference: Path, output: Path, translate: bool,
    already_repaired: bool = False
) -> tuple[RepairReport, Path | None]:
    """Build a repaired MDL and optionally translate it to Python."""
    source = source.resolve()
    reference = reference.resolve()
    output = output.resolve()

    if not source.is_file():
        raise FileNotFoundError(f"Source MDL does not exist: {source}")
    if not already_repaired and not reference.is_file():
        raise FileNotFoundError(f"Reference MDL does not exist: {reference}")
    if output == source:
        raise ValueError("Refusing to overwrite the source MDL; choose another --out.")

    if already_repaired:
        repaired, report = read_text(source), RepairReport()
        validate_repaired_model(repaired)
    else:
        repaired, report = repair_model(read_text(source), read_text(reference))
    before_sketch = repaired
    repaired, sketch_changes = normalize_sketch_arrows(repaired)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.with_suffix('.sketch_changes.json').write_text(
        json.dumps(sketch_changes, ensure_ascii=False, indent=2), encoding='utf-8')
    output.write_text(repaired, encoding="utf-8")
    py_path = translate_with_pysd(output) if translate else None
    patches = {}
    if py_path:
        module_dir = py_path.parent / ('modules_' + py_path.stem)
        if not module_dir.is_dir():
            raise RuntimeError('Expected native view modules were not generated.')
        for generated in [py_path] + sorted(module_dir.rglob('*.py')):
            count = patch_smooth_scalar_init(generated)
            if count:
                patches[str(generated.relative_to(output.parent))] = count
        import pysd
        with warnings.catch_warnings(record=True) as load_warnings:
            warnings.simplefilter('always')
            pysd.load(py_path)  # Confirm the patched files initialize correctly.
    info = {
        'source': str(source), 'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'output': str(output), 'already_repaired': already_repaired,
        'equations_preserved_by_sketch_normalization':
            split_equations_and_sketch(before_sketch)[0] == split_equations_and_sketch(repaired)[0],
        'sketch_arrow_changes': len(sketch_changes), 'smooth_patches': patches,
        'split_views': True, 'initialize_during_translation': False,
        'initialization_passed': py_path is not None,
        'view_module_count': len(list(module_dir.rglob('*.py'))) if py_path else 0,
        'pysd_version': pysd.__version__ if py_path else None,
        'initialization_warnings': [str(w.message) for w in load_warnings] if py_path else [],
    }
    output.with_suffix('.build_info.json').write_text(
        json.dumps(info, ensure_ascii=False, indent=2), encoding='utf-8')
    return report, py_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Repair the FELIX MDL and translate it with PySD by default."
    )
    parser.add_argument("--src", type=Path, default=DEFAULT_SOURCE, help="Source MDL")
    parser.add_argument('--already-repaired', action='store_true',
                        help='Copy/validate a repaired source, without reapplying repair rules')
    parser.add_argument(
        "--reference",
        type=Path,
        default=DEFAULT_REFERENCE,
        help="Complete reference MDL used to restore missing model content",
    )
    parser.add_argument(
        "--out", type=Path, default=DEFAULT_OUTPUT, help="Repaired MDL output path"
    )
    parser.add_argument(
        "--mdl-only",
        action="store_true",
        help="Generate the repaired MDL without invoking PySD",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        report, py_path = build(
            args.src, args.reference, args.out, translate=not args.mdl_only,
            already_repaired=args.already_repaired
        )
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        raise SystemExit(f"Error: {exc}") from exc

    print(f"Repaired MDL: {args.out.resolve()}")
    if py_path:
        print(f"PySD model: {py_path}")
    print(
        "Repair summary: "
        f"{len(report.ranges_restored)} subscript ranges, "
        f"{len(report.equations_restored)} equations, "
        f"{report.lookup_points} lookup points, "
        f"{sum(report.aliases_expanded.values())} slice aliases"
    )


if __name__ == "__main__":
    main()
