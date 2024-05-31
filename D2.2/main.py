from fmpy import *
from fmpy.util import plot_result
import numpy as np

def run_generated_fmu():
    fmu = 'TrussModel.fmu'
    print(dump(fmu))
    inputs = {'ElasticModulus': 3000}
    simulate_fmu(fmu, start_values=inputs,stop_time =0.001)

def run_bridge_model_FMU():
    fmu = 'Bridge.fmu'
    print(dump(fmu))

if __name__ == '__main__':
    run_generated_fmu()
