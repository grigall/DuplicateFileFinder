#UI Imports
from PyQt5.QtWidgets import QWidget, QFrame, QGridLayout, QApplication, QPushButton, QLabel, QFileDialog
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
import sys
import os

class UI(QWidget):
    def __init__(self):
        super(UI, self).__init__()
        #Export Variables
        self.exportVariables = ''

        #Path variables
        self.DEFAULT_SAVE_PATH = os.path.expanduser('~\Documents')
        self.PATH_MAIN = 'PATH_MAIN'
        self.PATH_COMP = 'PATH_COMP'
        
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

        #Add Path Labels
        self.mainPathLabel = QLabel(self)
        self.mainPathLabel.setObjectName('MPLabel')

        self.compPathLabel = QLabel(self)
        self.compPathLabel.setObjectName('CPLabel')


        #Add Buttons
        button1 = self.addButton('Main Directory','Button1', None, lambda: self.selectDirectory(self.PATH_MAIN, self.mainPathLabel, False))
        button2 = self.addButton('Comparison Directory','Button2', None, lambda: self.selectDirectory(self.PATH_COMP, self.compPathLabel, False))
        exitButton = self.addButton('\u2715', 'ExitButton', 'Exit Application', lambda: sys.exit(app.exec()))
        self.exportButton = self.addButton('Analyse Data', 'ExportButton', 'Export List to File', lambda: self.analyseData(self.PATH_MAIN, self.PATH_COMP))

        #Grid Positioning
        grid.addWidget(menuLabel, 0, 1, 1, 12)
        grid.addWidget(mainLabel, 3, 1, 9, 6)
        grid.addWidget(compLabel, 3, 7, 9, 6)
        grid.addWidget(self.mainPathLabel, 2, 1, 1, 6)
        grid.addWidget(self.compPathLabel, 2, 7, 1, 6)
        grid.addWidget(button1, 1, 1, 1, 6)
        grid.addWidget(button2, 1, 7, 1, 6)
        grid.addWidget(exitButton, 0, 12)
        grid.addWidget(self.exportButton, 12, 1, 1, 12)

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

    def selectDirectory(self, targetPath, targetLabel, savePath):
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory", self.DEFAULT_SAVE_PATH))
        if directory:
            if targetPath == 'PATH_COMP':
                self.PATH_COMP = directory #Sets global variable to selected folder
            elif targetPath == 'PATH_MAIN':
                self.PATH_MAIN = directory #Sets global variable to selected folder
            else:
                pass

        if targetLabel:
            #Update path label on GUI
            targetLabel.setText(directory)

        if savePath:
            self.saveFile(directory, self.exportVariables)
            #print('Save Directory: ', directory) #DEBUG

    #Allows you to move the window around the screen with the mouse
    def mousePressEvent(self, event):
        self.oldPosition = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint(event.globalPos() - self.oldPosition)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPosition = event.globalPos()

    #Implements analysis logic
    def analyseData(self, mainPath, compPath):
        import logic
        #Get data for right and left tables
        data = logic.get_file_data(mainPath)
        data_rt = logic.get_file_data(compPath)
        #Find duplicates within right and left tables
        mainDuplicates = logic.find_duplicates(data)
        compDuplicates = logic.find_duplicates(data_rt)

        #Find unique and duplicate values
        compUnique, bothDuplicates = logic.unique_in_rt_table(data, data_rt)

        self.exportVariables = [compUnique, bothDuplicates, mainDuplicates, compDuplicates]
        
        #Set Export Button Text and Functionality
        self.exportButton.setText('Export Files')
        self.exportButton.clicked.connect(lambda: self.selectDirectory(self.DEFAULT_SAVE_PATH, None, True))

    def saveFile(self, targetPath, fileList):
        filenames = ['Unique_from_Comparison_Folder.csv', 'Duplicates_from_Both_Folders.csv', 'Duplicates_from_Main_Folder.csv', 'Duplicates_from_Comparison_Folder.csv']
        for idx, file in enumerate(fileList):
            newPath = os.path.join(targetPath, filenames[idx])
            file.to_csv(newPath, sep='\t', index=False, encoding='utf-8')
        
        #Reset Export Button Info
        self.exportButton.setText('Analyse Data')
        self.exportButton.clicked.connect(lambda: self.analyseData(self.PATH_MAIN, self.PATH_COMP))

        #Reset Paths
        self.mainPathLabel.setText('')
        self.compPathLabel.setText('')

        print('Files Exported!') #DEBUG



#Initialize Application
app = QApplication(sys.argv)

#Instantiate Window Class
UIWindow = UI()

#Terminate the application upon exit
sys.exit(app.exec())
