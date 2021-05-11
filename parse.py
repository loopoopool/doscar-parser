import sys, re
import numpy as np
from matplotlib import pyplot as plt

def remove_all_whitespace(x):
    pattern = re.compile(r'\s+')
    return re.sub(pattern, '', x)

def whitespace_to_semicol(x):
    pattern = re.compile(r'\s+')
    return re.sub(pattern, ';', x)

def extract_coord(x):
    coo = whitespace_to_semicol( x ).split( ';' )[1:4]
    return np.array( [float(ci) for ci in coo] )


if ( len(sys.argv) != 2 ): 
    print('polaroncar >> Wrong number of arguments.')
    exit(404)

filename = sys.argv[1]

with open(filename, 'r') as f:
    doscar = f.readlines()

nions, _, pdos, _ = [int(n) for n in whitespace_to_semicol( doscar[0] ).split( ';' )[1:-1]]
vol, a, b, c, potim = [float(n) for n in whitespace_to_semicol( doscar[1] ).split( ';' )[1:-1]]
tebeg = float( remove_all_whitespace( doscar[2] ) )
system = remove_all_whitespace( doscar[4] )
emax, emin, nedos, efermi, _ = [float(n) for n in whitespace_to_semicol( doscar[5] ).split( ';' )[1:-1]]
nedos = int(nedos)
counter = 6
energy = np.zeros(nedos)
dos = np.zeros(nedos)
idos = np.zeros(nedos)
for i in range(nedos):
    energy[i], dos[i], idos[i] = (float(x) for x in whitespace_to_semicol( doscar[counter+i] ).split( ';' )[1:-1])

energy -= efermi
plt.xlabel('energy (eV)', size=20)
plt.xlim(min(energy), max(energy))
plt.ylabel('states/N ($eV^{-1}$)', size=20)
plt.ylim(0, max(dos)*1.05)
plt.tick_params(labelsize=15)
plt.plot(energy, dos)
plt.show()
#ucell = np.array( [extract_coord(x) for x in doscar[2:5]] )
#species = whitespace_to_semicol( doscar[5] ).split( ';' )[1:-1]
#nspecies = [int(n) for n in whitespace_to_semicol( doscar[6] ).split( ';' )[1:-1]]
#natoms = sum(nspecies)
#coosys = remove_all_whitespace( doscar[7] )
#pox = atomic_positions(doscar, natoms)
#
print(efermi)
