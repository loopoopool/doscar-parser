import sys
from Doscar import DOSCAR

doscar = DOSCAR('.')
atom = int(sys.argv[1])
print( doscar.sum_in_energy_interval(atom, 2.5, 3.1) ) 
