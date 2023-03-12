import json
import pprint

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import configparser

from widgets.Canvas.Canvas import Canvas
from widgets.Canvas.nodeBrowser import NodeBrowser
from widgets.Canvas.terminal import Terminal

from widgets.Menu.biggusMenu import BiggusMenu


class biggusPy(QMainWindow):

    canvas: Canvas
    nodeBrowser: NodeBrowser
    terminal: Terminal
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
        self.initUI()

    def initUI(self):
        lay1 = self.initCanvas()
        lay2 = self.initNodeBrowser()
        # il node browser non essere più grande di 1/3 del canvas
        self.initSize()
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(lay1)
        mainLayout.addLayout(lay2)
        mainWidget = QWidget()
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)
        menu = BiggusMenu(self)
        self.setMenuBar(menu)
        self.createStatusBar()

    def initCanvas(self):
        self.canvas = Canvas()
        layout = QHBoxLayout()
        layout.addWidget(self.canvas)
        return layout

    def initNodeBrowser(self):
        self.nodeBrowser = NodeBrowser()
        self.terminal = Terminal()
        layout = QHBoxLayout()
        layout.addWidget(self.nodeBrowser)
        layout.addWidget(self.terminal)
        return layout

    def initSize(self):
        self.nodeBrowser.setFixedHeight(int(self.canvas.rect().height() / 3))

    def initConnections(self):
        self.canvas.graphicView.scenePosChanged.connect(self.onScenePosChanged)
        self.terminal.terminalSignal.connect(self.onTerminalInput)

    def restartCanvas(self):
        self.canvas.cleanTheScene()
        self.canvas = Canvas()
        self.setCentralWidget(self.canvas)

    def createStatusBar(self):
        self.statusBar().showMessage("")
        self.statusMousePosition = QLabel("")
        self.statusBar().addPermanentWidget(self.statusMousePosition)

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

    # ------------------ SHOW ON CANVAS ------------------

    def printOnStatusBar(self, text):
        self.statusBar().showMessage(text, 2000)

    def onTerminalInput(self, command):
        self.printOnStatusBar(command)