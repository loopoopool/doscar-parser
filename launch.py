import sys, Doscar, PlotGUI

if ( len(sys.argv) != 2 ): 
    print('doscar-parser >> Wrong number of arguments.')
    exit(404)

print('\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
print('%%%%%%%%%%%%% DOSCAR-PARSER %%%%%%%%%%%%%%%%%%%%%%')
print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n')

filename = sys.argv[1]
dos = Doscar.DOSCAR(filename)
dos.plot()
