import json
import pprint

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import configparser

from widgets.Canvas.Canvas import Canvas

from widgets.Menu.biggusMenu import BiggusMenu


class biggusPy(QMainWindow):
    statusMousePosition: QLabel
    path = "saveDir"
    fileName = "untitled"
    recentFilesMenu: BiggusMenu
    recentFiles = []
    pythonFolderPath = r"elements/Nodes/PythonNodes"

    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowFlags())
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("BiggusPy(a great Caesar's friend) V0.1.3")
        self.setWindowIcon(QIcon('elements/imgs/BiggusIcon.ico'))
        self.canvas = Canvas()
        self.setCentralWidget(self.canvas)
        menu = BiggusMenu(self)
        self.setMenuBar(menu)
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

    def saveFile(self, filename, fileData):
        with open(filename, "w+") as file:
            file.write(fileData)

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
