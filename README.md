# FELIX MDL Repair and PySD Validation

This directory contains a reproducible workflow for repairing a damaged FELIX
Vensim model, translating the repaired model to Python with PySD, and comparing
selected simulation outputs with historical observations.

The repair is deliberately conservative: the source model is never overwritten,
missing content is copied only from the supplied reference model, and every
model-specific replacement has an expected match count.

## Repository layout

```text
.
├── felix_mdl_tool.py
├── FeliX3_ISE_v26_original_need_repaired.mdl
├── felix_validate_lx_manual_with_labor_force_patch.ipynb
├── requirements.txt
├── input/
│   ├── FeliX3_ISE_v26_reference_before_repaired.mdl
│   └── FeliX_HistoricalData.xlsx
└── output/
    ├── FeliX3_ISE_v26_final_fixed.mdl
    └── FeliX3_ISE_v26_final_fixed.py
```


| Path                                        | Role                                                         | Maintained manually? |
| ------------------------------------------- | ------------------------------------------------------------ | -------------------- |
| `felix_mdl_tool.py`                         | Repair, validation, and PySD translation pipeline            | Yes                  |
| `FeliX3_ISE_v26_original_need_repaired.mdl` | Damaged model used as the repair source                      | No                   |
| `input/*reference*.mdl`                     | Complete model used to restore missing content               | No                   |
| `input/*.xlsx`                              | Historical observations used by the notebooks                | No                   |
| `output/*.mdl`                              | Repaired Vensim model                                        | Generated            |
| `output/*.py`                               | PySD translation plus one generated-code compatibility patch | Generated            |
| `felix_validate_*.ipynb`                    | Interactive smoke tests and historical validation            | Yes                  |




## Repair logic

The build follows one deterministic pipeline:

1. Split the source and reference files at the Vensim sketch marker. Repairs
  operate only on equations; the source sketch is retained.
2. Restore subscript ranges that are absent from the source but present in the
  reference model.
3. Restore equations or indexed equation slices that have no left-hand-side
  definition in the source.
4. Rebuild the inverse-standard-normal lookup x-axis by applying the standard
  normal cumulative distribution function to the existing z-values. This makes
   the lookup coordinates strictly increasing without changing its z-values.
5. Expand nine known indexed aliases that PySD would otherwise merge into
  self-referential Python functions.
6. Check required equations and lookup monotonicity before writing the output.
7. Translate the repaired MDL with PySD, then patch the generated initialization
  of the dimensioned climate-event `SMOOTH` state by broadcasting its scalar
   initial value to the declared coordinate length.

For the files currently included here, a successful repair reports:

```text
Repair summary: 51 subscript ranges, 116 equations, 298 lookup points, 9 slice aliases
```

These counts are guardrails. A different model revision may require reviewed
changes to the repair rules rather than silently accepting different matches.

## Setup

Python 3.10 or newer is recommended. From this directory:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

The workflow was verified with PySD 3.9.0. Vensim Professional or DSS is needed
to edit or simulate this subscripted model in Vensim; PLE and PLE Plus do not
support the required subscript features.

## Build the repaired model

Run the complete repair and translation workflow:

```powershell
python felix_mdl_tool.py
```

To repair the MDL without invoking PySD:

```powershell
python felix_mdl_tool.py --mdl-only
```

Custom paths are supported:

```powershell
python felix_mdl_tool.py `
  --src "D:\models\felix_damaged.mdl" `
  --reference "D:\models\felix_reference.mdl" `
  --out "D:\models\felix_repaired.mdl"
```

Run `python felix_mdl_tool.py --help` for the complete command-line interface.

## Smoke-test the generated model

Use a small output set first. Explicit return columns reduce memory use and
avoid evaluating unrelated parts of this large model.

```python
from pathlib import Path

import pysd

model_path = Path("output") / "FeliX3_ISE_v26_final_fixed.py"
model = pysd.load(model_path)

result = model.run(
    final_time=1910,
    return_columns=[
        "Population",
        "Gross World Product",
        "C in Atmosphere",
    ],
)
print(result.tail())
```



## Validation notebooks

Run the notebooks from this directory so that their relative `input/` and
`output/` paths resolve correctly.

- `felix_validate_lx_manual.ipynb` loads the generated model, inspects
subscript structures, runs selected outputs, and plots historical comparisons.
- `felix_validate_lx_manual_with_labor_force_patch.ipynb` performs the same
analysis but overrides `Total Labor Force` at runtime. It weights the
skill/unskill population tensor by the age- and gender-specific labor-force
participation fraction before summing. This notebook exists to make the
disputed labor-force interpretation explicit; it does not modify the MDL.

Notebook outputs are intentionally cleared so that results are not confused with
a run made from a different model or PySD version. Run the cells in order to
reproduce the analysis.

The historical validation uses 15 indicators from
`input/FeliX_HistoricalData.xlsx` and follows the comparison context of Figure 8
in Ye et al. (2024), *FeliX 2.0: An integrated model of climate, economy,
environment, and society interactions*.

## Python API

The same build can be called from Python:

```python
from pathlib import Path

from felix_mdl_tool import build

report, generated_python = build(
    source=Path("FeliX3_ISE_v26_original_need_repaired.mdl"),
    reference=Path("input/FeliX3_ISE_v26_reference_before_repaired.mdl"),
    output=Path("output/FeliX3_ISE_v26_final_fixed.mdl"),
    translate=True,
)
print(report)
print(generated_python)
```



## Known limitations

- The repair rules are specific to the supplied FELIX model revision.
- The reference model is required because the missing ranges and equations
cannot be reconstructed reliably from the damaged file alone.
- The tool preserves the source sketch and does not repair diagram layout.
- YoGL life-table equations use `PreviousCohort`/`NextCohort` recursion that has
not been rewritten. Avoid requesting YoGL-related outputs until that subsystem
has a dedicated compatibility repair.
- PySD may emit warnings about incomplete subscript sets or mixed component
types. The CLI reports their count; review new warning categories when changing
model or PySD versions.
- `output/FeliX3_ISE_v26_final_fixed.py` is generated code. Do not edit it by
hand; update `felix_mdl_tool.py` and rebuild instead.

