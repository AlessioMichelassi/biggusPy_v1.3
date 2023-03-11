# -*- coding: utf-8 -*-
import math
import random

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMenu

from elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface


class IfNode(AbstractNodeInterface):
    resetValue = True
    menuReturnValue = "=="
    startValue = True
    width = 100
    height = 120
    colorTrain = [QColor(255, 255, 255), QColor(255, 0, 4), QColor(255, 246, 228), QColor(177, 202, 255),
                  QColor(255, 230, 177), QColor(52, 16, 38), QColor(255, 230, 177), QColor(255, 246, 228), ]

    def __init__(self, value: bool = True, inNum=4, outNum=1, parent=None):
        super().__init__(value, inNum, outNum, parent)

        self.menuReturnValue = "=="
        self.setClassName("IfNode")
        self.setName("IfNode")
        self.changeSize(self.width, self.height)
        self.changeInputValue(0, value, True)
        self.changeInputValue(1, value, True)
        self.setPlugInTitle(0, "leftOp")
        self.setPlugInTitle(1, "rightOp")
        self.setPlugInTitle(2, "trueFunction")
        self.setPlugInTitle(3, "falseFunction")

    def calculateOutput(self, plugIndex):
        val1 = self.inPlugs[0].getValue()
        val2 = self.inPlugs[1].getValue()
        operations = {
            "==": val1 == val2,
            "!=": val1 != val2,
            ">": val1 > val2,
            "<": val1 < val2,
            ">=": val1 >= val2,
            "<=": val1 <= val2,
            "inRange": val1 in range(val2),
        }
        value = operations[self.menuReturnValue]
        if value:
            self.outPlugs[plugIndex].setValue(self.inPlugs[2].getValue())
        else:
            if self.inPlugs[3].getValue() is not None:
                self.outPlugs[plugIndex].setValue(self.inPlugs[3].getValue())
            else:
                self.outPlugs[plugIndex].setValue(value)
        self.nodeGraphic.updateTxtValuePosition()
        return self.outPlugs[plugIndex].getValue()

    def getCode(self):
        return self.returnIfCode()

    def showContextMenu(self, position):
        contextMenu = QMenu()
        contextMenu.addSection("operation")
        action1 = contextMenu.addAction("==")
        action2 = contextMenu.addAction("!=")
        action3 = contextMenu.addAction(">")
        action4 = contextMenu.addAction("<")
        action5 = contextMenu.addAction(">=")
        action6 = contextMenu.addAction("<=")
        action7 = contextMenu.addAction("inRange")
        action = contextMenu.exec(position)
        if action == action1:
            self.execMenu(action1, "==")
        elif action == action2:
            self.execMenu(action2, "!=")
        elif action == action3:
            self.execMenu(action3, ">")
        elif action == action4:
            self.execMenu(action4, "<")
        elif action == action5:
            self.execMenu(action5, ">=")
        elif action == action6:
            self.execMenu(action6, "<=")
        elif action == action7:
            self.execMenu(action7, "inRange")

    def execMenu(self, action, operator):
        self.menuReturnValue = operator
        title = operator
        self.setGraphicTitleText(title)
        if self.nodeData.outConnections:
            for connection in self.nodeData.outConnections:
                connection.updateValue()
        else:
            self.nodeData.calculate()

    def returnIfCode(self):
        leftTitle, leftCode = self.getCodeFromInput(0)
        rightTitle, rightCode = self.getCodeFromInput(1)
        returnTrueTitle, returnTrueCode = self.getCodeFromInput(2)
        returnFalseTitle, returnFalseCode = self.getCodeFromInput(3)
        concatCode = f"{leftCode}\n{rightCode}\n{returnTrueCode}\n{returnFalseCode}"
        ifCode = f"if {leftTitle} {self.menuReturnValue} {rightTitle}:\n"
        ifBody = f"    return {returnTrueTitle}\nelse:\n    return {returnFalseTitle}"
        return f"{concatCode}\n{ifCode}{ifBody}"

    def setOperator(self, operator):
        self.menuReturnValue = operator
        title = operator
        self.setGraphicTitleText(title)
        if self.nodeData.outConnections:
            for connection in self.nodeData.outConnections:
                connection.updateValue()
        else:
            self.nodeData.calculate()

    def compare(self):
        # sourcery skip: assign-if-exp, boolean-if-exp-identity, remove-unnecessary-cast
        val1 = self.inPlugs[0].getValue()
        val2 = self.inPlugs[1].getValue()
        if val1 == val2:
            return True
        else:
            return False

    def different(self):
        # sourcery skip: assign-if-exp, boolean-if-exp-identity, remove-unnecessary-cast
        val1 = self.inPlugs[0].getValue()
        val2 = self.inPlugs[1].getValue()
        if val1 != val2:
            return True
        else:
            return False

    def greater(self):
        # sourcery skip: assign-if-exp, boolean-if-exp-identity, remove-unnecessary-cast
        val1 = self.inPlugs[0].getValue()
        val2 = self.inPlugs[1].getValue()
        if type(val1) == int and type(val2) == int:
            if val1 > val2:
                return True
            else:
                return False
        else:
            print("Error: Can't compare non-integers")
            return False

    def less(self):
        # sourcery skip: assign-if-exp, boolean-if-exp-identity, remove-unnecessary-cast
        val1 = self.inPlugs[0].getValue()
        val2 = self.inPlugs[1].getValue()
        if type(val1) == int and type(val2) == int:
            if val1 < val2:
                return True
            else:
                return False
        else:
            print("Error: Can't compare non-integers")
            return False

    def greaterOrEqual(self):
        # sourcery skip: assign-if-exp, boolean-if-exp-identity, remove-unnecessary-cast
        val1 = self.inPlugs[0].getValue()
        val2 = self.inPlugs[1].getValue()
        if type(val1) == int and type(val2) == int:
            if val1 >= val2:
                return True
            else:
                return False
        else:
            print("Error: Can't compare non-integers")

    def lessOrEqual(self):
        # sourcery skip: assign-if-exp, boolean-if-exp-identity, remove-unnecessary-cast
        val1 = self.inPlugs[0].getValue()
        val2 = self.inPlugs[1].getValue()
        if type(val1) == int and type(val2) == int:
            if val1 <= val2:
                return True
            else:
                return False
        else:
            print("Error: Can't compare non-integers")
            return False

    def inRange(self):
        # sourcery skip: assign-if-exp, boolean-if-exp-identity, remove-unnecessary-cast
        val1 = self.inPlugs[0].getValue()
        val2 = self.inPlugs[1].getValue()
        if type(val1) == int and type(val2) == int:
            return val1 in range(val2)
        print("Error: Can't compare non-integers")
        return False
