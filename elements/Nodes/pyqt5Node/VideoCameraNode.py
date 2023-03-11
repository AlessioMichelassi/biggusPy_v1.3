from PyQt5.QtCore import QDir, QUrl
from PyQt5.QtGui import QClipboard
from PyQt5.QtWidgets import QFileDialog, QApplication, QMenu

from elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface


class VideoCameraNode(AbstractNodeInterface):
    startValue = 0
    width = 50
    height = 120
    colorTrain = []
    logo = r"Release/biggusFolder/imgs/logos/Qt.png"

    def __init__(self, value="uriFile", inNum=2, outNum=1, parent=None):
        super().__init__(value, inNum, outNum, parent)
        self.setClassName("VideoCameraNode")
        self.setName("VideoCameraNode")
        self.changeSize(self.width, self.height)

    def calculateOutput(self, plugIndex):
        value = self.inPlugs[0].getValue()
        self.outPlugs[plugIndex].setValue(value)
        return self.outPlugs[plugIndex].getValue()

    def redesign(self):
        self.changeSize(self.width, self.height)

    def showContextMenu(self, position):
        contextMenu = QMenu(self)
        contextMenu.addSection("load a video file")
        action1 = contextMenu.addAction("load file")
        action2 = contextMenu.addAction("set as URL")
        action = contextMenu.exec(position)
        if action == action1:
            self.action1()
        elif action == action2:
            self.action2()

    def action1(self):
        pass

    def action2(self):
        pass

    def detectCamera(self):
        if not self.available_cameras:
            return

