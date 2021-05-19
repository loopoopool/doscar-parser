import sys, re
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import checkableComboBox
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
################################################################################
#              GUI
################################################################################
class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, doscar, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.set_xlabel('$E-E_{F}$ (eV)', size=20)
        self.axes.set_xlim(min(doscar.energy), max(doscar.energy))
        self.axes.set_ylabel('states/N ($eV^{-1}$)', size=20)
        self.axes.set_ylim(0, max(doscar.dos)*1.05)
        self.axes.tick_params(labelsize=15)
        self.axes.plot(doscar.energy, doscar.dos)
        super(MplCanvas, self).__init__(fig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow, doscar):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        self.left = 10
        self.top = 10
        self.width = 1920
        self.height = 1080
        self.setGeometry(self.left, self.top, self.width, self.height)
        #MainWindow.resize(1131, 657)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(30, 10, 411, 601))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_2.addWidget(self.label_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.spinBox = QSpinBox(self.verticalLayoutWidget)
        self.spinBox.setObjectName("first_atom")
        self.spinBox.setRange(1, doscar.natoms)

        self.horizontalLayout.addWidget(self.spinBox)

        self.horizontalSpacer = QSpacerItem(60, 40, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label_2 = QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.spinBox_2 = QSpinBox(self.verticalLayoutWidget)
        self.spinBox_2.setObjectName("last_atom")
        self.spinBox_2.setRange(1, doscar.natoms)

        self.horizontalLayout.addWidget(self.spinBox_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.label_4 = QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_2.addWidget(self.label_4)

        self.orbitals = checkableComboBox.CheckableComboBox(self.verticalLayoutWidget) 
        self.orbitals.addItems( doscar.guiLabel )

        self.verticalLayout_2.addWidget(self.orbitals)

        self.label_5 = QLabel(self.verticalLayoutWidget)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_2.addWidget(self.label_5)

        self.lineEdit = QLineEdit(self.verticalLayoutWidget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.verticalLayout_2.addWidget(self.lineEdit)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton = QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName(u"add_line")
        self.pushButton.clicked.connect(self.clickAddLine)

        self.horizontalLayout_2.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.verticalLayoutWidget)
        self.pushButton_2.setObjectName(u"save")

        self.horizontalLayout_2.addWidget(self.pushButton_2)

        self.pushButton_3 = QPushButton(self.verticalLayoutWidget)
        self.pushButton_3.setObjectName(u"close")
        self.pushButton_3.clicked.connect(self.close)

        self.horizontalLayout_2.addWidget(self.pushButton_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontaLayoutWidget = QWidget(self.centralwidget)
        self.horizontaLayoutWidget.setGeometry(QRect(460, 70, 651, 441))
        self.horizontalLayout_3 = QHBoxLayout(self.horizontaLayoutWidget)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.canvas = MplCanvas(doscar, width=5, height=4, dpi=100)
        self.horizontalLayout_3.addWidget(self.canvas)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1131, 23))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Project onto atoms:", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"from:", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"to:", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Project onto orbitals", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Line label:", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Add line", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Close", None))
    # retranslateUi

    def clickAddLine(self):
        atomlist = np.arange( self.spinBox.value()-1, self.spinBox_2.value() )
        orblist = self.orbitals.currentData()
        mylabel = self.lineEdit.text()
        self.canvas.axes.plot(doscar.energy, doscar.projector(atomlist, orblist), label=mylabel)
        self.canvas.draw()


class App(QMainWindow, Ui_MainWindow):
    def __init__(self, doscar, parent=None):
        super(App, self).__init__(parent)
        self.setupUi(self, doscar)

################################################################################

label_ispin1 = [ 's', 'p', 'd']
label_ispin1_lm = [ 's', 'px', 'py', 'pz', 'dxy', 'dyz', 'dz2', 'dxz', 'dx2' ]
label_ispin2 = [ 's+', 's-', 'p+', 'p-', 'd+', 'd-' ]
label_ispin2_lm = [ 's+', 'px+', 'py+', 'pz+', 'dxy+', 'dyz+', 'dz2+', 'dxz+', 'dx2+', 
        's-', 'px-', 'py-', 'pz-', 'dxy-', 'dyz-', 'dz2-', 'dxz-', 'dx2-' ]
label_ncl = [ 'stot' , 's(mx)', 's(my)', 's(mz)', 'ptot', 'p(mx)', 'p(my)', 'p(mz)', 
        'dtot', 'd(mx)', 'd(my)', 'd(mz)' ]
label_ncl_lm = [ 'stot', 's(mx)', 's(my)', 's(mz)', 'pxtot', 'px(mx)', 'px(my)', 'px(mz)', 
        'pytot', 'py(mx)', 'py(my)', 'py(mz)', 'pztot', 'pz(mx)', 'pz(my)', 'pz(mz)', 
        'dxytot', 'dxy(mx)', 'dxy(my)', 'dxy(mz)', 'dyztot', 'dyz(mx)', 'dyz(my)', 'dyz(mz)',
        'dz2tot', 'dz2(mx)', 'dz2(my)', 'dz2(mz)', 'dxztot', 'dxz(mx)', 'dxz(my)', 'dxz(mz)',
        'dx2tot', 'dx2(mx)', 'dx2(my)', 'dx2(mz)' ]

def remove_all_whitespace(x):
    pattern = re.compile(r'\s+')
    return re.sub(pattern, '', x)

def whitespace_to_semicol(x):
    pattern = re.compile(r'\s+')
    return re.sub(pattern, ';', x)

def split(x):
    return whitespace_to_semicol( x ).split( ';' )[1:-1]

def extract_coord(x):
    coo = whitespace_to_semicol( x ).split( ';' )[1:4]
    return np.array( [float(ci) for ci in coo] )


if ( len(sys.argv) != 2 ): 
    print('polaroncar >> Wrong number of arguments.')
    exit(404)

def parse_yn_bool(x):
    if ( x == 'y' ): 
        return True
    elif ( x == 'n' ): 
        return False
    else:
        print('\n!!!!! Invalid Answer - Aborting !!!!!\n')
        exit(-1)

# discarding energy column
# l=0 lm=f ncl=f isp=1 ncol=1
# l=0 lm=f ncl=f isp=2 ncol=2
# l=0 lm=f ncl=t       ncol=3
# l=0 lm=t ncl=f isp=1 ncol=1
# l=0 lm=t ncl=f isp=2 ncol=2
# l=0 lm=t ncl=t       ncol=3
# l=1 lm=f ncl=f isp=1 ncol=2
# l=1 lm=f ncl=f isp=2 ncol=4
# l=1 lm=f ncl=t       ncol=6
# l=1 lm=t ncl=f isp=1 ncol=4
# l=1 lm=t ncl=f isp=2 ncol=8
# l=1 lm=t ncl=t       ncol=17
# l=2 lm=f ncl=f isp=1 ncol=4
# l=2 lm=f ncl=f isp=2 ncol=8
# l=2 lm=f ncl=t       ncol=15
# l=2 lm=t ncl=f isp=1 ncol=9
# l=2 lm=t ncl=f isp=2 ncol=18
# l=2 lm=t ncl=t       ncol=38

def todic(labelarray):
    return { x : i for i, x in enumerate(labelarray) }



class DOSCAR:
    ########################################
    # USEFUL LOCAL VARS
    ########################################
    #######################################
    # FUNCTIONS
    #######################################

    ##### COSNTRUCTOR #####
    def __init__(self, filename):

        ispin=0
        ncl = parse_yn_bool( input('Non-collinear?(y/n): ') )
        if not ncl: ispin = int( input('ISPIN >> ') )
        lm = parse_yn_bool( input('lm-decomposed dos?(y/n): ') )
        with open(filename, 'r') as f:
            doscar = f.readlines()

        self.natoms, _, pdos, _ = [int(n) for n in split( doscar[0] )]
        vol, a, b, c, potim = [float(n) for n in split( doscar[1] )]
        tebeg = float( remove_all_whitespace( doscar[2] ) )
        system = remove_all_whitespace( doscar[4] )
        emax, emin, nedos, efermi, _ = [float(n) for n in split( doscar[5] )]
        self.nedos = int(nedos)
        counter = 6
        self.energy = np.zeros(self.nedos)

        if ( ispin != 2 ):
            self.dos = np.zeros(self.nedos)
            for i in range(self.nedos):
                self.energy[i], self.dos[i], _ = (float(x) for x in split( doscar[counter+i] ))
        else:
            self.dos_up = np.zeros(self.nedos)
            self.dos_down = np.zeros(self.nedos)
            for i in range(self.nedos):
                self.energy[i], self.dos_up[i], self.dos_down[i], _ = (float(x) for x in split( doscar[counter+i] ))

        self.energy -= efermi

        counter += self.nedos
        # skip header
        counter += 1
        ncol = len( split( doscar[self.nedos+7] ) ) - 1 # remove one col for energies
        self.pldos = np.zeros((self.natoms, self.nedos, ncol))

        for i in range(self.natoms):
            for j in range(self.nedos):
                self.pldos[i,j] = np.array( [float(x) for x in split( doscar[counter] )[1:] ] )
                counter += 1
            # skip header
            counter += 1

        # Extract labels
        global label_ispin1_lm, label_ispin1, label_ispin2_lm, label_ispin2, label_ncl_lm, label_ncl
        if ( ispin==1 ):
            if ( lm ): self.guiLabel = label_ispin1_lm[:ncol] 
            else: self.guiLabel = label_ispin1[:ncol]
        elif ( ispin==2 ):
            if ( lm ): self.guiLabel = label_ispin1_lm[:ncol]
            else: self.guiLabel = label_ispin2[:ncol]
        elif ( ncl ):
            if ( lm ): 
                self.guiLabel = label_ncl_lm[:ncol]
            else: self.guiLabel = label_ncl[:ncol]
        else: exit('\nUnrecognised structure. Aborting...\n')
        self.label = todic( self.guiLabel )
    ##############################  

    ##### PROJECTOR #####
    def projector(self, atoms, orbitals):
        projected = np.zeros(self.nedos)
        for aa in atoms:
            for oo in orbitals:
                projected += self.pldos[ aa, :, self.label[oo] ]
        return projected
    ############################## 

    ##### PLOTTER #####
    def plot(self):
        form = App(self)
        form.show()
        app.exec_()
        #plt.plot(self.energy, self.dos, label='total')
        #plt.legend(loc='best')
        #plt.show()

# embed matplotlib in pyqt

filename = sys.argv[1]

print('\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
print('%%%%%%%%%%%%% DOSCAR-PARSER %%%%%%%%%%%%%%%%%%%%%%')
print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n')

doscar = DOSCAR(filename)
app = QApplication(sys.argv)
doscar.plot()





