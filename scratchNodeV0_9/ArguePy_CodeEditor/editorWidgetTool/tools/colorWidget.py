import sys

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class ColorDialogSimple(QColorDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setOptions(self.options() | QColorDialog.ColorDialogOption.DontUseNativeDialog)

        for children in self.findChildren(QWidget):
            className = children.metaObject().className()
            if className not in ("QColorPicker", "QColorLuminancePicker"):
                children.hide()


class colorWidget(QWidget):
    gridLayout: QGridLayout
    colorChanged = pyqtSignal(QColor, str)
    nameList = ["KeywordColor", "functionColor", "builtInColor", "selfColor", "classFunctionColor", "methodColor",
                "braceColor", "stringColor", "numberColor", "commentColor", "comment2Color", "classColor",
                "operatorColor", "braceColor", "identifierColor", "commentLineColor", "commentDocColor" , "commentDocKeywordColor"]

    def __init__(self, editor, parent=None):
        super(colorWidget, self).__init__(parent)
        self.editor = editor
        """
        Imposta il layout principale formato dalla ruota colore e da una griglia di pulsanti.
        Ogni pulsante, corrisponde ai colori del lexer, se cliccato accetta un colore e manda
        il colore così modificato al metodo setLexerColor() di editorCode
        """
        self.mainLayout = QVBoxLayout()
        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(0)
        self.colorWheel = ColorDialogSimple()
        self.colorWheel.currentColorChanged.connect(self.changeColor)
        self.mainLayout.addWidget(self.colorWheel)
        self.mainLayout.addLayout(self.gridLayout)
        self.setLayout(self.mainLayout)
        self.currentBtn = None
        self.createBtnGrid()

    def createBtnGrid(self):
        """
        Crea una lista di pulsanti con lo stile di colore corrispondente
        alla colorList dell'editorCode

        Se il pulsante viene toggle si può cambiargli colore tramite la ruota colore
        ognuno di questi pulsanti è collegato alla variabile QColor corrispondente
        ed emette un segnale che viene intercettato da editorCode per impostare i colori del lexer
        """
        # crea una griglia quadrata di pulsanti
        # se la lunghezza della lista è 16 allora la griglia sarà 4x4
        grid = int(len(self.editor.colorList) ** 0.5)
        row, column = 0, 0
        for i in range(len(self.editor.colorList)):
            btn = QPushButton(self.nameList[i])
            btn.setFont(QFont("Consolas", 8))
            btn.setFixedSize(120, 40)
            btn.setCheckable(True)
            btn.setStyleSheet(f"background-color: {self.editor.colorList[i].name()}")
            btn.clicked.connect(self.setColor)
            self.gridLayout.addWidget(btn, row, column)
            column += 1
            if column == grid:
                row += 1
                column = 0

    def setColor(self):
        """
        Se il pulsante è stato premuto, allora si può cambiare il colore. Si può cambiare colore a un solo
        pulsante alla volta, quindi se un pulsante è stato premuto tutti gli altri vengono disattivati.
        """
        sender = self.sender()
        if sender.isChecked():
            self.currentBtn = sender
            # fa l'uncheck ti tutti gli altri bottoni
            for i in range(self.gridLayout.count()):
                item = self.gridLayout.itemAt(i)
                if item.widget() != sender:
                    item.widget().setChecked(False)

    def changeColor(self):
        if self.currentBtn is None:
            return
        self.currentBtn.setStyleSheet(f"background-color: {self.colorWheel.currentColor().name()}")
        for i in range(len(self.editor.colorList)):
            if self.currentBtn.text() == self.nameList[i]:
                self.editor.colorList[i] = self.colorWheel.currentColor()
                self.colorChanged.emit(self.editor.colorList[i], self.nameList[i])
                break
