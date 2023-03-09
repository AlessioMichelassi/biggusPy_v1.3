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
    frame: QFrame
    grpBox: QGroupBox
    grpBoxLayout: QVBoxLayout
    layout: QHBoxLayout
    width: int = 300
    height: int = 200

    radiusChange = pyqtSignal(str)
    sigmaChange = pyqtSignal(str)
    valueChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowType.Window)
        self.sld1 = sliderBox("radius")
        self.sld1.setSliderRange(0, 100)
        self.sld2 = sliderBox("sigma")
        self.sld2.setSliderRange(0, 100)
        self.initUI()
        self.initConnections()
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

    def initUI(self):
        mainLayout = QVBoxLayout()
        self.frame = QFrame(flags=Qt.WindowFlags())
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setContentsMargins(5, 5, 5, 5)
        self.frame.setFixedSize(self.width, self.height)
        self.frame.setLayout(QVBoxLayout())
        # aggiunge una groupBox
        self.grpBox = QGroupBox("Blur Tool")
        self.grpBox.setFixedSize(self.width-10, self.height-10)
        self.grpBoxLayout = QVBoxLayout()
        self.grpBox.setLayout(self.grpBoxLayout)
        self.grpBoxLayout.addWidget(self.sld1, alignment=Qt.AlignmentFlag.AlignCenter)
        self.grpBoxLayout.addWidget(self.sld2, alignment=Qt.AlignmentFlag.AlignCenter)
        self.frame.layout().addWidget(self.grpBox)
        mainLayout.addWidget(self.frame)
        self.setLayout(mainLayout)

    def initConnections(self):
        self.sld1.valueChanged.connect(self.onRadiusChange)
        self.sld2.valueChanged.connect(self.onSigmaChange)
        self.sld1.valueChanged.connect(self.valueChanged)
        self.sld2.valueChanged.connect(self.valueChanged)

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
        self.combo.addItems(["erode", "erode_Border_reflect", "erode_Border_reflect_101", "erode_Border_replicate", "erode_Border_wrap", "erode_Border_constant", "erode_Border_isolated", "dilate", "dilate_Border_reflect", "dilate_Border_reflect_101", "dilate_Border_replicate", "dilate_Border_wrap", "dilate_Border_constant", "dilate_Border_isolated"])
        self.layout.addWidget(self.combo)
        self.combo.currentIndexChanged.connect(self.onComboChanged)
        self.setStyleSheet(self.style)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(0, 0, 0, 0)

    def onComboChanged(self, index):
        self.toolBox.sld1.setSliderRange(0, 100)
        self.toolBox.sld2.setSliderRange(0, 100)
        self.toolBox.sld1.setValue(5)
        self.toolBox.sld2.setValue(0)

    def showToolBox(self, pos):
        self.toolBox.setGeometry(int(pos.x()), int(pos.y()), 200, 100)
        self.toolBox.show()


class ErodeCvNode(AbstractNodeInterface):
    startValue = ""
    width = 180
    height = 120
    colorTrain = [QColor(255, 234, 242),QColor(255, 91, 110),QColor(142, 255, 242),QColor(218, 255, 251),QColor(110, 255, 91),QColor(170, 61, 73),QColor(52, 19, 23),QColor(142, 255, 242),]
    radius = 7
    sigma = 0
    lastValue = None
    logo = r"Release/biggusFolder/imgs/logos/openCvLogo.png"

    def __init__(self, value=20, inNum=2, outNum=1, parent=None):
        super().__init__(value, inNum, outNum, parent)
        self.setClassName("ErodeCvNode")
        self.setName("ErodeCvNode")
        self.changeSize(self.width, self.height)
        self.AddProxyWidget()

    def calculateOutput(self, plugIndex):
        value = self.inPlugs[0].getValue()
        if value is not None:
            operation = {
                "erode": self.doErode,
                "erode_Border_reflect": self.doErode_reflect,
                "erode_Border_reflect_101": self.doErode_reflect_101,
                "erode_Border_replicate": self.doErode_replicate,
                "erode_Border_wrap": self.doErode_wrap,
                "erode_Border_constant": self.doErode_constant,
                "erode_Border_isolated": self.doErode_isolated,
                "dilate": self.doDilate,
                "dilate_Border_reflect": self.doDilate_reflect,
                "dilate_Border_reflect_101": self.doDilate_reflect_101,
                "dilate_Border_replicate": self.doDilate_replicate,
                "dilate_Border_wrap": self.doDilate_wrap,
                "dilate_Border_constant": self.doDilate_constant,
                "dilate_Border_isolated": self.doDilate_isolated
            }
            self.outPlugs[plugIndex].setValue(operation[self.proxyWidget.combo.currentText()](value))

        else:
            print("no image")
        return self.outPlugs[plugIndex].getValue()

    def redesign(self):
        self.changeSize(self.width, self.height)

    def doErode(self, image):
        return cv2.erode(image, (self.radius, self.radius))

    def doErode_reflect(self, image):
        kernel = np.ones((self.radius, self.radius), np.uint8)
        return cv2.erode(image, kernel, borderType=cv2.BORDER_REFLECT)

    def doErode_reflect_101(self, image):
        return cv2.erode(image, (self.radius, self.radius), borderType=cv2.BORDER_REFLECT_101)

    def doErode_replicate(self, image):
        return cv2.erode(image, (self.radius, self.radius), borderType=cv2.BORDER_REPLICATE)

    def doErode_wrap(self, image):
        return cv2.erode(image, (self.radius, self.radius), borderType=cv2.BORDER_WRAP)

    def doErode_constant(self, image):
        return cv2.erode(image, (self.radius, self.radius), borderType=cv2.BORDER_CONSTANT)

    def doErode_isolated(self, image):
        return cv2.erode(image, (self.radius, self.radius), borderType=cv2.BORDER_ISOLATED)

    def doDilate(self, image):
        return cv2.dilate(image, (self.radius, self.radius))

    def doDilate_reflect(self, image):
        return cv2.dilate(image, (self.radius, self.radius), borderType=cv2.BORDER_REFLECT)

    def doDilate_reflect_101(self, image):
        return cv2.dilate(image, (self.radius, self.radius), borderType=cv2.BORDER_REFLECT_101)

    def doDilate_replicate(self, image):
        return cv2.dilate(image, (self.radius, self.radius), borderType=cv2.BORDER_REPLICATE)

    def doDilate_wrap(self, image):
        return cv2.dilate(image, (self.radius, self.radius), borderType=cv2.BORDER_WRAP)

    def doDilate_constant(self, image):
        return cv2.dilate(image, (self.radius, self.radius), borderType=cv2.BORDER_CONSTANT)

    def doDilate_isolated(self, image):
        return cv2.dilate(image, (self.radius, self.radius), borderType=cv2.BORDER_ISOLATED)

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
        self.proxyWidget.toolBox.valueChanged.connect(self.nodeData.calculate)

    def setDefaultParameters(self):
        self.proxyWidget.combo.setCurrentIndex(0)
        self.proxyWidget.toolBox.sld1.setValue(7)
        self.proxyWidget.toolBox.sld2.setValue(0)

    def onRadiusChange(self, value):
        value = int(value)
        if value % 2 == 0:
            value += 1
        self.radius = value
        self.calculateOutput(0)
        if self.nodeData.outConnections:
            for connection in self.nodeData.outConnections:
                connection.updateValue()

    def onSigmaChange(self, value):
        value = int(value)

        self.sigma = value
        self.calculateOutput(0)
        if self.nodeData.outConnections:
            for connection in self.nodeData.outConnections:
                connection.updateValue()


