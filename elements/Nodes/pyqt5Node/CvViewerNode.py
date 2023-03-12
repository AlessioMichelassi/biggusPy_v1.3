import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface
import cv2

class ImageViewerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._image = None

    def setImage(self, image):
        self._image = image
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        if self._image is not None:
            painter.drawImage(self.rect(), self._image)


class CvViewerNode(AbstractNodeInterface):
    startValue = 0
    width = 400
    height = 250
    colorTrain = []
    proxyWidget: ImageViewerWidget
    logo = r"Release/biggusFolder/imgs/logos/Qt.png"

    def __init__(self, inNum=1, outNum=1, parent=None):
        super().__init__("ImageViewerNode", inNum, outNum, parent)

        self.AddProxyWidget()

    def calculateOutput(self, plugIndex):
        value = self.inPlugs[0].getValue()
        if isinstance(value, np.ndarray):
            self.proxyWidget.setImage(value)
            if len(value.shape) == 2:
                value = cv2.cvtColor(value, cv2.COLOR_GRAY2BGR)  # converti l'immagine in scala di grigio in BGR
            elif len(value.shape) == 3 and value.shape[2] == 4:
                value = cv2.cvtColor(value, cv2.COLOR_RGBA2BGR)  # converti l'immagine RGBA in BGR
            elif len(value.shape) == 3 and value.shape[2] == 2:
                value = cv2.cvtColor(value, cv2.COLOR_GRAY2BGR)  # converti l'immagine a 2 canali in BGR
            height, width, channel = value.shape
            bytesPerLine = 3 * width
            qImg = QImage(value.data, width, height, bytesPerLine,
                          QImage.Format.Format_BGR888)  # converte l'immagine in un oggetto QImage in formato BGR
            self.proxyWidget.setImage(qImg)
        elif isinstance(value, QImage):
            self.proxyWidget.setImage(value)

        self.updateAll()
        self.outPlugs[plugIndex].setValue(value)
        return self.outPlugs[plugIndex].getValue()

    def setImage(self, image):
        self.viewer.setImage(image)

    def AddProxyWidget(self):
        self.viewer = ImageViewerWidget()
        self.proxyWidget = self.viewer
        self.proxyWidget.setFixedSize(self.width - 20, self.height - 50)
        self.nodeGraphic.createProxyWidget(self.proxyWidget)
        self.proxyWidget.setFixedWidth(self.width - 20)
        self.proxyWidget.setFixedHeight(self.height - 50)
        self.proxyWidget.move(int(self.width // 2 - self.proxyWidget.width() // 2),
                              int(self.height // 2 - self.proxyWidget.height() // 2) + 20)
