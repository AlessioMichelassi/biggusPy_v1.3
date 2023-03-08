import cv2
import numpy as np
from PyQt5.QtCore import Qt, QDir, QUrl
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtWidgets import *

from elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface


class imageViewer(QGraphicsView):
    _image = None
    _imagePath = r"Release/biggusFolder/imgs/imgs/lena_std.tif"
    imageView: QGraphicsPixmapItem

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

    def initImageViewer(self):
        """
        ITA:
            crea un oggetto QGraphicItem che contiene l'immagine
        ENG:
            create a QGraphicItem object that contains the _image
        :return:
        """
        self.imageView = QGraphicsPixmapItem()
        self._image = QImage(self._imagePath)
        self.imageView.setPixmap(QPixmap.fromImage(self._image))
        self.scene.addItem(self.imageView)
        self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

    def setImage(self, uri):
        self.scene.clear()
        self._image = QImage(uri)
        self.scene.addPixmap(QPixmap.fromImage(self._image))
        self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

    def setCvImage(self, cvImage):
        self.scene.clear()
        rgbImage = cv2.cvtColor(cvImage, cv2.COLOR_BGR2RGB)
        self._image = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
        self.scene.addPixmap(QPixmap.fromImage(self._image))
        self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

    def resizeEvent(self, event):
        self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        self.centerOn(self.scene.sceneRect().center())

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.scale(1.1, 1.1)
        else:
            self.scale(0.9, 0.9)

    def contextMenuEvent(self, event) -> None:
        menu = QMenu()
        action1 = menu.addAction("loadImage")
        action2 = menu.addAction("saveImageAs")
        action3 = menu.addAction("blackAndWhite")
        menu.exec_(event.globalPos())

        if action1 == menu.exec_(event.globalPos()):
            self.loadImage()
        elif action2 == menu.exec_(event.globalPos()):
            self.saveImageAs()
        elif action3 == menu.exec_(event.globalPos()):
            self.blackAndWhite()

    def loadImage(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        dialog.setFilter(QDir.Files)
        if dialog.exec_():
            fileNames = dialog.selectedFiles()
            self._imagePath = fileNames[0]
            self.setImage(self._imagePath)

    def saveImageAs(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        dialog.setFilter(QDir.Files)
        if dialog.exec_():
            fileNames = dialog.selectedFiles()
            self._image.save(fileNames[0])

    def blackAndWhite(self):
        self._image = self._image.convertToFormat(QImage.Format.Format_Grayscale8)
        self.setImage(self._imagePath)


class ImageViewerNode(AbstractNodeInterface):
    startValue = 0
    width = 400
    height = 250
    colorTrain = []
    proxyWidget: imageViewer

    def __init__(self, value=20, inNum=2, outNum=1, parent=None):
        super().__init__(value, inNum, outNum, parent)
        self.setClassName("ImageViewer")
        self.setName("ImageViewer")
        self.changeSize(self.width, self.height)
        self.AddProxyWidget()

    def calculateOutput(self, plugIndex):
        value = self.inPlugs[0].getValue()
        try:
            if isinstance(value, np.ndarray):
                self.proxyWidget.setCvImage(value)
            elif isinstance(value, QImage):
                self.proxyWidget.setImage(value)
        except Exception as e:
            print(f"invalid video path: {value}")
        self.outPlugs[plugIndex].setValue(value)
        return self.outPlugs[plugIndex].getValue()

    def redesign(self):
        self.changeSize(self.width, self.height)

    def showContextMenu(self, position):
        contextMenu = self.contextMenu
        contextMenu.addSection("change name of menu here")
        action1 = contextMenu.addAction("action1")
        action2 = contextMenu.addAction("action2")
        action3 = contextMenu.addAction("action3")

        action = contextMenu.exec(position)
        if action == action1:
            self.doAction1()
        elif action == action2:
            self.doAction2()
        elif action == action3:
            self.doAction3()

    def doAction1(self):
        pass

    def doAction2(self):
        pass

    def doAction3(self):
        pass

    def AddProxyWidget(self):
        self.proxyWidget = imageViewer()
        self.proxyWidget.setFixedSize(self.width - 20, self.height - 50)
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
