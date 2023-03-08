import cv2
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import cv2 as cv
import sys
from elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface
from elements.tools.sliderBox import sliderBox


class toolz(QWidget):
    sld1: sliderBox
    sld2: sliderBox

    radiusChange = pyqtSignal(str)
    sigmaChange = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowType.Window)
        self.sld1 = sliderBox("radius")
        self.sld1.setSliderRange(0, 100)
        self.sld2 = sliderBox("sigma")
        self.sld2.setSliderRange(0, 100)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.sld1)
        self.layout.addWidget(self.sld2)
        self.sld1.valueChanged.connect(self.onRadiusChange)
        self.sld2.valueChanged.connect(self.onSigmaChange)

    def onRadiusChange(self, value):
        self.radiusChange.emit(str(value))

    def onSigmaChange(self, value):
        self.sigmaChange.emit(str(value))


class cmbBoxWidget(QWidget):
    style = f"""
        font: 6pt "Segoe UI";
        background-color: rgb(30, 30, 30);
        color: rgb(240, 240, 255);
        """
    radiusChange = pyqtSignal(int)
    sigmaChange = pyqtSignal(int)

    def __init__(self, reference, parent=None):
        super().__init__(parent)
        self.toolBox = toolz()
        self.reference = reference
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

    def onComboChanged(self, index):
        self.toolBox.sld1.setSliderRange(0, 100)
        self.toolBox.sld2.setSliderRange(0, 100)
        if index == 0:
            self.toolBox.sld1.setValue(5)
            self.toolBox.sld2.setValue(0)
        elif index == 1:
            self.toolBox.sld1.setValue(7)
            self.toolBox.sld2.setValue(0)
        elif index == 2:
            self.toolBox.sld1.setValue(7)
            self.toolBox.sld2.setValue(50)

    def showToolBox(self, pos):
        self.toolBox.setGeometry(int(pos.x()), int(pos.y()), 200, 100)
        self.toolBox.show()


class BlurCvNode(AbstractNodeInterface):
    startValue = ""
    width = 180
    height = 120
    colorTrain = []
    radius = 7
    sigma = 0

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
        return cv2.GaussianBlur(image, (self.radius, self.radius), self.sigma)

    def doMedian(self, image):
        return cv2.medianBlur(image, self.radius)

    def doBilateral(self, image):
        return cv2.bilateralFilter(image, self.radius, self.sigma, self.sigma)

    def AddProxyWidget(self):
        self.proxyWidget = cmbBoxWidget(self)
        self.proxyWidget.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.proxyWidget.setFixedSize(self.width - 20, self.height - 50)
        self.nodeGraphic.createProxyWidget(self.proxyWidget)
        self.proxyWidget.setFixedWidth(self.width - 20)
        self.proxyWidget.setFixedHeight(self.height - 50)
        self.proxyWidget.move(int(self.width // 2 - self.proxyWidget.width() // 2),
                              int(self.height // 2 - self.proxyWidget.height() // 2) + 20)
        self.setDefaultParameters()
        self.proxyWidget.toolBox.radiusChange.connect(self.onRadiusChange)
        self.proxyWidget.toolBox.sigmaChange.connect(self.onSigmaChange)

    def setDefaultParameters(self):
        self.proxyWidget.combo.setCurrentIndex(0)
        self.proxyWidget.toolBox.sld1.setValue(7)
        self.proxyWidget.toolBox.sld2.setValue(0)

    def onRadiusChange(self, value):
        value = int(value)
        if value % 2 == 0:
            value += 1
        self.radius = value
        print(f"Debug print from BlurCvNode: radius = {self.radius}")
        self.calculateOutput(0)

    def onSigmaChange(self, value):
        value = int(value)

        self.sigma = value
        self.calculateOutput(0)
