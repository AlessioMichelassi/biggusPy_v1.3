# -*- coding: utf-8 -*-
import math
import random
from typing import Union

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMenu

from elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface


class TupleNode(AbstractNodeInterface):
    menuReturnValue = "reset"
    startValue = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    width = 120
    height = 80
    colorTrain = [QColor(102, 92, 115), QColor(68, 61, 77), QColor(133, 120, 149), QColor(153, 138, 172),
                  QColor(184, 166, 207), QColor(3, 2, 3), QColor(68, 61, 77), QColor(133, 120, 149), ]

    def __init__(self, value: tuple[Union[int, float, str]] = None, inNum=1, outNum=1, parent=None):
        if value is None:
            value = self.startValue
        super().__init__(value, inNum, outNum, parent)
        self.setClassName("TupleNode")
        self.setName("TupleNode")
        self.changeSize(self.width, self.height)
        if value is not None:
            self.startValue = value
        else:
            value = self.startValue
        self.changeInputValue(0, value, True)

    def calculateOutput(self, plugIndex):
        value = self.inPlugs[0].getValue()
        valueSet = self.checkTuple(value)
        result = valueSet
        if self.menuReturnValue == "add":
            set2 = self.inPlugs[1].getValue()
            result.add(set2)
        elif self.menuReturnValue == "update":
            set2 = self.inPlugs[1].getValue()
            result.update(set2)
        elif self.menuReturnValue == "remove":
            value = self.inPlugs[1].getValue()
            try:
                result.remove(value)
            except KeyError:
                result = "value not in set"
            except TypeError:
                result = "value must be hashable"
        elif self.menuReturnValue == "discard":
            value = self.inPlugs[1].getValue()
            try:
                result.discard(value)
            except KeyError:
                result = "value not in set"
            except TypeError:
                result = "value must be hashable"
        elif self.menuReturnValue == "pop":
            try:
                result.pop()
            except KeyError:
                result = "set is empty"
        elif self.menuReturnValue == "clear":
            result.clear()
        elif self.menuReturnValue == "reset":
            result = self.startValue
        self.outPlugs[0].setValue(result)
        return self.outPlugs[plugIndex].getValue()

    def redesign(self):
        self.changeSize(self.width, self.height)

    def checkTuple(self, value):
        if isinstance(value, tuple):
            return value
        elif isinstance(value, list):
            return tuple(value)
        else:
            return tuple()

    def showContextMenu(self, position):
        """
        Il nodo deve avere un menu contestuale che permetta come nello stringNode di eseguire operazioni su una lista
        come append, insert, pop, remove, clear, index, sort, shuffle, reverse, extend
        :param position:
        :return:
        """
        contextMenu = QMenu()
        contextMenu.addSection("set")
        actions = {
            "add": self.doAdd,
            "update": self.doUpdate,
            "remove": self.doRemove,
            "discard": self.doDiscard,
            "pop": self.doPop,
            "clear": self.doClear,
            "reset": self.doReset,
        }
        for action in actions:
            contextMenu.addAction(action, actions[action])
        if selected_action := contextMenu.exec(position):
            action_func = actions[selected_action.text()]
            action_func()

        if self.nodeData.outConnections:
            for connection in self.nodeData.outConnections:
                connection.updateValue()
        else:
            self.nodeData.calculate()

    def doAdd(self):
        self.removeAllUnnecessaryPlugs()
        self.menuReturnValue = "add"
        self.addInPlug("add")
        self.changeInputValue(0, {})
        self.redesign()

    def doUpdate(self):
        self.removeAllUnnecessaryPlugs()
        self.menuReturnValue = "update"
        self.addInPlug("update")
        self.changeInputValue(0, {})
        self.redesign()

    def doRemove(self):
        self.removeAllUnnecessaryPlugs()
        self.menuReturnValue = "remove"
        self.addInPlug("remove")
        self.changeInputValue(0, {})
        self.redesign()

    def doDiscard(self):
        self.removeAllUnnecessaryPlugs()
        self.menuReturnValue = "discard"
        self.addInPlug("discard")
        self.changeInputValue(0, {})
        self.redesign()

    def doPop(self):
        self.removeAllUnnecessaryPlugs()
        self.menuReturnValue = "pop"
        value = self.inPlugs[0].getValue()
        valueSet = self.checkTuple(value)
        result = valueSet[:-1]
        self.changeInputValue(0, result)
        self.redesign()

    def doClear(self):
        self.removeAllUnnecessaryPlugs()
        self.menuReturnValue = "clear"
        self.changeInputValue(0, {})
        self.redesign()

    def doReset(self):
        self.removeAllUnnecessaryPlugs()
        self.menuReturnValue = "reset"
        self.changeInputValue(0, self.startValue)
        self.redesign()



