# -*- coding: utf-8 -*-
import math
import random
from typing import Union

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMenu

from elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface


class AndNode(AbstractNodeInterface):
    startValue = True
    width = 120
    height = 80
    operations = ["and", "or", "not"]
    default_operation = "and"
    colorTrain = [QColor(255, 230, 132), QColor(132, 157, 255), QColor(132, 157, 255), QColor(132, 255, 169),
                  QColor(255, 175, 113), QColor(22, 38, 50), QColor(113, 193, 255), QColor(122, 255, 113), ]
    menuReturnValue = "and"

    def __init__(self, value: Union[int, float, str] = False, operation=None, inNum=2, outNum=1, parent=None):
        super().__init__(value, inNum, outNum, parent)
        self.setClassName("AndNode")
        self.setName("AndNode")
        self.changeSize(self.width, self.height)
        self.operation = operation if operation in self.operations else self.default_operation
        self.changeInputValue(0, value, True)

    def calculateOutput(self, plugIndex):
        in1 = self.inPlugs[0].getValue()
        in2 = self.inPlugs[1].getValue()
        operations = {
            "and": in1 and in2,
            "or": in1 or in2,
            "not": not in1,
        }
        result = operations[self.menuReturnValue]
        self.outPlugs[0].setValue(result)
        return self.outPlugs[0].getValue()

    def getCode(self):
        if not self.inConnections:
            return f'{self.getTitle()} = {self.inPlugs[0].getValue()}'
        inPlugNodeName1, code1 = self.getCodeFromInput(0)
        inPlugNodeName2, code2 = self.getCodeFromInput(1)
        return (
            f'{self.getTitle()} = {self.inPlugs[0].getValue()}'
            if inPlugNodeName1 is None
            else f'{code1}\n{code2}\n{self.getTitle()} = {inPlugNodeName1} {self.menuReturnValue} {inPlugNodeName2}')

    def redesign(self):
        self.changeSize(self.width, self.height)

    def showContextMenu(self, position):
        contextMenu = QMenu()
        contextMenu.addSection("set node")

        contextMenu.addAction("and")
        contextMenu.addAction("or")
        contextMenu.addAction("not")

        action = contextMenu.exec(position)
        self.menuReturnValue = action.text()


