from PyQt5.QtCore import QDir
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMenu, QFileDialog
import cv2 as cv
import sys
from elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface


class ImageCvNode(AbstractNodeInterface):
    startValue = r"Release/biggusFolder/imgs/imgs/len_full.jpg"
    width = 80
    height = 120
    colorTrain = [QColor(255, 234, 242),QColor(255, 91, 110),QColor(142, 255, 242),QColor(218, 255, 251),QColor(110, 255, 91),QColor(170, 61, 73),QColor(52, 19, 23),QColor(142, 255, 242),]

    logo = r"Release/biggusFolder/imgs/logos/openCvLogo.png"

    def __init__(self, value = None, inNum=1, outNum=1, parent=None):
        super().__init__(value, inNum, outNum, parent)
        self.setClassName("ImageCvNode")
        self.setName("ImageCvNode")
        if value is not None:
            self.startValue = value
        self.changeInputValue(0, value)
        self.changeSize(self.width, self.height)
        self.updateAll()

    def calculateOutput(self, plugIndex):
        # sourcery skip: use-named-expression
        path = self.inPlugs[0].getValue()
        if path:
            value = cv.imread(path, cv.IMREAD_UNCHANGED)
            if value is None:
                value = cv.imread(self.startValue, cv.IMREAD_UNCHANGED)
            self.outPlugs[plugIndex].setValue(value)
            return self.outPlugs[plugIndex].getValue()

    def redesign(self):
        self.changeSize(self.width, self.height)

    def showContextMenu(self, position):
        contextMenu = QMenu()
        contextMenu.addSection("Open Image")
        action1 = contextMenu.addAction("Open Image")
        action = contextMenu.exec(position)
        if action == action1:
            self.openImage()

    def openImage(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setFilter(QDir.Files)
        if dialog.exec_():
            fileNames = dialog.selectedFiles()
            self.startValue = fileNames[0]
            self.changeInputValue(0, self.startValue, True)
            self.calculateOutput(0)
            self.updateAll()
