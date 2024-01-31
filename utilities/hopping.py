import sys
import numpy as np
from ploos.Poscar import POSCAR
from copy import deepcopy

p1 = POSCAR( sys.argv[1] )
p2 = POSCAR( sys.argv[2] )
xi = float( sys.argv[3] )

pend = deepcopy(p1)

pend.cartesianMatrix = (1.0 - xi)*p1.cartesianMatrix + xi*p2.cartesianMatrix
pend.write_to_file( 'POSCAR-{:.2f}.vasp'.format(xi), mode='D' )
