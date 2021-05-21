import sys
import Doscar, PlotGUI
from PyQt5.QtWidgets import QApplication

#if ( len(sys.argv) != 2 ): 
#    print('doscar-parser >> Wrong number of arguments.')
#    exit(404)

#print('\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
#print('%%%%%%%%%%%%% DOSCAR-PARSER %%%%%%%%%%%%%%%%%%%%%%')
#print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n')

#filename = sys.argv[1]
app = QApplication(sys.argv)
window = PlotGUI.App()
window.show()
app.exec_()
