
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

    def getTitle(self):
        return f"{self.name}_{self.index}"

    def changeValue(self, value, index=0, isAResetValue=False):
        """
        ITA:
            Cambia il valore di un plug di input.
            Questa funzione viene chiamata quando un plug di input viene modificato durante
            l'inizializzazione del nodo o quando un plug di output viene ricalcolato.
        ENG:
            Change the value of an input plug.
            This function is called when an input plug is modified during
            the initialization of the node or when an output plug is recalculated.
        :param value: a value like 10 or "hello"
        :param index: plug index
        :param isAResetValue: This value is used to reset the value of the plug. Comes handy to set a
                                default value for a plug when is created or disconnected.
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
            For every output plug, calculate the return value
        :return:
        """
        for i in range(len(self.outPlugs)):
            self.nodeInterface.calculateOutput(i)

