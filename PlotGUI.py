import Intro, Doscar, ProjectorGUI, SaveDialog, OpenDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, doscar, parent=None, width=10, height=3, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self.axes.set_xlabel('$E-E_{F}$ (eV)', size=20)
        self.axes.set_xlim(min(doscar.energy), max(doscar.energy))
        self.axes.set_ylabel('states ($eV^{-1}$)', size=20)
        self.axes.set_ylim(0, max(doscar.dos)*1.05)
        self.axes.tick_params(labelsize=15)
        self.axes.plot(doscar.energy, doscar.dos, label='total')
        self.axes.axvline(x=0.0, color='black')
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
        self.setWindowIcon( QIcon('icon.png') )
        
        # remove line
        self.actionRemoveLine = QAction(MainWindow)
        self.actionRemoveLine.setObjectName(u'actionRemoveLine')
        self.actionRemoveLine.triggered.connect( self.removeLine )

        # open projector
        self.actionOpen_projector = QAction(MainWindow)
        self.actionOpen_projector.setObjectName(u"actionOpen_projector")
        self.actionOpen_projector.triggered.connect( self.open_projector )
        if not doscar.enableProjector:
            self.actionOpen_projector.setEnabled(False)
        
        # save as
        self.actionSave_As = QAction(MainWindow)
        self.actionSave_As.setObjectName(u"actionSave_As")
        self.actionSave_As.triggered.connect( self.save_as )

        # open folder
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"open")
        self.actionOpen.triggered.connect( self.open )

        # plot on top
        self.actionOverlay = QAction(MainWindow)
        self.actionOverlay.setObjectName(u'overlay')
        self.actionOverlay.triggered.connect( self.overlay )
        
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        
        #self.horizontalLayout = QHBoxLayout(self.centralwidget)
        #self.horizontalLayout.setObjectName(u"horizontalLayout")

        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.canvas = MplCanvas(doscar, width=5, height=4, dpi=100)

        #self.verticalLayout.addWidget(self.canvas)
        
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        
        self.verticalLayout.addWidget(self.toolbar)
        self.verticalLayout.addWidget(self.canvas)

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
        self.menuEdit.addAction(self.actionRemoveLine)
        self.menuEdit.addAction(self.actionOpen_projector)
        self.menuEdit.addAction(self.actionOverlay)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave_As)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionOpen_projector.setText(QCoreApplication.translate("MainWindow", u"Open projector...", None))
        self.actionSave_As.setText(QCoreApplication.translate("MainWindow", u"Save As...", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open project...", None))
        self.actionOverlay.setText(QCoreApplication.translate("MainWindow", u"Overlay DOS...", None))
        self.actionRemoveLine.setText(QCoreApplication.translate("MainWindow", u"Remove line...", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))

    def open_projector(self):
        self.projectorDialog.exec_()

    def save_as(self):
        self.saveDialog.saveFileDialog(self.canvas)

    def open(self):
        path = self.openDialog.openDirectoryDialog()
        doscar = Doscar.DOSCAR( path )
        self.setupUi( self, doscar )
        self.projectorDialog = ProjectorGUI.AppProj( doscar, self.canvas )

    def overlay(self):
        path = self.openDialog.openDirectoryDialog()
        doscar = Doscar.DOSCAR( path )
        self.canvas.axes.plot(doscar.energy, doscar.dos, label='new')
        self.canvas.axes.legend(loc='best')
        self.canvas.draw()
        self.canvas.axes.autoscale_view()

    def removeLine(self):



class App(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        intro = Intro.AppIntro()
        intro.exec_()
        self.openDialog = OpenDialog.AppOpen()
        path = self.openDialog.openDirectoryDialog()
        doscar = Doscar.DOSCAR( path )
        self.setupUi( self, doscar )
        self.projectorDialog = ProjectorGUI.AppProj( doscar, self.canvas )
        self.saveDialog = SaveDialog.AppSave( self.canvas )

