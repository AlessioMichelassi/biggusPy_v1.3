# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class AbstractNodeData:
    className = "newAbstractNode"
    name: str
    index: int = 0
    isDisabled = False
    isNodeCreated: bool = False

    def __init__(self, className: str = None, nodeInterface=None):
        self.name = className
        self.className = className
        self.nodeGraphic = None
        self.nodeInterface = nodeInterface
        self.inPlugs = []
        self.outPlugs = []
        self.outConnections = []
        self.inConnections = None
        self.isNodeCreated = True

    def __str__(self):
        returnPlugs = ""

        for plug in self.inPlugs:
            returnPlugs += f"{plug.getTitle()} = {plug.getValue()} - "
        for plug in self.outPlugs:
            returnPlugs += f"{plug.getTitle()} = {plug.getValue()} -"

        returnConnectionString = ""
        for connection in self.outConnections:
            returnConnectionString += f"{connection} - "
        return f"className: {self.className}\n\tName: {self.name}\n\tTitle: {self.getTitle()}\n\tplugs: {returnPlugs}" \
               f"\n\t{returnConnectionString}"

    def getTitle(self):
        return f"{self.name}_{self.index}"

    def deleteInPlug(self, index):
        try:
            self.inPlugs.pop(index)
        except IndexError:
            print("Warning from AbstractNodeData.deleteInPlug: index out of range")

    def changeValue(self, index=0, value=1, isAResetValue=False):
        """
        ITA:
            Cambia il valore di un plug di input.
            Questa funzione viene chiamata quando un plug di input viene modificato durante
            l'inizializzazione del nodo o quando un plug di output viene ricalcolato.
        ENG:
            Change the node of an input plug.
            This function is called when an input plug is modified during
            the initialization of the node or when an output plug is recalculated.
        :param value: a node like 10 or "hello"
        :param index: plug index
        :param isAResetValue: This node is used to reset the node of the plug. Comes handy to set a
                                default node for a plug when is created or disconnected.
        :return:
        """
        if isAResetValue:
            self.inPlugs[index].resetValue = value
        self.inPlugs[index].setValue(value)
        self.calculate()
        if self.outConnections:
            for connection in self.outConnections:
                connection.updateValue()

    def calculate(self):
        """
            For every output plug, calculate the return node
        :return:
        """
        for i in range(len(self.outPlugs)):
            self.nodeInterface.calculateOutput(i)

    def checkInput(self, _type):
        """
        Check if the input is All of correct type
        :param _type:
        :return:
        """
        valueReturn = []
        for plug in self.inPlugs:
            if plug.getValue() is None:
                return False
            if type(plug.getValue()) == _type:
                valueReturn.append(True)
            else:
                valueReturn.append(False)
        return False not in valueReturn

    def outConnect(self, connection):
        self.outConnections.append(connection)
        for _connection in self.outConnections:
            _connection.updateValue()

    def inConnect(self, connection):
        inPlug = connection.inputPlug
        for plug in self.inPlugs:
            if plug.index == inPlug.index:
                plug.inConnection = connection

    def disconnect(self, node, nodePlugIndex):
        """
        Disconnect the node from the plug
        :param node: the node to disconnect
        :param nodePlugIndex: the index of the plug to disconnect
        :return:
        """
        self.calculate()
        node.inPlugs[nodePlugIndex].resetPlug()
        node.calculate()