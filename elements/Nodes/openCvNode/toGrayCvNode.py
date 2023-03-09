from PyQt5.QtCore import QDir
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMenu, QFileDialog
import cv2
import sys
from elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface


class toGrayCvNode(AbstractNodeInterface):
    startValue = ""
    menuOperation = "luminosity"
    width = 80
    height = 120
    colorTrain = [QColor(255, 234, 242), QColor(255, 91, 110), QColor(142, 255, 242), QColor(218, 255, 251),
                  QColor(110, 255, 91), QColor(170, 61, 73), QColor(52, 19, 23), QColor(142, 255, 242), ]
    logo = r"Release/biggusFolder/imgs/logos/openCvLogo.png"

    def __init__(self, value=None, inNum=1, outNum=1, parent=None):
        super().__init__(value, inNum, outNum, parent)
        self.setClassName("toGrayCvNode")
        self.setName("toGrayCv")
        self.changeSize(self.width, self.height)

    def calculateOutput(self, plugIndex):
        value = self.inPlugs[0].getValue()
        operation = {"luminosity": self.doByLuminosity,
                     "max": self.doByMax,
                     "min": self.doByMin,
                     "red": self.doByRed,
                     "green": self.doByGreen,
                     "blue": self.doByBlue,
                     "hue": self.doByHue,
                     "saturation": self.doBySaturation,
                     "value": self.doByValue
                     }

        if value is None:
            value = cv2.imread(self.startValue)
        outValue = operation[self.menuOperation]()
        self.outPlugs[plugIndex].setValue(outValue)
        return self.outPlugs[plugIndex].getValue()

    def redesign(self):
        self.changeSize(self.width, self.height)

    def showContextMenu(self, position):
        contextMenu = QMenu()
        contextMenu.addSection("change name of menu here")
        action1 = contextMenu.addAction("by Luminosity")
        action6 = contextMenu.addAction("by Max")
        action7 = contextMenu.addAction("by Min")
        action8 = contextMenu.addAction("by Red")
        action9 = contextMenu.addAction("by Green")
        action10 = contextMenu.addAction("by Blue")
        action11 = contextMenu.addAction("by Hue")
        action12 = contextMenu.addAction("by Saturation")
        action13 = contextMenu.addAction("by Value")

        action = contextMenu.exec(position)
        if action == action1:
            self.doByLuminosity()
        elif action == action6:
            self.doByMax()
        elif action == action7:
            self.doByMin()
        elif action == action8:
            self.doByRed()
        elif action == action9:
            self.doByGreen()
        elif action == action10:
            self.doByBlue()
        elif action == action11:
            self.doByHue()
        elif action == action12:
            self.doBySaturation()
        elif action == action13:
            self.doByValue()

        if self.nodeData.outConnections:
            for connection in self.nodeData.outConnections:
                connection.updateValue()
        else:
            self.nodeData.calculate()

    def doByLuminosity(self):
        self.menuOperation = "luminosity"
        image = self.inPlugs[0].getValue()
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def doByMax(self):
        self.menuOperation = "max"
        image = self.inPlugs[0].getValue()
        r, g, b = cv2.split(image)
        return cv2.max(cv2.max(r, g), b)

    def doByMin(self):
        self.menuOperation = "min"
        image = self.inPlugs[0].getValue()
        r, g, b = cv2.split(image)
        return cv2.min(cv2.min(r, g), b)

    def doByRed(self):
        self.menuOperation = "red"
        image = self.inPlugs[0].getValue()
        return image[:, :, 2]

    def doByGreen(self):
        self.menuOperation = "green"
        image = self.inPlugs[0].getValue()
        return image[:, :, 1]

    def doByBlue(self):
        self.menuOperation = "blue"
        image = self.inPlugs[0].getValue()
        return image[:, :, 0]

    def doByHue(self):
        self.menuOperation = "hue"
        image = self.inPlugs[0].getValue()
        return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)[:, :, 0]

    def doBySaturation(self):
        self.menuOperation = "saturation"
        image = self.inPlugs[0].getValue()
        return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)[:, :, 1]

    def doByValue(self):
        self.menuOperation = "value"
        image = self.inPlugs[0].getValue()
        return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)[:, :, 2]
