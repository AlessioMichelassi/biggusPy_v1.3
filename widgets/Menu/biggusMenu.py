import configparser
import json
import pprint
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from scratchNodeV0_9.scratchNode import scratchNodeV0_9
from widgets.Menu.openCvNodeMenu import OpenCvNodeMenu
from widgets.Menu.pythonNodeMenu import PythonNodeMenu
from widgets.Menu.pyQt5NodeMenu import PyQt5NodeMenu


class BiggusMenu(QMenuBar):
    # Menu Variables
    fileMenu: QMenu
    editMenu: QMenu
    nodeMenu: QMenu
    viewMenu: QMenu
    helpMenu: QMenu
    recentFilesMenu: QMenu

    pythonNodeMenu: QMenu
    openCvNodeMenu: QMenu
    pyQt5NodeMenu: QMenu

    # software link variables
    biggusPy: 'mainGraphicEditorWindows'
    canvas: 'canvas'
    graphicView: 'graphicView'
    graphicScene: 'graphicScene'
    ScratchONode: 'ScratchONode'

    # systemVariables
    recentFiles: list
    systemPath: str
    recentFiles = []

    fileName = "untitled"

    def __init__(self, biggusPy, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.biggusPy = biggusPy
        self.createMenu()
        self.createFileMenu()
        self.createEditMenu()
        self.createNodeMenu()
        self.createViewMenu()
        self.createHelpMenu()

    def createLink(self):
        self.canvas = self.biggusPy.canvas
        self.graphicView = self.biggusPy.graphicView
        self.graphicScene = self.biggusPy.graphicScene
        self.ScratchONode = self.biggusPy.ScratchONode

    def createMenu(self):
        self.fileMenu = self.addMenu("&File")
        self.editMenu = self.addMenu("&Edit")
        self.nodeMenu = self.addMenu("&Node")
        self.viewMenu = self.addMenu("&View")
        self.helpMenu = self.addMenu("&Help")

    def createFileMenu(self):
        """
        create the file menu with New, open, openRecent, save, saveAs, exit
        :return:
        """
        _new = QAction("New", self)
        _new.setShortcut("Ctrl+N")
        _new.setStatusTip("Create a new file")
        _new.triggered.connect(self.newFile)
        _open = QAction("Open", self)
        _open.setShortcut("Ctrl+O")
        _open.setStatusTip("Open a file")
        _open.triggered.connect(self.openFile)

        self.recentFilesMenu = QMenu('Recent Files', self)
        self.recentFiles = self.loadRecentFiles()
        self.recentFilesMenu.triggered.connect(self.openRecentFile)
        _save = QAction("Save", self)
        _save.setShortcut("Ctrl+S")
        _save.setStatusTip("Save the file")
        _save.triggered.connect(self.saveFile)
        _saveAs = QAction("Save As", self)
        _saveAs.setShortcut("Ctrl+Shift+S")
        _saveAs.setStatusTip("Save the file as")
        _saveAs.triggered.connect(self.saveAsFile)
        _exit = QAction("Exit", self)
        _exit.setShortcut("Ctrl+Q")
        _exit.setStatusTip("Exit the application")

        _exit.triggered.connect(self.exitApp)

        self.fileMenu.addAction(_new)
        self.fileMenu.addAction(_open)
        self.fileMenu.addMenu(self.recentFilesMenu)
        self.updateRecentFileMenu()
        self.fileMenu.addAction(_save)
        self.fileMenu.addAction(_saveAs)
        self.fileMenu.addAction(_exit)

    def createEditMenu(self):
        """
        create the edit menu with undo, redo, copy, paste, delete
        :return:
        """
        _undo = QAction("Undo", self)
        _undo.setShortcut("Ctrl+Z")
        _undo.setStatusTip("Undo the last action")
        _undo.triggered.connect(self.undo)
        _redo = QAction("Redo", self)
        _redo.setShortcut("Ctrl+Shift+Z")
        _redo.setStatusTip("Redo the last action")
        _redo.triggered.connect(self.redo)
        _copy = QAction("Copy", self)
        _copy.setShortcut("Ctrl+C")
        _copy.setStatusTip("Copy the selected item")
        _copy.triggered.connect(self.copy)
        _paste = QAction("Paste", self)
        _paste.setShortcut("Ctrl+V")
        _paste.setStatusTip("Paste the copied item")
        _paste.triggered.connect(self.paste)
        _delete = QAction("Delete", self)
        _delete.setShortcut("Del")
        _delete.setStatusTip("Delete the selected item")
        _delete.triggered.connect(self.delete)
        self.editMenu.addAction(_undo)
        self.editMenu.addAction(_redo)
        self.editMenu.addAction(_copy)
        self.editMenu.addAction(_paste)
        self.editMenu.addAction(_delete)

    def createNodeMenu(self):
        """
        create the node menu with addNode, removeNode, renameNode
        :return:
        """
        self.pythonNodeMenu = PythonNodeMenu(self, self.biggusPy)

        self.pyQt5NodeMenu = PyQt5NodeMenu(self, self.biggusPy)

        self.openCvNodeMenu = OpenCvNodeMenu(self, self.biggusPy)

        self.nodeMenu.addMenu(self.pythonNodeMenu)
        self.nodeMenu.addMenu(self.pyQt5NodeMenu)
        self.nodeMenu.addMenu(self.openCvNodeMenu)
        self.nodeMenu.addSeparator()
        action1 = self.nodeMenu.addAction("refresh node list")
        action1.triggered.connect(self.refreshNodeList)
        self.nodeMenu.addAction(action1)

    def createViewMenu(self):
        """
        create the view menu with zoomIn, zoomOut, zoomReset
        :return:
        """
        _zoomIn = QAction("Zoom In", self)
        _zoomIn.setShortcut("Ctrl+Shift+Up")
        _zoomIn.setStatusTip("Zoom in")
        _zoomIn.triggered.connect(self.zoomIn)
        _zoomOut = QAction("Zoom Out", self)
        _zoomOut.setShortcut("Ctrl+Shift+Down")
        _zoomOut.setStatusTip("Zoom out")
        _zoomOut.triggered.connect(self.zoomOut)
        _zoomReset = QAction("Zoom Reset", self)
        _zoomReset.setShortcut("Ctrl+Shift+Left")
        _zoomReset.setStatusTip("Zoom reset")
        _zoomReset.triggered.connect(self.zoomReset)

        _settings = QAction("Settings", self)
        _settings.setShortcut("Ctrl+Shift+Right")
        _settings.setStatusTip("Settings")
        _settings.triggered.connect(self.settings)

        _scratchONode = QAction("Scratch O Node", self)
        _scratchONode.setStatusTip("open the Scratch O Node Editor")
        _scratchONode.triggered.connect(self.openScratchONode)
        self.viewMenu.addAction(_zoomIn)
        self.viewMenu.addAction(_zoomOut)
        self.viewMenu.addAction(_zoomReset)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(_settings)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(_scratchONode)

    def createHelpMenu(self):
        """
        create the help menu with about
        :return:
        """
        _about = self.doAboutMenu(
            "About", "Ctrl+Shift+H", "About the application"
        )
        _about.triggered.connect(self.about)
        self.helpMenu.addAction(_about)
        _aboutQt = self.doAboutMenu(
            "About Qt", "Ctrl+Shift+Q", "About Qt"
        )

    def doAboutMenu(self, arg0, arg1, arg2):
        result = QAction(arg0, self)
        result.setShortcut(arg1)
        result.setStatusTip(arg2)
        return result

    def newFile(self):
        self.biggusPy.restartCanvas()
        self.biggusPy.printOnStatusBar("new")
        self.fileName = "Untitled"

    def openFile(self):
        self.newFile()
        openDialog = QFileDialog(self, "Open a file")
        if openDialog.exec() != QDialog.DialogCode.Accepted:
            return
        openDialog.setFileMode(QFileDialog.FileMode.AnyFile)
        file = openDialog.selectedFiles()[0]
        with open(file, "r") as f:
            file = f.read()
        self.biggusPy.canvas.deserialize(file)
        fileName = openDialog.selectedFiles()[0].split("/")[-1].split(".")[0]
        print(fileName)
        self.biggusPy.printOnStatusBar(f"File opened {self.fileName}")
        self.saveRecentFiles([openDialog.selectedFiles()[0]])
        self.updateRecentFileMenu()

    def openRecentFile(self, action):
        # sourcery skip: use-named-expression
        filename = action.text()  # ottiene il nome del file dall'action
        with open(filename, "r") as f:
            file = f.read()
        self.biggusPy.canvas.deserialize(file)
        self.fileName = filename
        self.biggusPy.printOnStatusBar(f"File opened {self.fileName}")
        self.saveRecentFiles([filename])
        self.updateRecentFileMenu()

    def saveFile(self):
        fileData = self.biggusPy.canvas.serialize()
        if self.fileName == "untitled":
            self.saveAsFile()
        else:
            with open(self.fileName, "w") as f:
                f.write(fileData)
            self.biggusPy.printOnStatusBar(f"File saved as {self.fileName}")

    def saveAsFile(self):
        dialog = QFileDialog.getSaveFileName(self, "Save as", self.biggusPy.path, "Json (*.json)")
        if not dialog[0]:
            return
        filename = dialog[0]
        file = QFile(filename)
        if not file.open(QFile.OpenModeFlag.WriteOnly | QFile.OpenModeFlag.Text):
            reason = file.errorString()
            QMessageBox.warning(self, "Dock Widgets",
                                f"Cannot write file {filename}:\n{reason}.")
            return
        with open(filename, "w") as f:
            f.write(self.biggusPy.canvas.serialize())
        self.biggusPy.printOnStatusBar(f"File saved as {self.fileName}")
        self.saveRecentFiles([filename])
        self.updateRecentFileMenu()

    def exitApp(self):
        sys.exit()

    def undo(self):
        print("undo")

    def redo(self):
        print("redo")

    def copy(self):
        self.biggusPy.canvas.graphicView.copyNode()

    def paste(self):
        self.biggusPy.canvas.pasteNode()

    def delete(self):
        self.biggusPy.canvas.graphicView.deleteSelectedItems()

    def refreshNodeList(self):
        self.pythonNodeMenu.updateNodeMenu()
        self.pyQt5NodeMenu.updateNodeMenu()
        self.openCvNodeMenu.updateNodeMenu()


    def addNode(self):
        print("add node")

    def removeNode(self):
        print("remove node")

    def renameNode(self):
        print("rename node")

    def zoomIn(self):
        print("zoom in")

    def zoomOut(self):
        print("zoom out")

    def zoomReset(self):
        print("zoom reset")

    def about(self):
        print("about")

    def aboutQt(self):
        print("about qt")

    def settings(self):
        print("settings")

    def openScratchONode(self):
        scratchNode = scratchNodeV0_9(self.biggusPy.canvas)
        scratchNode.filePath = "Release/biggusFolder/biggusCode/defaultNode.py"
        scratchNode.loadUntitledNode(scratchNode.filePath)
        scratchNode.show()

    # ------------------ recent files ------------------

    @staticmethod
    def saveRecentFiles(recentFiles):
        config = configparser.ConfigParser()
        config['recentFiles'] = {'files': ','.join(recentFiles)}
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    @staticmethod
    def loadRecentFiles():
        """
        get the recent files
        :return:
        """
        config = configparser.ConfigParser()
        config.read('config.ini')
        recentFiles = config['recentFiles']['files'].split(',')
        return [] if recentFiles == [''] else recentFiles

    def clearRecentFiles(self):
        """
        clear the recent files
        :return:
        """
        self.saveRecentFiles([])
        self.updateRecentFileMenu()

    def updateRecentFileMenu(self):
        """
        update the recent file menu
        :return:
        """
        self.recentFilesMenu.clear()
        recentFiles = self.loadRecentFiles()
        if len(recentFiles) == 0:
            self.recentFilesMenu.addAction("No recent files")
        else:
            for file in recentFiles:
                self.recentFilesMenu.addAction(file)
        self.recentFilesMenu.addSeparator()
        self.recentFilesMenu.addAction("Clear recent files").triggered.connect(self.clearRecentFiles)
