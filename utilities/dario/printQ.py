import sys
import numpy as np
from ploos.Poscar import POSCAR as PP
from scipy.linalg import solve


##################################################
# rot matrix for 'tetragonal' cell
c45 = np.cos(0.25*np.pi)
s45 = np.sin(0.25*np.pi)
rot = np.array( [[c45, s45, 0], [-s45, c45, 0], [0, 0, 1]] )
##################################################



##################################################
# helper function to calculate Qs
def calculate_Q(pp, center, cooref, octamode):
    if (octamode == 'tetragonal'):
        oc = pp.octahedron(center)
    else:
        oc = pp.octahedron_cubic(center)
    # library gives octahedron in van Vleck convention
    # go to Bersuker convention
    # see Fig. 7 of pol paper for reference
    oc_b = np.roll(oc, 1)
    tmp = oc_b[0]
    oc_b[0] = oc_b[3]
    oc_b[3] = tmp
    coodist = np.array( [pp.getBondLength(o, center)[1] for o in oc_b] )
    if (octamode == 'tetragonal'):
        for i, x in enumerate(coodist):
            coodist[i] = rot @ x
    tmp = coodist - cooref
    return m @ tmp.flatten()
##################################################



##################################################
# read input parameters
##################################################
octamode = sys.argv[1]
print(octamode)
# takes values 'cubic' or 'tetragonal' according to whether the cell has been
# rotated by 45 deg
pref = PP( sys.argv[2] )
# reference POSCAR (this actually is used only for Q1, all other modes do not
# depend on reference structure)
OsRef = int( sys.argv[3] )
# Os site corresponding to the center of the octahedron of interest in the
# refrence POSCAR
pdist = PP( sys.argv[4] )
# distorted POSCAR
OsDist = int( sys.argv[5] )
# Os site corresponding to the center of the octahedron of interest in the
# distorted POSCAR
##################################################



##################################################
# transformation matrix X_i, Y_i, Z_i --> Q_k
# see table in Fig. 7 of polaron paper
##################################################
m = np.array( 
 [[ 0.0,  0.0,  1.0,  1.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0, -1.0, -1.0,
     0.0,  0.0,  0.0, -1.0, 0.0], #Q1
  [ 0.0,  0.0,  2.0, -1.0,  0.0,  0.0,  0.0, -1.0,  0.0,  0.0,  0.0, -2.0,  1.0,
      0.0,  0.0,  0.0,  1.0, 0.0], #Q3
  [ 0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0, -1.0,  0.0,  0.0,  0.0,  0.0, -1.0,
   0.0,  0.0,  0.0,  1.0,  0.0], #Q2
  [ 0.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0, -1.0,  0.0,  0.0,
   0.0,  0.0,  0.0,  0.0, -1.0], #Qyz
  [ 1.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0, -1.0,  0.0,  0.0,  0.0,
   0.0, -1.0,  0.0,  0.0,  0.0], #Qxz
  [ 0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,
   -1.0,  0.0, -1.0,  0.0,  0.0], #Qxy
  [ 1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0,
   0.0,  0.0,  1.0,  0.0,  0.0], #Q'x
  [ 0.0,  1.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0,
   1.0,  0.0,  0.0,  0.0,  0.0], #Q'y
  [ 0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0,  0.0,
      0.0, 1.0,  0.0,  0.0,  1.0], #Q'z
  [ 0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,
   0.0,  0.0,  0.0,  0.0,  0.0], #Q''x
  [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.0,
   0.0,  0.0,  0.0,  1.0,  0.0], #Q''y
  [ 0.0,  0.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,
   0.0,  0.0,  0.0,  0.0,  0.0], #Q''z
  [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0, -1.0,  0.0,  0.0,  0.0,
   0.0,  0.0,  1.0,  0.0,  0.0], #Q'xy
  [ 0.0,  1.0,  0.0,  0.0, -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0,
   -1.0,  0.0,  0.0,  0.0,  0.0], #Q'yz
  [ 0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0, -1.0,  0.0,  0.0,  0.0,  0.0,
   0.0,  1.0,  0.0,  0.0, -1.0], #Q'xz
  [ 0.0,  -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  1.0,  0.0,  0.0,
      0.0,  0.0,  0.0,  0.0,  -1.0], # Qryz
  [ 1.0,  0.0,  0.0,  0.0,  0.0,  -1.0,  0.0,  0.0,  0.0, -1.0,  0.0,  0.0,  0.0,
    0.0,   1.0,  0.0,  0.0,  0.0], # Qrxz
  [ 0.0,  0.0,  0.0,  0.0,  1.0,  0.0, -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,
   -1.0,  0.0,  1.0,  0.0,  0.0]], #Qrxy
             dtype=np.float64 )

m[0]    *= 1/np.sqrt(6)
m[1]    *= 0.5/np.sqrt(3)
m[2:9]  *= 0.5
m[9:12] *= 1.0/np.sqrt(2)
m[12:]  *= 0.5
##################################################



##################################################
# initialize reference octahedron
oc = pref.octahedron_cubic(OsRef)
# library gives octahedron in van Vleck convention
# go to Bersuker convention
oc_b = np.roll(oc, 1)
tmp = oc_b[0]
oc_b[0] = oc_b[3]
oc_b[3] = tmp
cooref = np.array( [pref.getBondLength(o, OsRef)[1] for o in oc_b] )
##################################################



##################################################
# initialize distorted octahedron
if (octamode == 'cubic'):
    oc = pdist.octahedron_cubic(OsDist)
elif (octamode == 'tetragonal'):
    oc = pdist.octahedron(OsDist)
else:
    print( 'octahedron not implemented for this cell symm' )
    exit(-1)
oc_b = np.roll(oc, 1)
tmp = oc_b[0]
oc_b[0] = oc_b[3]
oc_b[3] = tmp
coodist = np.array( [pdist.getBondLength(o, OsRef)[1] for o in oc_b] )
##################################################



##################################################
# calculate distortions
Qdist = calculate_Q(pdist, OsRef, cooref, octamode)
##################################################



##################################################
# printing
if (len(sys.argv) == 6):
    print( np.round( Qdist, 5) )
else:
    mode = int(sys.argv[6])
    print( np.round(Qdist[mode], 7) )
##################################################
