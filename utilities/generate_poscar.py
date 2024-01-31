import sys
import numpy as np
from ploos.Poscar import POSCAR as PP
from copy import deepcopy
from scipy.linalg import solve

m = np.array( 
 [[ 0.0,  0.0,  1.0,  1.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0, -1.0, -1.0,
     0.0,  0.0,  0.0, -1.0, 0.0],
  [ 0.0,  0.0,  2.0, -1.0,  0.0,  0.0,  0.0, -1.0,  0.0,  0.0,  0.0, -2.0,  1.0,
      0.0,  0.0,  0.0,  1.0, 0.0],
  [ 0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0, -1.0,  0.0,  0.0,  0.0,  0.0, -1.0,  0.0,  0.0,  0.0,  1.0,  0.0],
  [ 0.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0, -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
  [ 1.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0, -1.0,  0.0,  0.0,  0.0,  0.0, -1.0,  0.0,  0.0,  0.0],
  [ 0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0,  0.0, -1.0,  0.0,  0.0],
  [ 1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0],
  [ 0.0,  1.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0,  0.0],
  [ 0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0,  0.0,
      0.0, 1.0,  0.0,  0.0,  1.0], #Qpz
  [ 0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.0],
  [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0],
  [ 0.0,  0.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
  [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0, -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0],
  [ 0.0,  1.0,  0.0,  0.0, -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0, -1.0,  0.0,  0.0,  0.0,  0.0],
  [ 0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0, -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0, -1.0],
  [ 0.0,  0.0,  0.0,  0.0,  1.0,  0.0, -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,
    -1.0,  0.0,  0.0,  0.0,  1.0],
  [ 1.0,  0.0,  0.0,  0.0,  0.0,  -1.0,  0.0,  0.0,  0.0, -1.0,  0.0,  0.0,  0.0,
    0.0,   1.0,  0.0,  0.0,  0.0],
  [ 0.0,  -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  1.0,  0.0,  0.0,
      0.0,  0.0,  0.0,  0.0,  -1.0]], dtype=np.float64 )


m[0]    *= 1/np.sqrt(6)
m[1]    *= 0.5/np.sqrt(3)
m[2:9]  *= 0.5
m[9:12] *= 1.0/np.sqrt(2)
m[12:]  *= 0.5

c45 = np.cos(0.25*np.pi)
s45 = np.sin(0.25*np.pi)

def calculate_Q(pp, OsRef, cooref):
    oc = pp.octahedron(OsRef)
    # library gives octahedron in van Vleck convention
    # go to Bersuker convention
    oc_b = np.roll(oc, 1)
    tmp = oc_b[0]
    oc_b[0] = oc_b[3]
    oc_b[3] = tmp
    coodist = np.array( [pp.getBondLength(o, OsRef)[1] for o in oc_b] )
    rot = np.array( [[c45, s45, 0], [-s45, c45, 0], [0, 0, 1]] )
    for i, x in enumerate(coodist):
        coodist[i] = rot @ x
    tmp = coodist - cooref
    return m @ tmp.flatten()

pref = PP( sys.argv[1])

# octahedron ref
OsRef = int( sys.argv[2] )
oc = pref.octahedron_cubic(OsRef)

# library gives octahedron in van Vleck convention
# go to Bersuker convention
oc_b = np.roll(oc, 1)
tmp = oc_b[0]
oc_b[0] = oc_b[3]
oc_b[3] = tmp
cooref = np.array( [pref.getBondLength(o, OsRef)[1] for o in oc_b] )

pdist = PP( sys.argv[3] )
OsRef = int( sys.argv[4] )
oc = pdist.octahedron(OsRef)
oc_b = np.roll(oc, 1)
tmp = oc_b[0]
oc_b[0] = oc_b[3]
oc_b[3] = tmp
coodist = np.array( [pdist.getBondLength(o, OsRef)[1] for o in oc_b] )
Qdist = calculate_Q(pdist, OsRef, cooref)

original = solve(m, Qdist)

mode = int( sys.argv[5] )
alpha = float( sys.argv[6] )

pp = deepcopy(pdist)
pp.SDflags[OsRef-1] = ['F', 'F', 'F']
Qdist_new = np.array( [x for x in Qdist] )
Qdist_new[mode] *= alpha
new = solve(m, Qdist_new)
tmp = new - original
dx = np.round(tmp.reshape((6,3)), 4)
rot = np.array( [[c45, -s45, 0], [s45, c45, 0], [0, 0, 1]] )

for i, o in enumerate(oc_b):
    tmp = pdist.getCartesianCoordinates( o )
    pp.setCartesianCoordinates( o, tmp + rot @ dx[i] )
    pp.SDflags[o-1] = ['F', 'F', 'F']

pp.write_to_file( sys.argv[7], mode='D')
