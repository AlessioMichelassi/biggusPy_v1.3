import cv2
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtWidgets import *

from elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface
from elements.Nodes.openCvNode.VideoCVCameraNode import VideoCVCameraNode


class usbCameraEasy(QObject):
    frame_ready = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.cam = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.start)

    def start(self):
        ret, frame = self.cam.read()
        if ret:
            self.frame_ready.emit(frame)

    def start_capture(self):
        self.timer.start(1)  # 1 millisecond interval

    def stop_capture(self):
        self.timer.stop()
        self.cam.release()


class imageViewer(QGraphicsView):
    _image = None
    imageView: QGraphicsPixmapItem
    _maxScale = 10.0

    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.verticalScrollBar().setDisabled(True)
        self.horizontalScrollBar().setDisabled(True)
        self.setStyleSheet("background:rgb(20,20,20); border: 6px;")
        # create the image viewer widget
        self.initImageViewer()
        self.setFixedSize((640 - 20), (480 - 20))
        self.camera_node = usbCameraEasy()
        self.camera_node.frame_ready.connect(self.process_frames)

    def initImageViewer(self):
        self.imageView = QGraphicsPixmapItem()
        self._image = np.zeros((480, 640, 3), dtype=np.uint8)
        self.imageView.setPixmap(QPixmap.fromImage(
            QImage(self._image.data, self._image.shape[1], self._image.shape[0], QImage.Format.Format_RGB888)))
        self.scene.addItem(self.imageView)
        self.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def setImage(self, frame):
        self.scene.clear()
        self.scene.addPixmap(frame)
        self.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def process_frames(self, frame):
        if isinstance(frame, np.ndarray):
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            bytesPerLine = 3 * width
            qImg = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qImg)
            self.setImage(pixmap)

    def resizeEvent(self, event):
        self.centerOn(self.scene.sceneRect().center())

    def contextMenuEvent(self, QContextMenuEvent):
        contextMenu = QMenu(self)
        contextMenu.addAction("startCamera")
        contextMenu.addAction("stopCamera")

        action = contextMenu.exec_(self.mapToGlobal(QContextMenuEvent.pos()))
        if action:
            if action.text() == "startCamera":
                self.camera_node.start_capture()
            elif action.text() == "stopCamera":
                self.camera_node.stop_capture()

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        scaleFactor = 1.1 if delta > 0 else 0.9
        self.scaleScene(scaleFactor)

    def scaleScene(self, scaleFactor):
        """
        Scale the scene
        :param scaleFactor:
        :return:
        """
        self.scale(scaleFactor, scaleFactor)


class VideoCVCameraTestNode(AbstractNodeInterface):
    startValue = 0
    width = 640
    height = 480
    colorTrain = [QColor(189, 149, 245), QColor(95, 33, 68), QColor(255, 167, 78), QColor(255, 188, 228),
                  QColor(255, 255, 255), QColor(66, 76, 163), QColor(163, 49, 117), QColor(255, 139, 209)]
    proxyWidget: imageViewer
    lastImage = None
    logo = r"Release/biggusFolder/imgs/logos/Qt.png"
    imageView: QGraphicsPixmapItem

    def __init__(self, value=20, inNum=1, outNum=1, parent=None):
        super().__init__(value, inNum, outNum, parent)
        self.setClassName("VideoMonitorNode")
        self.setName("VideoMonitorNode")
        self.AddProxyWidget()
        self.changeSize(self.width, self.height)

    def calculateOutput(self, plugIndex):  # sourcery skip: extract-method
        value = self.inPlugs[0].getValue()
        if isinstance(value, VideoCVCameraNode):
            self.process_input(value.frame)
        self.outPlugs[plugIndex].setValue(value)
        return self.outPlugs[plugIndex].getValue()

    def process_input(self, value):
        if isinstance(value, np.ndarray):
            frame = cv2.cvtColor(value, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            bytesPerLine = 3 * width
            qImg = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qImg)
            self.proxyWidget.setImage(pixmap)
            self.lastImage = value

    def redesign(self):
        self.changeSize(self.width, self.height)

    def AddProxyWidget(self):
        self.proxyWidget = imageViewer()
        self.nodeGraphic.createProxyWidget(self.proxyWidget)
        self.proxyWidget.setFixedWidth(self.width - 20)
        self.proxyWidget.setFixedHeight(self.height - 50)
        self.proxyWidget.move(int(self.width // 2 - self.proxyWidget.width() // 2),
                              int(self.height // 2 - self.proxyWidget.height() // 2) + 20)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    player = imageViewer()
    player.resize(320, 240)
    player.show()

    sys.exit(app.exec_())
