import math
import random

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from elements.Nodes.AbstractNodeData import AbstractNodeData


class NumberNode(AbstractNodeData):
    _className = "NumberNode"
    startValue = 0

    def __init__(self, value, inNum=1, outNum=1):
        super().__init__(inNum, outNum)
        self.startValue = value
        self.changeValue(value, type(value), 0, True)

    def calculateOutput(self, plugIndex):
        value = self.inPlugs[0].getValue()
        if self.checkInput(int):
            self.outPlugs[plugIndex].setValue(value[0], int, f"{self.getTitle()} = {self.inPlugs[0].getValue()[0]}")
        elif self.checkInput(float):
            self.outPlugs[plugIndex].setValue(value[0], float, f"{self.getTitle()} = {self.inPlugs[0].getValue()[0]}")
        return self.outPlugs[plugIndex].getValue()

    def redesign(self):
        pass

    def showContextMenu(self, position):
        contextMenu = QMenu()
        contextMenu.addSection("set value")
        actionRandomInt = contextMenu.addAction("random int")
        actionRandomFloat = contextMenu.addAction("random float")
        actionPI = contextMenu.addAction("pi")
        actionEuler = contextMenu.addAction("euler")

        action = contextMenu.exec(position)
        if action == actionRandomInt:
            self.randomInt()
        elif action == actionRandomFloat:
            self.randomFloat()
        elif action == actionPI:
            self.pi()
        elif action == actionEuler:
            self.euler()

    def updateNode(self, className, value):
        title = className.title()
        self.nodeInterface.nodeGraphic.setTitle(title)
        self.nodeInterface.updateTxtTitleFromGraphics(title)
        self.nodeInterface.updateInPlugValueFromGraphics(value)

    def randomInt(self):
        value = random.randint(1, 99)
        self.changeValue(value, type(value), 0, True)
        self.updateNode("randomInt", value)

    def randomFloat(self):
        value = random.uniform(1.0, 99.0)
        self.changeValue(value, type(value), 0, True)
        self.updateNode("randomFloat", value)

    def pi(self):
        value = math.pi
        self.changeValue(value, type(value), 0, True)
        self.updateNode("pi", value)

    def euler(self):
        value = math.e
        self.changeValue(value, type(value), 0, True)
        self.updateNode("euler", value)