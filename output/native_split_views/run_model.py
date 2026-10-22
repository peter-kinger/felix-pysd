"""Run selected core outputs from the native split-view PySD model."""
import argparse
from pathlib import Path
import time
import numpy as np
import pysd

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--final-time',type=int,default=1902)
    args = parser.parse_args()
    if not 1900 <= args.final_time <= 2100:
        parser.error('--final-time must be between 1900 and 2100')
    model = pysd.load(HERE/'FeliX3_ISE_v26_final_fixed.py')
    start = time.perf_counter()
    result = model.run(
        return_columns=['Population','Gross World Product','Total Labor Force',
                        'Temperature Change from Preindustrial',
                        'Atmospheric Concentration CO2','Forest Land'],
        initial_condition='original',final_time=args.final_time,time_step=.125,
        return_timestamps=np.arange(1900,args.final_time+1),
        cache_output=False,progress=False)
    path = HERE/'example_results.csv'
    result.to_csv(path)
    print(result.tail())
    print(f'Simulation seconds: {time.perf_counter()-start:.3f}')
    print(f'Results: {path}')


if __name__=='__main__':
    main()
