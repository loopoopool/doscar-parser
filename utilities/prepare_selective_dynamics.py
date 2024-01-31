import sys
from ploos.Poscar import POSCAR

infile = sys.argv[1]
outfile = sys.argv[2]

poscar = POSCAR(infile)

poscar.selectiveDynamicsConstraintBorders(outfile) 
