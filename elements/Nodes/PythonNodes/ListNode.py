import math
import random
from typing import Union

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface


class ListNode(AbstractNodeInterface):
    _className = "ListNode"
    menuReturnValue = "reset"
    startValue = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    width = 120
    height = 80
    colorTrain = [QColor(219, 255, 190),QColor(226, 190, 255),QColor(226, 190, 255),QColor(190, 252, 255),QColor(255, 155, 127),QColor(127, 227, 255),QColor(127, 227, 255),QColor(163, 255, 127),]

    def __init__(self, value: list[Union[int, float, str]]=None, inNum=1, outNum=1):
        super().__init__(inNum, outNum)
        if value is not None:
            self.startValue = value
        else:
            value = self.startValue
        self.changeInputValue(0, value)
        self.changeSize(self.width, self.height)

    def calculateOutput(self, plugIndex):
        value = self.inPlugs[0].getValue()
        valueList = self.checkList(value)
        result = valueList
        if len(self.inPlugs) > 1:
            if self.menuReturnValue == "append":
                list2 = self.inPlugs[1].getValue()
                if len(list2) > 0:
                    result += list2
            elif self.menuReturnValue == "insert":
                index = self.inPlugs[1].getValue()
                list1 = self.inPlugs[2].getValue()
                if index < len(valueList):
                    try:
                        result = valueList.insert(index, list1)
                    except IndexError:
                        result = "index out of range"
            elif self.menuReturnValue == "remove":
                value = self.inPlugs[1].getValue()
                try:
                    result = valueList.remove(value)
                except ValueError:
                    result = "value not in list"
            elif self.menuReturnValue == "index":
                value = self.inPlugs[1].getValue()
                try:
                    result = valueList[value]
                except IndexError:
                    result = "Out of range"
            elif self.menuReturnValue == "extend":
                list2 = self.inPlugs[1].getValue()
                try:
                    if len(list2) > 0:
                        result.extend(list2)
                except TypeError:
                    result = "list2 is not a list"
        self.outPlugs[plugIndex].setValue(result)
        return self.outPlugs[plugIndex].getValue()

    def redesign(self):
        self.nodeGraphic.redesign(120, 80)

    @staticmethod
    def checkList(value):
        if isinstance(value, list):
            return value
        input_string = value.strip()
        # controlla se inizia con "[" e finisce con "]"
        if input_string.startswith("[") and input_string.endswith("]"):
            # se sì, rimuovi "[" e "]" e splitta la stringa restante sulla base della virgola
            input_list = input_string[1:-1].split(",")
        else:
            # altrimenti, splitta la stringa sulla base della virgola
            input_list = input_string.split(",")
        # prova a convertire ciascun elemento della lista in un numero (intero o decimale)
        try:
            return [int(x) if x.isdigit() else float(x) for x in input_list]
        except ValueError:
            # se non è possibile convertire un elemento in un numero, restituisci la lista come lista di stringhe
            return [x.strip() for x in input_list]

    def showContextMenu(self, position):
        """
        Il nodo deve avere un menu contestuale che permetta come nello stringNode di eseguire operazioni su una lista
        come append, insert, pop, remove, clear, index, sort, shuffle, reverse, extend
        :param position:
        :return:
        """
        contextMenu = QMenu()
        contextMenu.addSection("list")
        actions = {
            "append": self.doAppend,
            "insert": self.doInsert,
            "pop": self.doPop,
            "remove": self.doRemove,
            "clear": self.doClear,
            "index": self.doIndex,
            "sort": self.doSort,
            "shuffle": self.doShuffle,
            "reverse": self.doReverse,
            "extend": self.doExtend,
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

    def doAppend(self):
        self.removeAllUnnecessaryPlugs()
        self.addInPlug("append")
        self.changeInputValue(1, [])
        self.menuReturnValue = "append"
        self.updateAll()
        
    def doInsert(self):
        self.removeAllUnnecessaryPlugs()
        self.addInPlug("index")
        self.addInPlug("insert")
        self.changeInputValue(1, 0)
        self.changeInputValue(2, [])
        self.menuReturnValue = "insert"
        self.updateAll()
        
    def doPop(self):
        self.removeAllUnnecessaryPlugs()
        self.menuReturnValue = "pop"
        value = self.inPlugs[0].getValue()
        if value is None:
            value = []
        valueList = self.checkList(value)
        valueList.pop()
        self.changeInputValue(0, valueList)
        self.updateAll()
        
    def doRemove(self):
        self.removeAllUnnecessaryPlugs()
        self.addInPlug("remove")
        self.changeInputValue(1, [])
        self.menuReturnValue = "remove"
        self.updateAll()
        
    def doClear(self):
        self.removeAllUnnecessaryPlugs()
        self.menuReturnValue = "clear"
        value = self.inPlugs[0].getValue()
        if value is None:
            value = []
        valueList = self.checkList(value)
        valueList.clear()
        self.changeInputValue(0, valueList)
        self.updateAll()
        
    def doIndex(self):
        self.removeAllUnnecessaryPlugs()
        self.addInPlug("index")
        self.changeInputValue(1, 0)
        self.menuReturnValue = "index"
        self.updateAll()
        
    def doSort(self):
        self.removeAllUnnecessaryPlugs()
        self.menuReturnValue = "sort"
        value = self.inPlugs[0].getValue()
        if value is None:
            value = []
        valueList = self.checkList(value)
        valueList.sort()
        self.changeInputValue(0, valueList)
        self.updateAll()
        
    def doShuffle(self):
        self.removeAllUnnecessaryPlugs()
        self.menuReturnValue = "shuffle"
        value = self.inPlugs[0].getValue()
        if value is None:
            value = []
        valueList = self.checkList(value)
        random.shuffle(valueList)
        self.changeInputValue(0, valueList)
        self.updateAll()
        
    def doReverse(self):
        self.removeAllUnnecessaryPlugs()
        self.menuReturnValue = "reverse"
        value = self.inPlugs[0].getValue()
        if value is None:
            value = []
        valueList = self.checkList(value)
        valueList.reverse()
        self.changeInputValue(0, valueList)
        self.updateAll()
        
    def doExtend(self):
        self.removeAllUnnecessaryPlugs()
        self.addInPlug("extend")
        self.changeInputValue(1, [])
        self.menuReturnValue = "extend"
        self.updateAll()
        
    def doReset(self):
        self.removeAllUnnecessaryPlugs()
        self.menuReturnValue = "reset"
        self.changeInputValue(0, self.startValue)
        self.updateAll()

        