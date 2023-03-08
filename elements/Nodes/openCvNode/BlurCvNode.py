import cv2
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import cv2 as cv
import sys
from elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface


class cmbBoxWidget(QWidget):
    style = f"""
        font: 6pt "Segoe UI";
        background-color: rgb(30, 30, 30);
        color: rgb(240, 240, 255);
        """
    returnOperation = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent, Qt.Window)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.combo = QComboBox()
        self.combo.setFixedSize(130, 20)
        self.combo.addItems(["Gaussian", "median", "bilateral", "...", "..."])
        self.layout.addWidget(self.combo)
        self.combo.currentIndexChanged.connect(self.onComboChanged)
        self.setStyleSheet(self.style)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        # fa i bordi del wisget stondati
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

    def onComboChanged(self, index):
        if index == 0:
            self.returnOperation.emit("Gaussian")
        elif index == 1:
            self.returnOperation.emit("median")
        elif index == 2:
            self.returnOperation.emit("bilateral")

    def event(self, QEvent):
        if QEvent.type() == QEvent.MouseButtonDblClick:
            print("double click")
        return super().event(QEvent)


class BlurCvNode(AbstractNodeInterface):
    startValue = ""
    width = 180
    height = 120
    colorTrain = []

    def __init__(self, value=20, inNum=2, outNum=1, parent=None):
        super().__init__(value, inNum, outNum, parent)
        self.setClassName("BlurCvNode")
        self.setName("BlurCvNode")
        self.changeSize(self.width, self.height)
        self.AddProxyWidget()

    def calculateOutput(self, plugIndex):
        value = self.inPlugs[0].getValue()
        if isinstance(value, np.ndarray):
            if self.proxyWidget.combo.currentText() == "Gaussian":
                value = self.doGaussian(value)
            elif self.proxyWidget.combo.currentText() == "median":
                value = self.doMedian(value)
            elif self.proxyWidget.combo.currentText() == "bilateral":
                value = self.doBilateral(value)
            self.outPlugs[plugIndex].setValue(value)
        else:
            print("no image")
        return self.outPlugs[plugIndex].getValue()

    def redesign(self):
        self.changeSize(self.width, self.height)

    def doGaussian(self, image):
        print("gaussian")
        return cv2.GaussianBlur(image, (7, 7), 0)

    def doMedian(self, image):
        return cv2.medianBlur(image, 5)

    def doBilateral(self, image):
        return cv2.bilateralFilter(image, 9, 75, 75)

    def AddProxyWidget(self):
        self.proxyWidget = cmbBoxWidget()
        self.proxyWidget.setFixedSize(self.width - 20, self.height - 50)
        self.nodeGraphic.createProxyWidget(self.proxyWidget)
        self.proxyWidget.setFixedWidth(self.width - 20)
        self.proxyWidget.setFixedHeight(self.height - 50)
        self.proxyWidget.move(int(self.width // 2 - self.proxyWidget.width() // 2),
                              int(self.height // 2 - self.proxyWidget.height() // 2) + 20)
