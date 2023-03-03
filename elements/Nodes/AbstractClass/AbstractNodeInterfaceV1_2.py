# -*- coding: utf-8 -*-
from elements.Nodes.AbstractClass.AbstractNodeDataV1_2 import AbstractNodeData
from elements.Nodes.AbstractClass.AbstractNodeGraphicV1_2 import AbstractNodeGraphic
from elements.Plugs.PlugData import PlugData

"""
ITA:
Un nodo è composto da:
- un oggetto che rappresenta il nodo nel grafico
- un oggetto che rappresenta il nodo nel codice
- un'interfaccia che permette di comunicare tra il nodo nel grafico e il nodo nel codice

ENG:
A node consists of:
- an object that represents the node in the graphic
- an object that represents the node in the code
- an interface that allows communication between the node in the graphic and the node in the code

                    nodeInterface
                    |            \
                    |             \
            nodeGraphic         nodeData

ITA:
Di per se un nodo non fa niente di particolare, a parte prendere un valore in ingresso
 e restituirlo in uscita.

Il nodo può essere modificato in modo da fare qualcosa di particolare, per esempio
un nodo che somma due numeri, o un nodo che moltiplica due numeri, o un nodo che
fa una media di due numeri, etc etc.

Per farlo si può creare una classe che eredita abstractNodeInterface, e che implementa
il metodo calculateOutput(plugIndex).

Inoltre è possibile cambiare il numero di Input, il numero di output, il colore del nodo,
la dimensione del nodo, etc etc.

ENG:
In itself a node does nothing special, except take a value as input
and return it as output.

The node can be modified to do something special, for example
a node that adds two numbers, or a node that multiplies two numbers, or a node that
does an average of two numbers, etc etc.

To do this you can create a class that inherits abstractNodeInterface, and that implements
the calculateOutput (plugIndex) method.

In addition, it is possible to change the number of Input, the number of output, the color of the node,
the size of the node, etc etc.
"""


class AbstractNodeInterface:
    colorTrain = []
    isDisabled = False
    contextMenu = None
    resetValue = 0
    isEditable = True
    canvas = None
    mainWidget = None
    _isNodeCreated = False

    def __init__(self, value=220, inNum=1, outNum=1, parent=None):
        self.nodeData = AbstractNodeData("AbstractNodeInterface", self)

        self.nodeGraphic = AbstractNodeGraphic(self)
        self.contextMenu = self.nodeGraphic.contextMenu
        self.createPlug(inNum, outNum)
        self.initGraphics()
        self.nodeData.changeValue(0, value, True)

    @property
    def className(self):
        return self.nodeData.className

    @property
    def index(self):
        return self.nodeData.index

    @index.setter
    def index(self, index):
        self.nodeData.index = index

    # ###############################################
    #
    #      THIS FUNCTION IS FOR GRAPHIC NODES

    @property
    def title(self):
        return self.nodeData.getTitle()

    def initGraphics(self):
        self.nodeGraphic.createTitle()
        self.nodeGraphic.createTxtValue()
        pngFile = "elements/imgs/pythonLogo.png"
        self.nodeGraphic.setLogo(pngFile)
        if self.colorTrain:
            self.setColorTrain(self.colorTrain)

    def setGraphicTitleText(self, title):
        self.nodeGraphic.updateTitle(title)

    def updateTxtTitleFromGraphics(self, title):
        self.nodeData.name = title
        self.nodeData.index = 0
        if self.isEditable:
            self.mainWidget.changeNodeTitle(title)
        if not self.canvas:
            return self.title
        if not self.canvas.getNodeByTitle(self.title):
            self.canvas.nodesTitleList.append(title)
            self.nodeData.index = 0
            return self.title
        node = self.canvas.updateTitle(self)
        return node.title

    def setColorTrain(self, colorTrain):
        self.nodeGraphic.setColorTrain(colorTrain)

    def getColorTrain(self):
        return self.nodeGraphic.getColorTrain()

    def setDisabled(self, isDisabled):
        self.isDisabled = isDisabled

    def getDisabled(self):
        return self.isDisabled

    def setLogo(self, logo):
        self.nodeGraphic.setLogo(logo)

    def changeSize(self, width, height):
        self.nodeGraphic.changeSize(width, height)

    def updateAll(self):
        self.nodeGraphic.updateTitlePosition()
        self.nodeGraphic.updateTxtValuePosition()
        self.nodeGraphic.updatePlugsPos()
        self.nodeGraphic.updateLogoPosition()

    # ###############################################
    #
    #      THIS FUNCTION IS FOR CONNECTIONS
    #

    @property
    def inConnections(self):
        return self.nodeData.inConnections

    @property
    def outConnections(self):
        return self.nodeData.outConnections

    def setName(self, name):
        self.nodeData.name = name

    def setClassName(self, className):
        self.nodeData.className = className
        self.nodeGraphic.updateTitle(className)

    def setPos(self, pos):
        self.nodeGraphic.setPos(pos)

    # ###############################################
    #
    #      THIS FUNCTION IS FOR DATA NODES

    def getOutputValue(self, plugIndex):
        return self.nodeData.outPlugs[plugIndex].getValue()

    def getInputValue(self, plugIndex):
        return self.nodeData.inPlugs[plugIndex].getValue()

    def setInputValue(self, plugIndex, value, isAResetValue=False):
        if isAResetValue:
            self.resetValue = value
        try:
            self.nodeData.inPlugs[plugIndex].setValue(value)
            self.nodeData.calculate()
            if self.outConnections:
                for connection in self.outConnections:
                    connection.updateValue()
            self.nodeGraphic.setTextValueOnQLineEdit(self.getOutputValue(0))
        except Exception as e:
            """print(f"Debug: class AbstractNodeInterface, function setInputValue, error: {e}"
                  f"\nplugIndex: {plugIndex}, value: {value}, isAResetValue: {isAResetValue} ")"""
            a = e

    def calculateOutput(self, plugIndex):
        """
        Override this function to calculate the output value
        :param plugIndex:
        :return:
        """
        return self.nodeData.inPlugs[plugIndex].getValue()

    # ###############################################
    #
    #    Plug functions
    #

    def changeInputValue(self, plugIndex, value, isAResetValue=False):
        """
        ITA:
            Cambia il valore di un plug di input.
            Questa funzione viene chiamata quando un plug di input viene modificato durante
            l'inizializzazione del nodo o quando un plug di output viene ricalcolato.
        ENG:
            Change the value of an input plug.
            This function is called when an input plug is modified during
            the initialization of the node or when an output plug is recalculated.
        :param plugIndex:
        :param value:
        :return:
        """
        self.nodeData.changeValue(plugIndex, value, isAResetValue)
        self.nodeData.calculate()
        if self.outConnections:
            for connection in self.outConnections:
                connection.updateValue()
        self.updateAll()

    @property
    def inPlugs(self):
        return self.nodeData.inPlugs

    @property
    def outPlugs(self):
        return self.nodeData.outPlugs

    def createPlug(self, inNumber, outNumber):
        """
        Create the input and output plugs
        :param inNumber: how many input plugs
        :param outNumber: how many output plugs
        :return:
        """
        for x in range(inNumber):
            plug = PlugData("In", x)
            self.nodeData.inPlugs.append(plug)
            gPlug = plug.createPlugGraphic(self.nodeGraphic)
            self.nodeGraphic.inPlugs.append(gPlug)
        for y in range(outNumber):
            plug = PlugData("Out", y)
            self.nodeData.outPlugs.append(plug)
            gPlug = plug.createPlugGraphic(self.nodeGraphic)
            self.nodeGraphic.outPlugs.append(gPlug)
        self.nodeGraphic.updatePlugsPos()

    def addInPlug(self, plug):
        self.nodeData.inPlugs.append(plug)

    def addOutPlug(self, plug):
        self.nodeData.outPlugs.append(plug)

    def deleteInPlug(self, index):
        if len(self.nodeData.inPlugs) > 1:
            self.nodeData.inPlugs.pop(index)

    def deleteOutPlug(self, index):
        if len(self.nodeData.outPlugs) > 1:
            self.nodeData.outPlugs.pop(index)

    # ###############################################
    #
    #               CONTEXT MENU
    #

    def showContextMenu(self, position):
        """
        Fa l'override del context menu del nodo
        in modo da poterlo personalizzare
        :param position:
        :return:
        """
        self.contextMenu.exec(position)
        print(f"Debug from class {self.className} function showContextMenu {position}")