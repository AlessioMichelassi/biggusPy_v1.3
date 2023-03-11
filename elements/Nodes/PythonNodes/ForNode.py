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
        self.changeInputValue(1, None, True)

    def calculateOutput(self, plugIndex):
        iterable = self.inPlugs[0].getCode()
        function = self.inPlugs[1].getValue()
        if function is not None:
            try:
                function_code = compile(function, "<string>", "exec")
                local_context = {"iterable": iterable}
                global_context = {}
                exec(function_code, global_context, local_context)
                returnValue = local_context.get("returnValue", [])
            except Exception as e:
                print(f"WARNING FROM FOR NODE: FUNCTION IS NOT VALID\n{e}")
                print("__" * 20)
                returnValue = []
            self.outPlugs[plugIndex].setValue(returnValue)
        return self.outPlugs[plugIndex].getValue()

    def executeForBody(self, code, element):
        # Creazione del dizionario con le variabili da utilizzare all'interno della funzione
        local_vars = {"elements": element}

        # Esecuzione del codice all'interno del for, passando il dizionario delle variabili
        # e catturando eventuali errori
        try:
            exec(code, globals(), local_vars)
            result = local_vars.get("returnValue", None)
        except Exception as e:
            print(f"ERROR: {e}")
            result = None

        return result
