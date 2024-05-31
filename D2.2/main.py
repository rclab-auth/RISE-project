from fmpy import *
from fmpy.util import plot_result
import numpy as np

def main():
    fmu = 'TrussModel.fmu'
    print(dump(fmu))
    inputs = np.array(3000)
    simulate_fmu(fmu, start_values={'ElaticModulus': 4000},stop_time =0.001)
    dump(fmu)



if __name__ == '__main__':
    main()
