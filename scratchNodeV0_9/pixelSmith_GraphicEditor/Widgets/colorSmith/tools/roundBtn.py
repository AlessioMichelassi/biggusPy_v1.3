from random import randint

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class RoundButton(QPushButton):
    """
        Crea un pulsante di forma rotonda associato a una label. Il pulsante è di tipo checkable
        ed è pensato per essere utilizzato come selezionatore di colore.
        Il pulsante è di default disabilitato.
    """
    name = "default"
    size = 40
    btnColorChanged = pyqtSignal(QColor, name="btnColorChanged")

    colorFill: QColor = QColor(40, 40, 40)
    colorBorder: QColor = QColor(0, 0, 0)
    colorBorderSelected: QColor = QColor(90, 90, 90)
    canAcceptColor = True
    style = """ """

    def __init__(self, colorSelector, name, parent=None):
        super(RoundButton, self).__init__(parent)
        self.name = name
        self.colorSelector = colorSelector
        self.initUI()
        self.initStyle()
        self.initConnection()
        self.setAcceptDrops(True)

    def initUI(self):
        self.setCheckable(True)
        self.setFixedSize(self.size, self.size)
        self.setContentsMargins(0, 0, 0, 0)

    def initStyle(self):
        self.style = f"""
            QPushButton {{
                border-radius: {self.size // 2}px;
                border: 1px solid {self.colorBorder.name()};
                background-color: {self.colorFill.name()};
            }}
            QPushButton:checked {{
                border-radius: {self.size // 2}px;
                border: 2px solid {self.colorBorderSelected.name()};
                background-color: {self.colorFill.name()};
            }}
        """
        self.setStyleSheet(self.style)

    def initConnection(self):
        self.toggled.connect(self.onBtnToggled)

    def onBtnToggled(self, checked):
        self.canAcceptColor = bool(checked)

    def setColor(self, color: QColor):
        if self.canAcceptColor:
            self.colorFill = color
            self.initStyle()

    def getColor(self):
        return self.colorFill

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        parent = self.parent()
        if parent is not None:
            parent.mousePressEvent(event)
            parent.mouseMoveEvent(event)
            parent.mouseReleaseEvent(event)