import numpy as np
from ploos import Intro, Doscar, ProjectorGUI, SaveDialog, OpenDialog, LegendDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from matplotlib import pyplot as plt

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, doscar, parent=None, width=10, height=3, dpi=100):
#    def __init__(self, doscar, width=10, height=3, dpi=100):
        self.doscar = [ doscar ] 
        self.ndoscar = 1
        self.compare = False
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = np.array( [self.fig.add_subplot()] )
        self.axes[0].set_xlabel('$E-E_{F}$ (eV)', size=30)
        self.axes[0].set_xlim(min(doscar.energy), max(doscar.energy))
        self.axes[0].set_ylabel('states ($eV^{-1}$)', size=30)
        self.axes[0].set_ylim(0, np.average(doscar.dos))
        self.axes[0].tick_params(labelsize=25)
        self.axes[0].plot(doscar.energy, doscar.dos, label='total', color='lightgrey')
        self.axes[0].fill_between(doscar.energy, np.zeros(doscar.energy.shape), doscar.dos, color='lightgrey', alpha=0.6)
        self.axes[0].axvline(x=0.0, color='black', label='fermi')
        self.axes[0].legend(loc='upper right', prop={'size' : 20})
        
        super(MplCanvas, self).__init__(self.fig)

        self.setParent(parent)

        self.colors = {0 : 'tab:blue', 1 : 'tab:orange', 2 : 'tab:green', 3 : 'tab:red', 
                4 : 'tab:purple', 5 : 'tab:brown', 6 : 'tab:pink', 7 : 'tab:gray', 
                8 : 'tab:olive', 9 : 'tab:cyan'}

#        self.axes = self.fig.subplots(111)
#        self.axes.set_xlabel('$E-E_{F}$ (eV)', size=30)
#        self.axes.set_xlim(min(doscar.energy), max(doscar.energy))
#        self.axes.set_ylabel('states ($eV^{-1}$)', size=30)
#        self.axes.set_ylim(0, np.average(doscar.dos))
#        self.axes.tick_params(labelsize=25)
#        self.axes.plot(doscar.energy, doscar.dos, label='total', color='lightgrey')
#        self.axes.fill_between(doscar.energy, np.zeros(doscar.energy.shape), doscar.dos, color='lightgrey', alpha=0.6)
#        self.axes.axvline(x=0.0, color='black', label='fermi')
        
        FigureCanvasQTAgg.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow, doscar):
        MainWindow.setObjectName(u"Density of States")
        MainWindow.resize(1000, 800)
        self.setWindowIcon( QIcon('icon.png') )
        
        # remove line
#        self.actionRemoveLine = QAction(MainWindow)
#        self.actionRemoveLine.setObjectName(u'actionRemoveLine')
#        self.actionRemoveLine.triggered.connect( self.removeLine )

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
        
        # compare
        self.actionCompare = QAction(MainWindow)
        self.actionCompare.setObjectName(u'compare')
        self.actionCompare.triggered.connect( self.compare )
        
        # set legend size
        self.actionLegendSize = QAction(MainWindow)
        self.actionLegendSize.setObjectName(u'legend_size')
        self.actionLegendSize.triggered.connect( self.legend_size )
        
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
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
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
        self.menubar.addAction(self.menuView.menuAction())

        self.menuView.addAction(self.actionLegendSize)
#        self.menuEdit.addAction(self.actionRemoveLine)
        self.menuEdit.addAction(self.actionOpen_projector)
        self.menuEdit.addAction(self.actionOverlay)
        self.menuEdit.addAction(self.actionCompare)
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
        self.actionCompare.setText(QCoreApplication.translate("MainWindow", u"Compare DOS...", None))
#        self.actionRemoveLine.setText(QCoreApplication.translate("MainWindow", u"Remove line...", None))
        self.actionLegendSize.setText(QCoreApplication.translate("MainWindow", u"Set legend size", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))

    def open_projector(self):
        self.projectorDialog.exec_()

    def save_as(self):
        self.saveDialog.saveFileDialog(self.canvas)

    def open(self):
        path = self.openDialog.openDirectoryDialog()
        doscar = Doscar.DOSCAR( self.path )
        self.setupUi( self, doscar )
        self.projectorDialog = ProjectorGUI.AppProj( self.canvas )

    def overlay(self):
        path = self.openDialog.openDirectoryDialog()
        doscar = Doscar.DOSCAR( path )
        self.canvas.axes[0].plot(doscar.energy, doscar.dos, label='new')
#        self.canvas.axes.axvline( x=doscar.efermi - self.doscar.efermi,
#               color='red' )
        self.canvas.axes[0].legend(loc='best', prop={'size' : 20})
        self.canvas.draw()
        self.canvas.axes[0].autoscale_view()

    def compare( self ):
        self.compare=True
        path = self.openDialog.openDirectoryDialog()
        self.canvas.doscar.append( Doscar.DOSCAR( path ) )
        self.canvas.nodoscar = 2
        self.canvas.fig.clf()
        xmin = max( [ min(self.canvas.doscar[0].energy), min(self.canvas.doscar[1].energy) ] )
        xmax = min( [ max(self.canvas.doscar[0].energy),
            max(self.canvas.doscar[1].energy) ] )
        ymax = min( [ np.average(self.canvas.doscar[0].dos),
            np.average(self.canvas.doscar[1].dos) ] )

        self.canvas.axes = self.canvas.fig.subplots(nrows=2, ncols=1,
            sharex=True, sharey=True) 
        self.canvas.axes.flatten()[-1].set_xlabel('$E-E_{F}$ (eV)', size=30)
        self.projectorDialog.axis.clear()
        self.projectorDialog.axis.addItems( [ str(i) for i,x in enumerate(self.canvas.axes) ] )
        for i, axis in enumerate(self.canvas.axes.flatten()):
            axis.set_xlim( xmin, xmax )
            axis.set_ylabel('states ($eV^{-1}$)', size=30)
            axis.set_ylim(0, ymax)
            axis.tick_params(labelsize=25)
            axis.axvline(x=0.0, color='black')
            axis.plot(self.canvas.doscar[i].energy, self.canvas.doscar[i].dos,
                    label='total', color='lightgrey')
            axis.fill_between(self.canvas.doscar[i].energy,
                    np.zeros(self.canvas.doscar[i].energy.shape),
                    self.canvas.doscar[i].dos, color='lightgrey', alpha=0.6)
#            axis.legend(loc='best', prop={'size' : 20})
#        self.canvas.legend = self.canvas.fig.legend(loc='upper right')
#        handles, labels = self.canvas.axes[-1].get_legend_handles_labels()
#        self.canvas.fig.legend(handles, labels, loc='upper right')
#        
#        self.canvas.axes[1].set_ylabel('states ($eV^{-1}$)', size=30)
#        self.canvas.axes[1].set_ylim(0, np.average(self.canvas.doscar[1].dos))
#        self.canvas.axes[1].tick_params(labelsize=25)
#        self.canvas.axes[1].plot(self.canvas.doscar[1].energy, self.canvas.doscar[1].dos, label='new', color='lightgrey')
#        self.canvas.axes[1].fill_between(self.canvas.doscar[1].energy,
#                np.zeros(self.canvas.doscar[1].energy.shape),
#                self.canvas.doscar[1].dos, color='lightgrey', alpha=0.6)
#        self.canvas.axes[1].legend(loc='best', prop={'size' : 20})

        self.canvas.fig.subplots_adjust( hspace=0 )
        self.canvas.draw()
#        self.canvas.axes.autoscale_view()
#        self.canvas.new_axis.autoscale_view()

    def legend_size(self):
        self.legendDialog = LegendDialog.AppLegend( self.canvas )
        self.legendDialog.exec_()

#    def removeLine(self):



class App(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None, path=None):
        super(App, self).__init__(parent)
        self.openDialog = OpenDialog.AppOpen()
        if path is None:
            intro = Intro.AppIntro()
            intro.exec_()
            path = self.openDialog.openDirectoryDialog()
        doscar = Doscar.DOSCAR( path )
        self.setupUi( self, doscar )
        self.projectorDialog = ProjectorGUI.AppProj( self.canvas )
        self.saveDialog = SaveDialog.AppSave( self.canvas )
        self.legendDialog = LegendDialog.AppLegend( self.canvas )

