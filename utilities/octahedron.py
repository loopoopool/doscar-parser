import sys
import numpy as np
from ploos.Poscar import POSCAR as PP

p = PP( sys.argv[1])

# octahedron ref
OsRef = int( sys.argv[2] )
oc = p.octahedron(OsRef)

# library gives octahedron in van Vleck convention
# go to Bersuker convention
oc_b = np.roll(oc, 1)
tmp = oc_b[0]
oc_b[0] = oc_b[3]
oc_b[3] = tmp
bl = np.array( [p.getBondLength(o, OsRef)[0] for o in oc_b] )

for i, b in zip(oc_b, bl): print(i, ' : ', np.round(b, 4))
