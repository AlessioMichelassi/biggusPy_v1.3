# -*- coding: utf-8 -*-
import math
import random
from typing import Union

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMenu

from elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface


class SetNode(AbstractNodeInterface):
    menuReturnValue = "reset"
    resetValue = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
    width = 120
    height = 80
    colorTrain = [QColor(102, 92, 115), QColor(68, 61, 77), QColor(133, 120, 149), QColor(153, 138, 172),
                  QColor(184, 166, 207), QColor(3, 2, 3), QColor(68, 61, 77), QColor(133, 120, 149), ]

    def __init__(self, value: set[Union[int, float, str]] = None, inNum=1, outNum=1, parent=None):
        super().__init__(value, inNum, outNum, parent)
        self.setClassName("SetNode")
        self.setName("SetNode")
        self.changeSize(self.width, self.height)
        if value is not None:
            self.startValue = value
        else:
            value = self.startValue
        self.changeInputValue(0, value, True)

    def calculateOutput(self, plugIndex):
        value = self.inPlugs[0].getValue()
        valueSet = self.checkSet(value)
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
                result = "node not in set"
            except TypeError:
                result = "node must be hashable"
        elif self.menuReturnValue == "discard":
            value = self.inPlugs[1].getValue()
            try:
                result.discard(value)
            except KeyError:
                result = "node not in set"
            except TypeError:
                result = "node must be hashable"
        elif self.menuReturnValue == "pop":
            try:
                result.pop()
            except KeyError:
                result = "set is empty"
        elif self.menuReturnValue == "clear":
            result.clear()
            result: set = set()
        elif self.menuReturnValue == "reset":
            result = self.startValue
        self.outPlugs[plugIndex].setValue(result)
        return self.outPlugs[plugIndex].getValue()

    def redesign(self):
        self.changeSize(self.width, self.height)

    def showContextMenu(self, position):
        contextMenu = QMenu()
        contextMenu.addSection("set")
        actions = {
            "add": self.doAdd,
            "update": self.doUpdate,
            "remove": self.doRemove,
            "discard": self.doDiscard,
            "pop": self.doPop,
            "clear": self.doClear,
            "reset": self.doReset
        }
        for action_name in actions:
            contextMenu.addAction(action_name)

        if selected_action := contextMenu.exec(position):
            action_func = actions[selected_action.text()]
            action_func()

        if self.nodeData.outConnections:
            for connection in self.nodeData.outConnections:
                connection.updateValue()
        else:
            self.nodeData.calculate()

    @staticmethod
    def checkSet(value):
        inputString = str(value)
        print(inputString)
        # controlla se inizia con "{" e finisce con "}"
        if inputString.startswith("{") and inputString.endswith("}"):
            # se sì, rimuovi "{" e "}" e splitta la stringa restante sulla base della virgola
            input_set = inputString[1:-1].split(",")
        elif inputString.startswith("[") and inputString.endswith("]"):
            # se sì, rimuovi "[" e "]" e splitta la stringa restante sulla base della virgola
            input_set = inputString[1:-1].split(",")
        else:
            # altrimenti, splitta la stringa sulla base della virgola
            input_set = inputString.split(",")
        # prova a convertire ciascun elemento del set in un numero (intero o decimale)
        try:
            return {int(x) if x.isdigit() else float(x) for x in input_set}
        except ValueError:
            # se non è possibile convertire un elemento in un numero, restituisci il set come set di stringhe
            return {x.strip() for x in input_set}

    def doAdd(self):
        self.removeAllUnnecessaryPlugs()
        self.addInPlug("add")
        self.changeInputValue(1, {})
        self.menuReturnValue = "add"
        self.redesign()

    def doUpdate(self):
        self.removeAllUnnecessaryPlugs()
        self.addInPlug("update")
        self.changeInputValue(1, {})
        self.menuReturnValue = "update"
        self.redesign()

    def doRemove(self):
        self.removeAllUnnecessaryPlugs()
        self.addInPlug("remove")
        self.changeInputValue(1, {})
        self.menuReturnValue = "remove"
        self.redesign()

    def doDiscard(self):
        self.removeAllUnnecessaryPlugs()
        self.addInPlug("discard")
        self.changeInputValue(1, {})
        self.menuReturnValue = "discard"
        self.redesign()

    def doPop(self):
        self.menuReturnValue = "pop"
        value = self.inPlugs[0].getValue()
        valueSet = self.checkSet(value)
        valueSet.pop()
        self.changeInputValue(0, valueSet)

    def doClear(self):
        self.menuReturnValue = "clear"
        value = self.inPlugs[0].getValue()
        valueSet = self.checkSet(value)
        valueSet.clear()

    def doReset(self):
        self.removeAllUnnecessaryPlugs()
        self.menuReturnValue = "reset"
        self.changeInputValue(0, self.startValue)
        self.updateAll()
