# -*- coding: utf-8 -*-
import math
import random

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMenu

from elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface


class DictionaryNode(AbstractNodeInterface):
    menuReturnValue = "reset"
    resetValue = {"a": 1, "b": 2, "c": 3}
    startValue = {"a": 1, "b": 2, "c": 3}
    width = 120
    height = 80
    colorTrain = [QColor(102, 92, 115), QColor(68, 61, 77), QColor(133, 120, 149), QColor(153, 138, 172),
                  QColor(184, 166, 207), QColor(3, 2, 3), QColor(68, 61, 77), QColor(133, 120, 149), ]

    def __init__(self, value: dict = None, inNum=1, outNum=1, parent=None):
        super().__init__(value, inNum, outNum, parent)
        self.setClassName("DictionaryNode")
        self.setName("DictionaryNode")
        self.changeSize(self.width, self.height)
        if value is not None:
            self.startValue = value
        else:
            value = self.startValue
        self.changeInputValue(0, value, True)

    def calculateOutput(self, plugIndex):
        value = self.inPlugs[0].getValue()
        valueDict = self.checkDict(value)
        result = valueDict
        if len(self.inPlugs) > 1:
            if self.menuReturnValue == "update":
                dict2 = self.inPlugs[1].getValue()
                result.update(dict2)
            elif self.menuReturnValue == "get":
                key = self.inPlugs[1].getValue()
                result = result.get(key)
            elif self.menuReturnValue == "remove":
                key = self.inPlugs[1].getValue()
                try:
                    result.pop(key)
                except KeyError:
                    result = f"Key '{key}' not found."
        self.outPlugs[plugIndex].setValue(result)
        return self.outPlugs[plugIndex].getValue()

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

    def checkDict(self, value):
        if not isinstance(value, dict):
            print("Value is not a dictionary. Resetting to default.")
        return self.startValue
