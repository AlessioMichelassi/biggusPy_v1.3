# -*- coding: utf-8 -*-
import math
import random

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMenu

from elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface


class BooleanNode(AbstractNodeInterface):
    resetValue = True
    menuReturnValue = "True"
    width = 70
    height = 60
    colorTrain = [QColor(89, 17, 18), QColor(132, 0, 0), QColor(220, 78, 182), QColor(87, 48, 27),
                  QColor(255, 255, 255), QColor(188, 64, 100), QColor(255, 33, 80), QColor(254, 130, 171), ]

    def __init__(self, value: bool = True, inNum=1, outNum=1, parent=None):
        super().__init__(value, inNum, outNum, parent)
        self.setClassName("BooleanNode")
        self.setName("BooleanNode")
        self.changeSize(self.width, self.height)
        self.changeInputValue(0, value, True)

    def calculateOutput(self, plugIndex):
        value = self.inPlugs[0].getValue()
        self.outPlugs[plugIndex].setValue(bool(value))
        return self.outPlugs[plugIndex].getValue()

    def redesign(self):
        self.changeSize(self.width, self.height)

    def showContextMenu(self, position):
        contextMenu = QMenu()
        contextMenu.addSection("set node")
        actionTrue = contextMenu.addAction("True")
        actionFalse = contextMenu.addAction("False")

        action = contextMenu.exec(position)
        if action == actionTrue:
            self.changeInputValue(0, True, True)
        elif action == actionFalse:
            self.changeInputValue(0, False, True)
