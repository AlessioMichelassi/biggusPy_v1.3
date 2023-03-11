# -*- coding: utf-8 -*-
import ast
import math
import random
from typing import Union

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMenu

from elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface

testCode = """
numbers = [1, 2, 3, 4, 5]
total = 0
for n in numbers:
    total += n
print(total)"""

testCode2 = """
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)
"""

class ForNode(AbstractNodeInterface):
    resetValue = []
    startFunction = lambda x: x
    startValue = []
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
        self.changeInputValue(1, self.startFunction, True)

    def calculateOutput(self, plugIndex):
        iterable = self.inPlugs[0].getValue()
        function = self.inPlugs[1].getValue()
        if function is not None:
            try:
                functionGlobals = {}
                exec(function, functionGlobals)
                returnFunction = functionGlobals["function"]
                returnValue = [returnFunction(value) for value in iterable]
            except Exception as e:
                print(f"WARNING FROM FOR NODE: FUNCTION IS NOT VALID\n{e}")
                print("__"*20)
                returnValue = []
            self.outPlugs[plugIndex].setValue(returnValue)
        return self.outPlugs[plugIndex].getValue()




