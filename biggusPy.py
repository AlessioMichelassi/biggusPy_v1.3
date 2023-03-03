import json
import pprint

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


import configparser

from widgets.Canvas.Canvas import Canvas


class biggusPy(QMainWindow):
    statusMousePosition: QLabel
    path = "saveDir"
    recentFilesMenu: QMenu
    recentFiles = []

    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowFlags())
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("BiggusPy(a great Caesar's friend) V0.1.2")
        self.setWindowIcon(QIcon('elements/imgs/BiggusIcon.ico'))
        self.canvas = Canvas()
        self.setCentralWidget(self.canvas)
        self.initMenu()
        self.createStatusBar()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.saveRecentFiles(self.recentFiles)

    def initCanvas(self):
        self.canvas = Canvas()
        self.setCentralWidget(self.canvas)

    def restartCanvas(self):
        self.canvas.cleanTheScene()
        self.canvas = Canvas()
        self.setCentralWidget(self.canvas)

    def createStatusBar(self):
        self.statusBar().showMessage("")
        self.statusMousePosition = QLabel("")
        self.statusBar().addPermanentWidget(self.statusMousePosition)
        self.canvas.graphicView.scenePosChanged.connect(self.onScenePosChanged)

    def onScenePosChanged(self, x, y):
        self.statusMousePosition.setText(f"Scene Pos: {x}:{y}")

    def initMenu(self):
        # Crea il menù
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        editMenu = menubar.addMenu('Edit')
        helpMenu = menubar.addMenu('Help')

        # MENU FILE
        newAction = QAction('new', self)
        newAction.setShortcut('Ctrl+N')
        openAction = QAction('open', self)
        openAction.setShortcut('Ctrl+O')

        self.recentFilesMenu = QMenu('Recent Files', self)
        self.recentFiles = self.loadRecentFiles()

        saveAction = QAction('save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAsAction = QAction('saveAs', self)
        saveAsAction.setShortcut('Ctrl+Shift+S')
        exitAction = QAction('Quit', self)
        exitAction.setShortcut('Ctrl+Q')

        newAction.triggered.connect(self.onNew)
        openAction.triggered.connect(self.onOpen)
        saveAction.triggered.connect(self.onSave)
        saveAsAction.triggered.connect(self.onSaveAs)
        exitAction.triggered.connect(qApp.quit)

        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)

        fileMenu.addAction(self.recentFilesMenu.menuAction())
        self.updateRecentFileMenu()
        fileMenu.addAction(saveAction)
        fileMenu.addAction(saveAsAction)
        fileMenu.addAction(exitAction)

        # MENU EDIT
        graphicEditorAction = QAction('Graphic Editor', self)
        graphicEditorAction.triggered.connect(self.onGraphicEditor)
        editMenu.addAction(graphicEditorAction)

        # MENU HELP
        aboutAction = QAction('About', self)
        aboutQtAction = QAction('About Qt', self)

        aboutAction.triggered.connect(self.onAbout)
        aboutQtAction.triggered.connect(QApplication.instance().aboutQt)

        helpMenu.addAction(aboutAction)
        helpMenu.addAction(aboutQtAction)

    def onNew(self):
        self.restartCanvas()
        print(f"this is a print debug from canvas: {self.canvas}")

    def openFile(self, filePath):
        with open(filePath, "r") as f:
            file = f.read()
        self.canvas.deserialize(file)
        self.canvas.fileName = filePath.split("/")[-1].split(".")[0]
        self.statusBar().showMessage(f"{self.canvas.fileName}", 2000)
        self.saveRecentFiles([filePath])
        self.updateRecentFileMenu()

    def onOpen(self):
        self.onNew()
        openDialog = QFileDialog(self, "Open a file")
        if openDialog.exec() != QDialog.DialogCode.Accepted:
            return
        openDialog.setFileMode(QFileDialog.FileMode.AnyFile)
        file = openDialog.selectedFiles()[0]
        with open(file, "r") as f:
            file = f.read()
        self.canvas.deserialize(file)
        self.canvas.fileName = openDialog.selectedFiles()[0].split("/")[-1].split(".")[0]
        self.statusBar().showMessage(f"{self.canvas.fileName}", 2000)
        self.saveRecentFiles([openDialog.selectedFiles()[0]])
        self.updateRecentFileMenu()

    def onSave(self, fileName=None):
        fileData = self.canvas.serialize()
        if fileName is None:
            file = f"{self.path}/{self.canvas.fileName}.json"
        else:
            file = fileName
            self.canvas.fileName = file.split("/")[-1].split(".")[0]
            self.statusBar().showMessage(f"File saved as {self.canvas.fileName}", 2000)
        with open(file, "w+") as file:
            file.write(fileData)

    def onSaveAs(self):
        dialog = QFileDialog.getSaveFileName(self, "Save as", self.path, "Json (*.json)")

        if not dialog[0]:
            return
        filename = dialog[0]
        file = QFile(filename)
        if not file.open(QFile.OpenModeFlag.WriteOnly | QFile.OpenModeFlag.Text):
            reason = file.errorString()
            QMessageBox.warning(self, "Dock Widgets",
                                f"Cannot write file {filename}:\n{reason}.")
            return
        self.onSave(filename)

    def onAbout(self):
        pass

    @staticmethod
    def saveRecentFiles(recentFiles):
        config = configparser.ConfigParser()
        config['recentFiles'] = {'files': ','.join(recentFiles)}
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    @staticmethod
    def loadRecentFiles():
        config = configparser.ConfigParser()
        config.read('config.ini')
        if 'recentFiles' in config:
            recentFiles = config['recentFiles']['files'].split(',')
            return recentFiles
        else:
            return []

    def updateRecentFileMenu(self):
        """
        Update the recent file menu
        :return: nothing
        """
        self.recentFilesMenu.clear()

        for filePath in self.recentFiles:
            action = QAction(filePath, self)
            action.triggered.connect(lambda: self.openFile(filePath))
            self.recentFilesMenu.addAction(action)

    def readDataJason(self, file):
        canvas = json.loads(file)
        print(f"canvasName: {canvas['name']}")
        print(f"width: {canvas['sceneWidth']}")
        print(f"height: {canvas['sceneHeight']}")
        print(f"Nodes:\n")
        nodes = canvas['Nodes']
        for node in nodes:
            ppj = pprint.pformat(node).replace("'", '')
            print(ppj)

    def onGraphicEditor(self):
        pass

    # ################################################
    #
    #               KEYBOARD EVENTS
    #

    def event(self, event):
        # per intercettare il tasto tab c'è bisogno che venga controllato
        # prima di ogni evento
        if event.type() == QEvent.Type.KeyPress:
            if not self.canvas.graphicView.isTabWindowsOpen:
                if event.key() == Qt.Key.Key_Tab:
                    self.canvas.graphicView.openTabWindow()
                    return True
        return super().event(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        self.checkKeyFor(event)
        super().keyPressEvent(event)

    def checkKeyFor(self, event):
        if event.key() == Qt.Key.Key_Delete:
            self.canvas.graphicView.deleteSelectedItems()
        elif event.key() == Qt.Key.Key_D:
            self.canvas.graphicView.disableNode()
        elif event.key() == Qt.Key.Key_C:
            if event.modifiers() and Qt.KeyboardModifier.ControlModifier:
                self.canvas.graphicView.copyNode()
        elif event.key() == Qt.Key.Key_V:
            if event.modifiers() and Qt.KeyboardModifier.ControlModifier:
                self.canvas.pasteNode()