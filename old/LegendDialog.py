from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog, canvas):
        self.canvas = canvas
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(381, 150)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(10)
        self.label.setFont(font)

        self.horizontalLayout.addWidget(self.label)

        self.lineEdit = QLineEdit(Dialog)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout.addWidget(self.lineEdit)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect( self.setSize )
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Set legend Size", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Size:", None))

    def setSize(self):
        size = int( self.lineEdit.text() )
        lines = {}
        for axis in self.canvas.axes.flatten():
            legend = axis.get_legend()
            if (legend): legend.remove()
            for line in axis.get_lines():
                lines[line.get_label()] = line
        ll = [ lines[x] for x in lines ]
        lb = [ x for x in lines ]

        self.canvas.axes.flatten()[0].legend(ll, lb, loc='upper right',
                prop={'size':size}) 
        self.canvas.draw()
        self.lineEdit.clear()
        self.reject()
        


class AppLegend(QDialog, Ui_Dialog):
    def __init__(self, canvas, parent=None):
        super(AppLegend, self).__init__(parent)
        self.setupUi(self, canvas)
