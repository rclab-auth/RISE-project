
import numpy as np
import matplotlib.pyplot as plt
from fmup.fmi2slave import Fmi2Slave, Fmi2Causality, Fmi2Variability, Real
try:
    import openseespy.opensees as ops
except ImportError:
    ops=None

class TrussModel(Fmi2Slave):
    author ="RISE-Project"
    description="Simple Truss OpenSeesPy example"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # remove existing model
        self.ElaticModulus = 3000.0
        self.ux = 0.0
        self.uy = 0.0
        self.register_variable(Real('ElaticModulus', causality=Fmi2Causality.input))
        self.register_variable(Real('ux', causality=Fmi2Causality.output))
        self.register_variable(Real('uy', causality=Fmi2Causality.output))
        ops.wipe()

        # set modelbuilder
        ops.model('basic', '-ndm', 2, '-ndf', 2)

        # create nodes
        ops.node(1, 0.0, 0.0)
        ops.node(2, 144.0,  0.0)
        ops.node(3, 168.0,  0.0)
        ops.node(4,  72.0, 96.0)

        # set boundary condition
        ops.fix(1, 1, 1)
        ops.fix(2, 1, 1)
        ops.fix(3, 1, 1)

        # define materials
        ops.uniaxialMaterial("Elastic", 1, self.ElaticModulus)

        # define elements
        ops.element("Truss",1,1,4,10.0,1)
        ops.element("Truss",2,2,4,5.0,1)
        ops.element("Truss",3,3,4,5.0,1)

        # create TimeSeries
        ops.timeSeries("Linear", 1)

        # create a plain load pattern
        ops.pattern("Plain", 1, 1)

        # Create the nodal load - command: load nodeID xForce yForce
        ops.load(4, 100.0, -50.0)

        # ------------------------------
        # Start of analysis generation
        # ------------------------------

        # create SOE
        ops.system("BandSPD")
        ops.numberer("RCM")
        ops.constraints("Plain")
        ops.integrator("LoadControl", 1.0)
        ops.algorithm("Linear")
        ops.analysis("Static")
        ops.analyze(1)

    def do_step(self, current_time, step_size):

        print(f'Displacement ux: {ops.nodeDisp(4,1)}')
        print(f'Displacement uy: {ops.nodeDisp(4,2)}')
        return True