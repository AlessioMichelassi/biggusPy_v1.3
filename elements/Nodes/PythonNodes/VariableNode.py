# -*- coding: utf-8 -*-
import math
import random

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMenu

from elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface


class VariableNode(AbstractNodeInterface):
    resetValue = 0
    width = 50
    height = 120
    menuReturnValue = "int"
    colorTrain = [QColor(177, 225, 40), QColor(95, 217, 173), QColor(143, 129, 158), QColor(91, 240, 171),
                  QColor(220, 215, 146), QColor(30, 31, 2), QColor(97, 239, 255), QColor(149, 97, 228), ]

    def __init__(self, value=80, inNum=1, outNum=1, parent=None):
        super().__init__(value, inNum, outNum, parent)
        self.setClassName("VariableNode")
        self.setName("VariableNode")
        self.changeSize(self.width, self.height)
        self.changeInputValue(0, value, True)

    def calculateOutput(self, plugIndex):
        value = self.inPlugs[0].getValue()
        self.outPlugs[plugIndex].setValue(value)
        return self.outPlugs[plugIndex].getValue()

    def getCode(self):
        if not self.inConnections:
            return f'{self.getTitle()} = {self.inPlugs[0].getValue()}'
        inPlugNodeName, code = self.getCodeFromInput(0)
        return (
            f'{self.getTitle()} = {self.inPlugs[0].getValue()}'
            if inPlugNodeName is None
            else f'{code}\n{self.getTitle()} = {self.menuReturnValue}({inPlugNodeName})')

    def redesign(self):
        self.changeSize(self.width, self.height)

    def showContextMenu(self, position):
        contextMenu = QMenu()
        contextMenu.addSection("set type")
        actionInt = contextMenu.addAction("int")
        actionFloat = contextMenu.addAction("float")
        action = contextMenu.exec(position)
        self.menuReturnValue = action.text()
        if action == actionInt:
            self.changeInputValue(0, int(self.inPlugs[0].getValue()), True)
            self.nodeGraphic.updateTxtValuePosition()
        elif action == actionFloat:
            self.changeInputValue(0, float(self.inPlugs[0].getValue()), True)
            self.nodeGraphic.updateTxtValuePosition()
