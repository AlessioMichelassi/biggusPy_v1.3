from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import cv2

from elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface


class blinker(QWidget):
    lblBlink: QLabel
    lblImage: QLabel

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.lblBlink = QLabel(self)
        self.lblBlink.setFixedSize(20, 10)
        layout = QVBoxLayout()
        layout.addWidget(self.lblBlink, 0, Qt.AlignCenter)
        layout.setContentsMargins(2, 2, 2, 2)
        self.setStyleSheet("background-color: transparent; border: 1px solid black; border-radius: 2px;")
        self.setLayout(layout)

    def doBlinking(self, blink):
        if blink:
            style = "QLabel { background-color : red; }"
        else:
            style = "QLabel { background-color : rgb(10,10,10); }"
        self.lblBlink.setStyleSheet(style)


class CameraWorker(QThread):
    frame_ready = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.cam = cv2.VideoCapture(0)
        self.frame = None
        self._stopped = False

    def run(self):
        while not self._stopped:
            ret, self.frame = self.cam.read()
            if ret:
                self.frame_ready.emit(self.frame)

    def stop(self):
        self._stopped = True
        self.wait()
        self.cam.release()


class VideoCVCameraNode(AbstractNodeInterface):
    startValue = 0
    width = 50
    height = 120
    colorTrain = [QColor(255, 234, 242), QColor(255, 91, 110), QColor(142, 255, 242), QColor(218, 255, 251),
                  QColor(110, 255, 91), QColor(170, 61, 73), QColor(52, 19, 23), QColor(142, 255, 242)]
    logo = r"Release/biggusFolder/imgs/logos/openCvLogo.png"
    proxyWidget: blinker
    isBlinking = False

    def __init__(self, value="uriFile", inNum=1, outNum=1, parent=None):
        super().__init__(value, inNum, outNum, parent)
        self.setClassName("VideoCameraNode")
        self.setName("VideoCameraNode")
        self.changeSize(self.width, self.height)
        self.AddProxyWidget()
        self.videoCamera = CameraWorker()  # Cambio dell'istanza con il thread
        self.videoCamera.frame_ready.connect(self.process_frames)

        self.frameImage = QImage()
        self.lastFrame = None

    def calculateOutput(self, plugIndex):
        value = self.inPlugs[0].getValue()
        self.outPlugs[plugIndex].setValue(value)
        return self.outPlugs[plugIndex].getValue()

    def process_frames(self, frame):
        self.changeInputValue(0, frame)
        self.calculateOutput(0)
        # visualizza il frame nel widget proxy
        height, width, channel = frame.shape
        bytesPerLine = 3 * width
        qImg = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
        return QPixmap.fromImage(qImg)

    def redesign(self):
        self.changeSize(self.width, self.height)

    def updateAll(self):
        super().updateAll()
        self.isBlinking = not self.isBlinking
        self.proxyWidget.doBlinking(self.isBlinking)

    def AddProxyWidget(self):
        self.proxyWidget = blinker()
        self.nodeGraphic.createProxyWidget(self.proxyWidget)
        self.proxyWidget.setFixedWidth(self.width - 20)
        self.proxyWidget.setFixedHeight(20)
        self.proxyWidget.move(int(self.width // 2 - self.proxyWidget.width() // 2),
                              int(self.height - 30))

    def onClose(self):
        # Stop al worker del thread
        self.videoCamera.stop()
        super().onClose()

    def showContextMenu(self, position):
        menu = QMenu()
        action1 = menu.addAction("Start")
        action2 = menu.addAction("Save Video As")
        action3 = menu.addAction("Stop")

        action = menu.exec_(position)
        if action == action1:
            self.videoCamera.start()
        elif action == action2:
            print("Save Video As")
        elif action == action3:
            self.videoCamera.stop()
