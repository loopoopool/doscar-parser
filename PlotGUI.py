import ProjectorGUI, SaveDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, doscar, parent=None, width=10, height=3, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self.axes.set_xlabel('$E-E_{F}$ (eV)', size=20)
        self.axes.set_xlim(min(doscar.energy), max(doscar.energy))
        self.axes.set_ylabel('states/N ($eV^{-1}$)', size=20)
        self.axes.set_ylim(0, max(doscar.dos)*1.05)
        self.axes.tick_params(labelsize=15)
        self.axes.plot(doscar.energy, doscar.dos, label='total')
        self.axes.legend(loc='best')

        super(MplCanvas, self).__init__(self.fig)
        self.setParent(parent)

        FigureCanvasQTAgg.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)

        self.colors = {0 : 'tab:blue', 1 : 'tab:orange', 2 : 'tab:green', 3 : 'tab:red', 
                4 : 'tab:purple', 5 : 'tab:brown', 6 : 'tab:pink', 7 : 'tab:gray', 
                8 : 'tab:olive', 9 : 'tab:cyan'}

class Ui_MainWindow(object):
    def setupUi(self, MainWindow, doscar):
        MainWindow.setObjectName(u"Density of States")
        MainWindow.resize(1000, 800)
        self.actionOpen_projector = QAction(MainWindow)
        self.actionOpen_projector.setObjectName(u"actionOpen_projector")
        self.actionOpen_projector.triggered.connect( self.open_projector )
        self.actionSave_As = QAction(MainWindow)
        self.actionSave_As.setObjectName(u"actionSave_As")
        self.actionSave_As.triggered.connect( self.save_as )
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        
        self.canvas = MplCanvas(doscar, width=5, height=4, dpi=100)
        self.horizontalLayout.addWidget(self.canvas)

        self.horizontalLayout.addWidget(self.canvas)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 859, 23))
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menuEdit.addAction(self.actionOpen_projector)
        self.menuFile.addAction(self.actionSave_As)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionOpen_projector.setText(QCoreApplication.translate("MainWindow", u"Open projector...", None))
        self.actionSave_As.setText(QCoreApplication.translate("MainWindow", u"Save As...", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

    def open_projector(self):
        self.projectorDialog.exec_()

    def save_as(self):
        self.saveDialog.saveFileDialog(self.canvas)
        


class App(QMainWindow, Ui_MainWindow):
    def __init__(self, doscar, parent=None):
        super(App, self).__init__(parent)
        self.setupUi(self, doscar)
        self.projectorDialog = ProjectorGUI.AppProj(doscar, self.canvas)
        self.saveDialog = SaveDialog.AppSave( self.canvas )

