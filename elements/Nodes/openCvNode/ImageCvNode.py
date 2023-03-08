from PyQt5.QtCore import QDir
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMenu, QFileDialog
import cv2 as cv
import sys
from elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface


class ImageCvNode(AbstractNodeInterface):
    startValue = r"Release/biggusFolder/imgs/imgs/len_full.jpg"
    width = 50
    height = 120
    colorTrain = []

    def __init__(self, value= 20, inNum=2, outNum=1, parent=None):
        super().__init__(value, inNum, outNum, parent)
        self.setClassName("ImageCvNode")
        self.setName("ImageCvNode")
        self.changeSize(self.width, self.height)

    def calculateOutput(self, plugIndex):
        # sourcery skip: use-named-expression
        path = self.inPlugs[0].getValue()
        if path:
            value = cv.imread(path)
            if value is None:
                value = cv.imread(self.startValue)
            self.outPlugs[plugIndex].setValue(value)
            return self.outPlugs[plugIndex].getValue()

    def redesign(self):
        self.changeSize(self.width, self.height)

    def showContextMenu(self, position):
        contextMenu = self.contextMenu
        contextMenu.addSection("change name of menu here")
        action1 = contextMenu.addAction("open _image")

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
