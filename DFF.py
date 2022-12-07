#UI Imports
from PyQt5.QtWidgets import QWidget, QFrame, QGridLayout, QApplication, QPushButton, QLabel, QFileDialog
#from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
import sys
import os



###Data Imports
#import os
#import numpy as np
#import pandas as pd

###Pandas options
#pd.set_option('display.max_rows', None)
#pd.set_option('display.max_columns', None)

###Path variables
DEFAULT_SAVE_PATH = os.path.expanduser('~\Documents')
PATH_MAIN = ''
PATH_COMP = ''

class UI(QWidget):
    def __init__(self):
        super(UI, self).__init__()
        #Set Base Window Parameters
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFixedWidth(700)
        self.setFixedHeight(400)
        self.setObjectName('MainWindow')
        self.layout = QGridLayout() #Instantiate grid for Main Widget
        self.setLayout(self.layout)

        #Initialize Grid
        grid = QGridLayout()


        #Set Base Frame
        frame = QFrame(self)
        frame.setFixedWidth(700)
        frame.setFixedHeight(400)
        frame.setObjectName('MainFrame')
        frame.setLayout(grid)

        #Set Application Label
        menuLabel = QLabel(self)
        menuLabel.setObjectName('MenuLabel')
        menuLabel.setText('Duplicate File Finder')
        menuLabel.setAlignment(Qt.AlignCenter)
        
        #Add Directory Labels
        mainLabel = QLabel(self)
        mainLabel.setObjectName('MainDirectory')
        mainLabel.setWordWrap(True)
        mainLabel.setText('Main Directory HERE')

        compLabel = QLabel(self)
        compLabel.setObjectName('CompDirectory')
        compLabel.setWordWrap(True)
        compLabel.setText('Comp Directory HERE')

        #Add Buttons
        button1 = self.addButton('Main Directory','Button1', None, lambda: selectDirectory(PATH))
        button2 = self.addButton('Comparison Directory','Button2', None, lambda: print('Comparison Directory'))
        exitButton = self.addButton('\u2715', 'ExitButton', 'Exit Application', lambda: sys.exit(app.exec()))
        exportButton = self.addButton('Export Results', 'ExportButton', 'Export List to File', lambda: print('Exported!'))

        #Grid Positioning
        grid.addWidget(menuLabel, 0, 1, 1, 12)
        grid.addWidget(mainLabel, 2, 1, 10, 6)
        grid.addWidget(compLabel, 2, 7, 10, 6)
        grid.addWidget(button1, 1, 1, 1, 6)
        grid.addWidget(button2, 1, 7, 1, 6)
        grid.addWidget(exitButton, 0, 12)
        grid.addWidget(exportButton, 12, 1, 1, 12)

        #Set Styling
        self.css()
        self.show()
    
    def addButton(self, name, id, tooltip, myFunction):
        assert type(name) == str
        assert type(id) == str
        button = QPushButton(self)
        button.setText(name)
        button.setObjectName(id)
        button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        button.setToolTip(tooltip)
        button.clicked.connect(myFunction)

        return button

    def css(self):
        with open('DFF.css') as file:
            sheet = file.read()
            self.setStyleSheet(sheet)

    def selectDirectory(self, targetPath):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory", DEFAULT_SAVE_PATH))
        if file:
            targetPath = file
            print(targetPath)


    #def clicked(self):
        #self.label.setText('New Text that is too big for the button!')
        #self.update()

    #def update(self):
        #self.label.adjustSize()

    def mousePressEvent(self, event):
        self.oldPosition = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint(event.globalPos() - self.oldPosition)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPosition = event.globalPos()


#Initialize Application
app = QApplication(sys.argv)

#Instantiate Window Class
UIWindow = UI()

#Terminate the application upon exit
sys.exit(app.exec())