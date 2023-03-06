# -*- coding: utf-8 -*-
import math
import random
from typing import Union

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMenu

from elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface


class ForNode(AbstractNodeInterface):
    resetValue = []
    startFunction = lambda x: x
    width = 120
    height = 80
    colorTrain = [QColor(184, 204, 236), QColor(252, 104, 95), QColor(178, 218, 131), QColor(130, 177, 107),
                  QColor(198, 179, 250), QColor(20, 245, 238), QColor(46, 85, 40), QColor(165, 36, 53), ]

    def __init__(self, value: list[Union[int, float, str]] = None, inNum=2, outNum=1, parent=None):
        super().__init__(value, inNum, outNum, parent)
        self.setClassName("ForNode")
        self.setName("ForNode")
        self.changeSize(self.width, self.height)
        if value is None:
            value = []
        self.changeInputValue(0, value, True)
        self.setPlugInTitle(0, "iterable")
        self.setPlugInTitle(1, "function")

    def calculateOutput(self, plugIndex):
        iterable = self.inPlugs[0].getValue()
        function = self.createFunction(self.inPlugs[1].getValue())
        accumulator = None
        for value in iterable:
            accumulator = function(value)
        self.outPlugs[0].setValue(accumulator)
        return self.outPlugs[0].getValue()

    @staticmethod
    def createFunction(_function):
        return _function if callable(_function) else (lambda x: x)


