# -*- coding: utf-8 -*-
import math
import random

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMenu

from elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface


class IfNode(AbstractNodeInterface):
    resetValue = True
    menuReturnValue = "=="
    width = 120
    height = 80
    colorTrain = [QColor(255, 255, 255), QColor(255, 0, 4), QColor(255, 246, 228), QColor(177, 202, 255),
                  QColor(255, 230, 177), QColor(52, 16, 38), QColor(255, 230, 177), QColor(255, 246, 228), ]

    def __init__(self, value: bool = True, inNum=2, outNum=2, parent=None):
        super().__init__(value, inNum, outNum, parent)

        self.menuReturnValue = "=="
        self.setClassName("IfNode")
        self.setName("IfNode")
        self.changeSize(self.width, self.height)
        self.changeInputValue(0, value, True)
        self.changeInputValue(1, value, True)

    def calculateOutput(self, plugIndex):
        operations = {
            "==": self.compare,
            "!=": self.different,
            ">": self.greater,
            "<": self.less,
            ">=": self.greaterOrEqual,
            "<=": self.lessOrEqual,
            "inRange": self.inRange,
        }
        var = operations[self.menuReturnValue]()
        if plugIndex == 0:
            self.outPlugs[0].setValue(var)
            return self.outPlugs[0].getValue()
        elif plugIndex == 1:
            self.outPlugs[1].setValue(not var)
            return self.outPlugs[1].getValue()

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
            self.menuReturnValue = "=="
        elif action == action2:
            self.menuReturnValue = "!="
        elif action == action3:
            self.menuReturnValue = ">"
        elif action == action4:
            self.menuReturnValue = "<"
        elif action == action5:
            self.menuReturnValue = ">="
        elif action == action6:
            self.menuReturnValue = "<="
        elif action == action7:
            self.menuReturnValue = "inRange"

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
