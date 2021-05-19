import sys, re
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget
import checkableComboBox
import numpy as np
from matplotlib import pyplot as plt

################################################################################
#              GUI
################################################################################

class Ui_Form(object):
    def setupUi(self, Form, doscar):
        Form.setObjectName("Form")
        Form.resize(434, 453)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 411, 431))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.spinBox = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.spinBox.setObjectName("first_atom")
        self.spinBox.setRange(1, doscar.natoms)
        self.horizontalLayout.addWidget(self.spinBox)
        spacerItem = QtWidgets.QSpacerItem(60, 40, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.spinBox_2 = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.spinBox_2.setObjectName("last_atom")
        self.spinBox_2.setRange(1, doscar.natoms)
        self.horizontalLayout.addWidget(self.spinBox_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.orbitals = checkableComboBox.CheckableComboBox(self.verticalLayoutWidget) 
        self.orbitals.addItems( doscar.guiLabel )
        self.verticalLayout_2.addWidget(self.orbitals)
        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)
        self.lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_2.addWidget(self.lineEdit)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName("addLine")
        self.pushButton.clicked.connect(self.clickAddLine)
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_2.setObjectName("save")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_3.setObjectName("close")
        self.pushButton_3.clicked.connect(self.close)
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_3.setText(_translate("Form", "Project onto atoms:"))
        self.label.setText(_translate("Form", "from:"))
        self.label_2.setText(_translate("Form", "to:"))
        self.label_4.setText(_translate("Form", "Project onto orbitals"))
        self.label_5.setText(_translate("Form", "Line label:"))
        self.pushButton.setText(_translate("Form", "Add line"))
        self.pushButton_2.setText(_translate("Form", "Save"))
        self.pushButton_3.setText(_translate("Form", "Close"))

    def clickAddLine(self):
        atomlist = np.arange( self.spinBox.value()-1, self.spinBox_2.value() )
        orblist = self.orbitals.currentData()
        mylabel = self.lineEdit.text()
        plt.plot(doscar.energy, doscar.projector(atomlist, orblist), label=mylabel)
        plt.draw()




class App(QWidget, Ui_Form):
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
            if ( lm ): self.label = todic( label_ispin1_lm[:ncol] )
            else: self.label = todic( label_ispin1[:ncol] )
        elif ( ispin==2 ):
            if ( lm ): self.label = todic( label_ispin1_lm[:ncol] )
            else: self.label = todic( label_ispin2[:ncol] )
        elif ( ncl ):
            if ( lm ): 
                self.label = todic( label_ncl_lm[:ncol] )
                self.guiLabel = label_ncl_lm[:ncol]
            else: self.label = todic( label_ncl[:ncol] )
        else: exit('\nUnrecognised structure. Aborting...\n')
        
        self.atomilst = []
        self.orblist = []
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
        plt.xlabel('$E-E_{F}$ (eV)', size=20)
        plt.xlim(min(self.energy), max(self.energy))
        plt.ylabel('states/N ($eV^{-1}$)', size=20)
        plt.ylim(0, max(self.dos)*1.05)
        plt.tick_params(labelsize=15)
        plt.plot(self.energy, self.dos, label='total')
        form = App(self)
        form.show()
        app.exec_()
        plt.legend(loc='best')
        plt.show()

# embed matplotlib in pyqt

filename = sys.argv[1]

print('\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
print('%%%%%%%%%%%%% DOSCAR-PARSER %%%%%%%%%%%%%%%%%%%%%%')
print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n')

doscar = DOSCAR(filename)
app = QApplication(sys.argv)
doscar.plot()




