# -*- coding: utf-8 -*-
import math
import random

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMenu

from elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface


class NumberNode(AbstractNodeInterface):
    startValue = 0
    width = 50
    height = 120
    colorTrain = [QColor(177, 225, 40), QColor(95, 217, 173), QColor(143, 129, 158), QColor(91, 240, 171),
                  QColor(220, 215, 146), QColor(30, 31, 2), QColor(97, 239, 255), QColor(149, 97, 228), ]

    def __init__(self, value=80, inNum=1, outNum=1, parent=None):
        super().__init__(value, inNum, outNum, parent)
        self.setClassName("NumberNode")
        self.setName("NumberNode")
        self.changeSize(self.width, self.height)
        self.changeInputValue(0, value, True)

    def calculateOutput(self, plugIndex):
        value = self.inPlugs[0].getValue()
        self.outPlugs[plugIndex].setValue(value)
        return self.outPlugs[plugIndex].getValue()

    def redesign(self):
        self.changeSize(self.width, self.height)

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

    def randomInt(self):
        value = random.randint(1, 99)
        self.changeInputValue(0, value, True)
        self.updateAll()

    def randomFloat(self):
        value = random.uniform(1.0, 99.0)
        self.changeInputValue(0, value, True)
        self.updateAll()

    def pi(self):
        value = math.pi
        self.changeInputValue(0, value, True)
        self.updateAll()

    def euler(self):
        value = math.e
        self.changeInputValue(0, value, True)
        self.updateAll()
