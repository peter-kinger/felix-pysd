"""Check sketch failure, SMOOTH compatibility and split-output equivalence."""
from pathlib import Path
import hashlib
import json
import shutil
import tempfile
import time
import warnings

import numpy as np
import pysd
from pysd.translators.vensim.vensim_file import VensimFile

HERE = Path(__file__).resolve().parent
ENTRY = HERE/'FeliX3_ISE_v26_final_fixed.py'
ORIGINAL = HERE.parent/ENTRY.name
CORE = ['Population','Gross World Product','Total Labor Force',
        'Temperature Change from Preindustrial','Atmospheric Concentration CO2',
        'Total C Emissions','Forest Land','population_cohorts']


def main():
    result = {'pysd':pysd.__version__,'checks':{}}
    hashes = {str(p):hashlib.sha256(p.read_bytes()).hexdigest()
              for p in [ORIGINAL, ORIGINAL.with_suffix('.mdl')]}
    try:
        VensimFile(ORIGINAL.with_suffix('.mdl')).parse_sketch([])
        result['checks']['original_sketch'] = {'returned':True}
    except Exception as exc:
        result['checks']['original_sketch'] = {'error':type(exc).__name__,'message':str(exc)}

    modules = HERE/('modules_'+ENTRY.stem)
    # Create a confined temporary copy to demonstrate what happens if the
    # generated module is initialized before scalar SMOOTH repair.
    with tempfile.TemporaryDirectory(prefix='_smooth_check_',dir=HERE) as folder:
        temp = Path(folder).resolve()
        temp.relative_to(HERE.resolve())  # Verify cleanup stays inside this output folder.
        shutil.copy2(ENTRY,temp/ENTRY.name)
        shutil.copy2(HERE/('_subscripts_'+ENTRY.stem+'.json'),temp/('_subscripts_'+ENTRY.stem+'.json'))
        shutil.copytree(modules,temp/modules.name,ignore=shutil.ignore_patterns('__pycache__','*.before_smooth.txt'))
        backups = list(modules.rglob('*.py.before_smooth.txt'))
        for backup in backups:
            relative = str(backup.relative_to(HERE)).removesuffix('.before_smooth.txt')
            shutil.copy2(backup,temp/relative)
        assert backups, 'No raw SMOOTH module captured during build'
        try:
            with warnings.catch_warnings(record=True):
                warnings.simplefilter('always')
                pysd.load(temp/ENTRY.name)
            result['checks']['unpatched_smooth_initialization'] = {'returned':True}
        except Exception as exc:
            result['checks']['unpatched_smooth_initialization'] = {'error':type(exc).__name__,'message':str(exc)}

    frames = {}
    for label,path in [('original',ORIGINAL),('native_split',ENTRY)]:
        start = time.perf_counter()
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always')
            model = pysd.load(path)
            out = model.run(return_columns=CORE,final_time=1902,time_step=.125,
                            return_timestamps=[1900,1901,1902],cache_output=False,
                            initial_condition='original',progress=False)
        frames[label] = out
        out.to_csv(HERE/(label+'_1900_1902.csv'))
        result['checks'][label] = {'seconds':time.perf_counter()-start,
            'all_finite':bool(np.isfinite(out.to_numpy(float)).all()),
            'rows':len(out),'columns':len(out.columns),
            'warnings':sorted(set(str(w.message) for w in caught))}
    a,b = frames.values()
    assert a.columns.equals(b.columns) and a.index.equals(b.index)
    assert np.isfinite(a.to_numpy(float)).all() and np.isfinite(b.to_numpy(float)).all()
    np.testing.assert_allclose(a.to_numpy(float),b.to_numpy(float),rtol=1e-12,atol=1e-8)
    result['equivalence_passed'] = True
    result['max_absolute_error'] = float(np.max(np.abs(a.to_numpy(float)-b.to_numpy(float))))
    result['original_file_hashes_unchanged'] = all(
        hashlib.sha256(Path(p).read_bytes()).hexdigest()==digest for p,digest in hashes.items())
    result['view_module_count'] = len(list(modules.glob('*.py')))
    (HERE/'validation_results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
