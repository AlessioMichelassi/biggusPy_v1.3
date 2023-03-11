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
        value0 = self.checkTuple(value)
        returnValue = value0
        if len(self.inPlugs) > 1:
            if self.menuReturnValue == "add":
                value1 = self.checkTuple(self.inPlugs[1].getValue())
                returnValue = tuple(value0) + tuple(value1)
            elif self.menuReturnValue == "remove":
                value1 = self.inPlugs[1].getValue()
                try:
                    returnValue = value0.remove(value1)
                except ValueError:
                    print(f"Value '{value0}' not found.")
            elif self.menuReturnValue == "discard":
                value1 = self.checkTuple(self.inPlugs[1].getValue())
                returnValue = value0.discard(value1)
        elif self.menuReturnValue == "pop":
            returnValue = value0.pop()
        elif self.menuReturnValue == "clear":
            returnValue = value0.clear()
        elif self.menuReturnValue == "reset":
            returnValue = self.startValue
        self.outPlugs[0].setValue(returnValue)
        return self.outPlugs[0].getValue()

    def getCode(self):
        if not self.inConnections:
            return f'{self.getTitle()} = {self.inPlugs[0].getValue()}'
        if self.menuReturnValue == "add":
            return self.returnAddCode()
        elif self.menuReturnValue == "update":
            return self.returnUpdateCode()
        elif self.menuReturnValue == "remove":
            return self.returnRemoveCode()
        elif self.menuReturnValue == "discard":
            return self.returnDiscardCode()
        elif self.menuReturnValue == "pop":
            return self.returnPopCode()
        elif self.menuReturnValue == "clear":
            return self.returnClearCode()
        elif self.menuReturnValue == "reset":
            return f'{self.getTitle()} = {self.inPlugs[0].getValue()}'

    def redesign(self):
        self.changeSize(self.width, self.height)

    def checkTuple(self, value):
        inputString = str(value)
        if inputString.startswith("(") and inputString.endswith(")"):
            inputString = inputString[1:-1]

        input_Tuple = inputString.split(",")
        try:
            return {int(x) if x.isdigit() else float(x) for x in input_Tuple}
        except ValueError:
            # se non è possibile convertire un elemento in un numero, restituisci il set come set di stringhe
            return {x.strip() for x in input_Tuple}

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
            self.menuReturnValue = selected_action.text()
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

    def returnAddCode(self):
        in0Title, in0Code = self.getCodeFromInput(0)
        in1Title, in1Code = self.getCodeFromInput(1)
        concat = f'{in0Code}\n{in1Code}\n'
        returnCode = f"try:\n\t{in0Title}.add({in1Title})\nexcept TypeError:\n\tprint('node must be " \
                     f"hashable')\nexcept KeyError:\n\tprint('node already in set')"
        return concat + returnCode

    def doUpdate(self):
        self.removeAllUnnecessaryPlugs()
        self.menuReturnValue = "update"
        self.addInPlug("update")
        self.changeInputValue(0, {})
        self.redesign()

    def returnUpdateCode(self):
        in0Title, in0Code = self.getCodeFromInput(0)
        in1Title, in1Code = self.getCodeFromInput(1)
        concat = f'{in0Code}\n{in1Code}\n'
        returnCode = f"try:\n\t{in0Title}.update({in1Title})\nexcept TypeError:\n\tprint('node must be hashable')\nexcept KeyError:\n\tprint('node already in set')"
        return concat + returnCode

    def doRemove(self):
        self.removeAllUnnecessaryPlugs()
        self.menuReturnValue = "remove"
        self.addInPlug("remove")
        self.changeInputValue(0, {})
        self.redesign()

    def returnRemoveCode(self):
        in0Title, in0Code = self.getCodeFromInput(0)
        in1Title, in1Code = self.getCodeFromInput(1)
        concat = f'{in0Code}\n{in1Code}\n'
        returnCode = f"try:\n\t{in0Title}.remove({in1Title})\nexcept TypeError:\n\tprint('node must be " \
                     f"hashable')\nexcept KeyError:\n\tprint('node not in set')"
        return concat + returnCode

    def doDiscard(self):
        self.removeAllUnnecessaryPlugs()
        self.menuReturnValue = "discard"
        self.addInPlug("discard")
        self.changeInputValue(0, {})
        self.redesign()

    def returnDiscardCode(self):
        in0Title, in0Code = self.getCodeFromInput(0)
        in1Title, in1Code = self.getCodeFromInput(1)
        concat = f'{in0Code}\n{in1Code}\n'
        returnCode = f"try:\n\t{in0Title}.discard({in1Title})\nexcept TypeError:\n\tprint('node must be " \
                     f"hashable')\nexcept KeyError:\n\tprint('node not in set')"
        return concat + returnCode

    def doPop(self):
        self.removeAllUnnecessaryPlugs()
        self.menuReturnValue = "pop"
        value = self.inPlugs[0].getValue()
        valueSet = self.checkTuple(value)
        result = valueSet[:-1]
        self.changeInputValue(0, result)
        self.redesign()

    def returnPopCode(self):
        in0Title, in0Code = self.getCodeFromInput(0)
        returnCode = f"try:\n\t{in0Title}.pop()\nexcept TypeError:\n\tprint('node must be hashable')\nexcept " \
                     f"KeyError:\n\tprint('node not in set')"
        return in0Code + returnCode

    def doClear(self):
        self.removeAllUnnecessaryPlugs()
        self.menuReturnValue = "clear"
        self.changeInputValue(0, {})
        self.redesign()

    def returnClearCode(self):
        in0Title, in0Code = self.getCodeFromInput(0)
        returnCode = f"try:\n\t{in0Title}.clear()\nexcept TypeError:\n\tprint('node must be hashable')\nexcept " \
                     f"KeyError:\n\tprint('node not in set')"
        return in0Code + returnCode

    def doReset(self):
        self.removeAllUnnecessaryPlugs()
        self.menuReturnValue = "reset"
        self.changeInputValue(0, self.startValue)
        self.redesign()



