from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class MenuBar(QMenuBar):
    fileMenu: QMenu
    editMenu: QMenu
    viewMenu: QMenu
    SettingsMenu: QMenu
    helpMenu: QMenu
    mainWindows: 'mainGraphicEditorWindows'
    recentFiles: list

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mainWindows = self.parent()
        self.createMenu()
        self.createFileMenu()
        self.createEditMenu()
        self.createViewMenu()
        self.createSettingsMenu()
        self.createHelpMenu()

    # ################################################
    #
    #       create menu
    #
    #

    def createMenu(self):
        self.fileMenu = self.addMenu("&File")
        self.editMenu = self.addMenu("&Edit")
        self.viewMenu = self.addMenu("&View")
        self.SettingsMenu = self.addMenu("&Settings")
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
        _openRecent = QAction("Open Recent", self)
        _openRecent.setShortcut("Ctrl+Shift+O")
        _openRecent.setStatusTip("Open a recent file")
        _openRecent.triggered.connect(self.openRecentFile)
        _save = QAction("Save", self)
        _save.setShortcut("Ctrl+S")
        _save.setStatusTip("Save the file")
        _save.triggered.connect(self.saveFile)
        _saveAs = QAction("Save As", self)
        _saveAs.setShortcut("Ctrl+Shift+S")
        _saveAs.setStatusTip("Save the file as")
        _saveAs.triggered.connect(self.saveFileAs)
        _exit = QAction("Exit", self)
        _exit.setShortcut("Ctrl+Q")
        _exit.setStatusTip("Exit the application")
        _exit.triggered.connect(self.exitApplication)
        self.fileMenu.addAction(_new)
        self.fileMenu.addAction(_open)
        self.fileMenu.addAction(_openRecent)
        self.fileMenu.addAction(_save)
        self.fileMenu.addAction(_saveAs)
        self.fileMenu.addAction(_exit)

    def createEditMenu(self):
        pass

    def createViewMenu(self):
        pass

    def createSettingsMenu(self):
        _loadSettings = QAction("Load Settings", self)
        _loadSettings.setStatusTip("Load settings")
        _loadSettings.triggered.connect(self.loadSettings)
        _saveSettings = QAction("Save Settings", self)
        _saveSettings.setStatusTip("Save settings")
        _saveSettings.triggered.connect(self.saveSettings)
        self.SettingsMenu.addAction(_loadSettings)
        self.SettingsMenu.addAction(_saveSettings)

    def createHelpMenu(self):
        _help = QAction("Help", self)
        _help.setStatusTip("Help")
        _help.triggered.connect(self.help)
        _about = QAction("About", self)
        _about.setStatusTip("About")
        _about.triggered.connect(self.about)
        _aboutQt = QAction("About Qt", self)
        _aboutQt.setStatusTip("About Qt")
        _aboutQt.triggered.connect(self.aboutQt)
        self.helpMenu.addAction(_help)
        self.helpMenu.addAction(_about)
        self.helpMenu.addAction(_aboutQt)

    # ################################################
    #
    #       file menu
    #
    #

    def newFile(self):
        self.mainWindows.newNode()

    def openFile(self):
        self.mainWindows.openFile()

    def openRecentFile(self):
        """
            ITA: Apre la lista dei file recenti
            ENG: Open the recent files list
        :return:
        """
        with open("recentFiles.ini", "r") as file:
            self.recentFiles = file.readlines()

    def saveRecentFiles(self):
        with open("recentFiles.ini", "w") as file:
            for _fileName in self.recentFiles:
                file.write(_fileName)

    def saveFile(self):
        self.mainWindows.saveFile()

    def saveFileAs(self):
        self.mainWindows.saveFileAs()

    def exitApplication(self):
        self.saveSettings()
        self.saveRecentFiles()
        self.mainWindows.close()

    # ################################################
    #
    #       edit menu
    #
    #

    def undo(self):
        pass

    def redo(self):
        pass

    def cut(self):
        pass

    def copy(self):
        pass

    def paste(self):
        pass

    def delete(self):
        pass

    def selectAll(self):
        pass

    def find(self):
        pass

    def replace(self):
        pass

    # ################################################
    #
    #       view menu
    #
    #

    def zoomIn(self):
        pass

    def zoomOut(self):
        pass

    def zoomReset(self):
        pass

    def zoomFit(self):
        pass

    def zoomFitWidth(self):
        pass

    def zoomFitHeight(self):
        pass

    def zoomFitPage(self):
        pass

    def zoomFitPageWidth(self):
        pass

    def zoomFitPageHeight(self):
        pass

    def zoomFitSelection(self):
        pass

    def zoomFitSelectionWidth(self):
        pass

    def zoomFitSelectionHeight(self):
        pass

    def zoomFitSelectionPage(self):
        pass

    def zoomFitSelectionPageWidth(self):
        pass

    def zoomFitSelectionPageHeight(self):
        pass

    def zoomFitWindow(self):
        pass

    # ################################################
    #
    #       settings menu
    #
    #

    def settings(self):
        pass

    def preferences(self):
        pass

    def loadSettings(self):
        self.mainWindows.loadSettings()

    def saveSettings(self):
        self.mainWindows.saveSettings()

    # ################################################
    #
    #       help menu
    #
    #

    def help(self):
        pass

    def about(self):
        aboutDialog = QDialog(self)
        aboutDialog.setWindowTitle("About scratchNodeV0_9")
        aboutDialog.setFixedSize(600, 300)

        titleLabel = QLabel("scratchNodeV0_9")
        titleLabel.setStyleSheet("font-size: 24px; font-weight: bold;")
        versionLabel = QLabel("Version 0.8")
        versionLabel.setStyleSheet("font-size: 16px; font-weight: bold;")
        authorLabel = QLabel("Author: Alessio Michelassi (2023)")
        authorLabel.setStyleSheet("font-size: 12px; font-weight: bold;")
        descriptionTxt = QTextEdit()
        descriptionTxt.setStyleSheet("font-size: 10px;")
        with open("pixelSmith_GraphicEditor/CommonMenu/AboutThisSoftware", "r") as file:
            aboutTxt = file.read()
        descriptionTxt.setText(aboutTxt)
        descriptionTxt.setReadOnly(True)
        layout = QVBoxLayout()
        layout.addWidget(titleLabel)
        layout.addWidget(versionLabel)
        layout.addWidget(descriptionTxt)
        aboutDialog.setLayout(layout)

        # Visualizzazione della finestra di dialogo
        aboutDialog.exec_()

    def aboutQt(self):
        """
            ITA: Mostra la finestra di About Qt
            ENG: Show the About Qt window
        :return:
        """
        QMessageBox.aboutQt(self.mainWindows, "About Qt")
