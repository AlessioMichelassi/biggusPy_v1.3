import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Terminal(QPlainTextEdit):
    backgroundColor: QColor = QColor(30, 31, 34)
    textColor: QColor = QColor(167, 183, 198)
    lineNumberColor: QColor = QColor(200, 200, 240, 255)
    lineNumberBackgroundColor: QColor = backgroundColor.darker(110)
    indentationLineColor: QColor = QColor(255, 100, 100, 255)
    systemFont: QFont = QFont("Lohit Gujarati", 8)
    terminalSignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.updateSystemColors()
        self.initFont()
        self.prompt = ">>>"
        self.insertPlainText(f"{self.prompt} ")

    def updateSystemColors(self):
        # dovrebbe cambiare solo lo sfondo non tutto il colore del widget
        style = f"QPlainTextEdit {{background-color: {self.backgroundColor.name()}; color: {self.textColor.name()};}}"
        self.setStyleSheet(style)

    def initFont(self):
        self.systemFont.setStyleHint(QFont.TypeWriter)
        self.systemFont.setPointSize(8)
        self.setFont(self.systemFont)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return:
            command = self.document().lastBlock().text().strip()
            self.handleCommand(command)
            self.insertPlainText(f"\n{self.prompt} ")
            return
        super().keyPressEvent(event)

    def handleCommand(self, command):
        # Qui inserisci la logica per gestire i comandi inseriti nel terminale
        pass
