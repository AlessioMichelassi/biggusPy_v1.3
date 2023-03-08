import importlib
import json
import os
from collections import OrderedDict

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from elements.Connections.Connection import Connection
from elements.Nodes.AbstractClass.AbstractNodeGraphicV1_2 import AbstractNodeGraphic
from elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface
from elements.Plugs.PlugGraphic import PlugGraphic
from elements.object.resizableRectangle import ResizableRectangle
from graphicEngine.GraphicSceneOverride import GraphicSceneOverride
from graphicEngine.graphicViewOverride import GraphicViewOverride

from widgets.CodeToNodeWidget.codeToNode import CodeToNode
from widgets.NodeFinderWidget import NodeFinderWidget

code2 = '''
a = 80
def SieveOfEratosthenes(n):
    prime_list = []
    for i in range(2, n+1):
        if i not in prime_list:
            print (i)
            for j in range(i*i, n+1, i):
                prime_list.append(j)'''

codeComplex1 = '''
def printValues(values):
    for node in values:
        print(node)

numberNode = 6
values = [1, 2, 3, 4, 5]
printValues(values)'''

codeComplex2 = """
def add_and_multiply(a, b, c):
    d = a + b
    e = d * c
    return e

x = add_and_multiply(1, 2, 3)
y = add_and_multiply(4, 5, 6)
z = x + y
"""
"""
print(z)
"""


class Canvas(QWidget):
    node_name_list = ["NumberNode", "StringNode", "ListNode", "DictionaryNode", "MathNode",
                      "IfNode", "ForNode", "RangeNode", "FunctionNode", "BooleanNode", "WhileNode", "AndNode", "PrintNode"]
    mainLayout: QVBoxLayout
    graphicScene: GraphicSceneOverride
    graphicView: QGraphicsView
    width: int = 10000
    height: int = 10000
    clipboard = None

    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowFlags())
        self.fileName = "Untitled"
        self.initUI()
        self.nodes = []
        self.nodesTitleList = []
        self.connections = []
        self.clipboard = QApplication.clipboard()

    def initUI(self):
        self.mainLayout = QVBoxLayout()
        self.graphicScene: GraphicSceneOverride = GraphicSceneOverride()
        self.graphicScene.setGraphicSceneSize(self.width, self.height)
        self.graphicView:GraphicViewOverride = GraphicViewOverride(self, self.graphicScene)
        self.mainLayout.addWidget(self.graphicView)
        self.setLayout(self.mainLayout)

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        contextMenu = QMenu(self)
        contextMenu.addSection("Python Nodes")
        actionCenterObject = contextMenu.addAction("Center Object on View")
        _numberNode = contextMenu.addAction("Number Node")
        _stringNode = contextMenu.addAction("String Node")
        _listNode = contextMenu.addAction("List Node")
        _rangeNode = contextMenu.addAction("Range Node")
        _mathNode = contextMenu.addAction("Math Node")
        _ifNode = contextMenu.addAction("If Node")
        _forNode = contextMenu.addAction("For Node")
        _functionNode = contextMenu.addAction("Function Node")
        _booleanNode = contextMenu.addAction("Boolean Node")
        _printNode = contextMenu.addAction("Print Node")
        _addClassNode = contextMenu.addAction("Add Class Node")
        _nodeToCode = contextMenu.addAction("codeToNode")
        _videoPlayer = contextMenu.addAction("Video Player")
        _videoFile = contextMenu.addAction("Video File")
        action = contextMenu.exec(self.mapToGlobal(event.pos()))

        if action == actionCenterObject:
            self.graphicView.selectAllCenterSceneAndDeselect()
        if action == _numberNode:
            self.addNodeByName("NumberNode")
        elif action == _stringNode:
            self.addNodeByName("StringNode")
        elif action == _listNode:
            self.addNodeByName("ListNode")
        elif action == _rangeNode:
            self.addNodeByName("RangeNode")
        elif action == _mathNode:
            self.addNodeByName("MathNode")
        elif action == _ifNode:
            self.addNodeByName("IfNode")
        elif action == _forNode:
            self.addNodeByName("ForNode")
        elif action == _functionNode:
            self.addNodeByName("FunctionNode")
        elif action == _booleanNode:
            self.addNodeByName("BooleanNode")
        elif action == _printNode:
            self.addNodeByName("PrintNode")
        elif action == _videoPlayer:
            node = self.createNodeOther("elements.Nodes.pyqt5Node", "ImageViewerNode")
            self.addNode(node)
        elif action == _videoFile:
            node = self.createNodeOther("elements.Nodes.pyqt5Node", "VideoFileNode")
            self.addNode(node)
        elif action == _addClassNode:
            rectangle = ResizableRectangle(0, 0, 1000, 1000)
            self.graphicScene.addItem(rectangle)
            rectangle.setPos(self.mapToGlobal(event.pos()))
        elif action == _nodeToCode:
            self.createNodeFromCode()

    def __str__(self):
        returnNodes = ""
        for node in self.nodes:
            returnNodes += f"{node}\n"
        return returnNodes

    @staticmethod
    def createNode(className: str, *args, **kwargs):
        # sourcery skip: use-named-expression
        """
        ITA:
            Crea un nodo a partire dal nome della classe ad Es: "NumberNode".
            Il metodo importa il modulo e crea un oggetto della classe passata come parametro,
            quindi ritorna l'interfaccia del nodo. In args e kwargs vanno passati i parametri
            come Value, Name, InputNumber, OutputNumber ecc...
        ENG:
            Create a node from the name of the class, for example "NumberNode".
            The method imports the module and creates an object of the class passed as a parameter,
            then it returns the node interface. In args and kwargs you have to pass the parameters
            as Value, Name, InputNumber, OutputNumber etc ...
        :param className: class name of the node
        :param args:  node, name, inputNumber, outputNumber etc...
        :param kwargs:  node, name, inputNumber, outputNumber etc...
        :return:
        """
        module = None
        nodeClass = None
        try:
            module = importlib.import_module(f"elements.Nodes.PythonNodes.{className}")
        except Exception as e:
            print(f"module not found: {className} not found {e}")
        try:
            if module:
                nodeClass = getattr(module, className)
        except Exception as e:
            print(f"Error in nodeClass: {className} {e}")
            return None
        try:
            if nodeClass:
                node = nodeClass(*args, **kwargs)
                value = kwargs.get("node", node.resetValue)
                if value:
                    node.resetValue = value
                return node
        except Exception as e:
            print(f"Error in createNode: {className} {e}")
            return None

    @staticmethod
    def createNodeOther(path, className: str, *args, **kwargs):
        # sourcery skip: use-named-expression
        """
        ITA:
            Crea un nodo a partire dal nome della classe ad Es: "NumberNode".
            Il metodo importa il modulo e crea un oggetto della classe passata come parametro,
            quindi ritorna l'interfaccia del nodo. In args e kwargs vanno passati i parametri
            come Value, Name, InputNumber, OutputNumber ecc...
        ENG:
            Create a node from the name of the class, for example "NumberNode".
            The method imports the module and creates an object of the class passed as a parameter,
            then it returns the node interface. In args and kwargs you have to pass the parameters
            as Value, Name, InputNumber, OutputNumber etc ...
        :param path:
        :param className: class name of the node
        :param args:  node, name, inputNumber, outputNumber etc...
        :param kwargs:  node, name, inputNumber, outputNumber etc...
        :return:
        """
        module = None
        nodeClass = None
        try:
            module = importlib.import_module(f"{path}.{className}")
        except Exception as e:
            print(f"module not found: {className} not found {e}")
        try:
            if module:
                nodeClass = getattr(module, className)
        except Exception as e:
            print(f"Error in nodeClass: {className} {e}")
            return None
        try:
            if nodeClass:
                node = nodeClass(*args, **kwargs)
                value = kwargs.get("node", node.resetValue)
                if value:
                    node.resetValue = value
                return node
        except Exception as e:
            print(f"Error in createNode: {className} {e}")
            return None

    @staticmethod
    def createNodeFromAbsolutePath(path, className: str, *args, **kwargs):
        # sourcery skip: use-named-expression
        """
        ITA:
            Crea un nodo a partire dal nome della classe ad Es: "NumberNode".
            Il metodo importa il modulo e crea un oggetto della classe passata come parametro,
            quindi ritorna l'interfaccia del nodo. In args e kwargs vanno passati i parametri
            come Value, Name, InputNumber, OutputNumber ecc...
        ENG:
            Create a node from the name of the class, for example "NumberNode".
            The method imports the module and creates an object of the class passed as a parameter,
            then it returns the node interface. In args and kwargs you have to pass the parameters
            as Value, Name, InputNumber, OutputNumber etc ...
        :param path:
        :param className: class name of the node
        :param args:  node, name, inputNumber, outputNumber etc...
        :param kwargs:  node, name, inputNumber, outputNumber etc...
        :return:
        """
        nodes_folder = os.path.abspath(path)
        relative_path = os.path.relpath(nodes_folder, os.getcwd())
        moduleName = f"{relative_path.replace('/', '.')}.{className}"
        module = None
        nodeClass = None
        try:
            module = importlib.import_module(moduleName)
        except Exception as e:
            print(f"module not found: {className} not found {e}")
        try:
            if module:
                nodeClass = getattr(module, className)
        except Exception as e:
            print(f"Error in nodeClass: {className} {e}")
            return None
        try:
            if nodeClass:
                node = nodeClass(*args, **kwargs)
                value = kwargs.get("node", node.resetValue)
                if value:
                    node.resetValue = value
                return node
        except Exception as e:
            print(f"Error in createNode: {className} {e}")
            return None

    def addNodeFromMenu(self, path, className):
        node = self.createNodeFromAbsolutePath(path, className)
        position = self.graphicScene.currentMousePos
        if not position:
            position = self.graphicScene.sceneRect().center()
        if node:
            self.addNode(node)
            node.setPos(position)

    def addNode(self, node):
        _node = self.updateTitle(node)
        _node.updateTitle()
        self.nodesTitleList.append(_node.title)
        self.nodes.append(_node)
        self.graphicScene.addItem(_node.nodeGraphic)

    def addNodeByName(self, name, value=None):
        node = self.createNode(name, value) if value else self.createNode(name)
        if node:
            self.addNode(node)
            node.setPos(self.graphicScene.currentMousePos)

    def createAndReturnNode(self, name, value=None):
        return self.createNode(name, value) if value else self.createNode(name)

    def updateTitle(self, node):
        """
        This method update the title of the node if it is already present in the canvas
        :param node: node to update
        :return:
        """
        while node.title in self.nodesTitleList:
            node.index += 1
        node.updateAll()
        node.canvas = self
        self.nodesTitleList.append(node.title)
        return node

    def addConnection(self, inputNode, inIndex, outputNode, outIndex):
        """
        This method create a connection object in the Canvas and in the scene.
        Is generally called during deserialization
        :param inputNode:
        :param inIndex:
        :param outputNode:
        :param outIndex:
        :return:
        """
        inputNodeData = inputNode.nodeData
        OutputNodeData = outputNode.nodeData

        outputPlug = OutputNodeData.outPlugs[outIndex]
        inputPlug = inputNodeData.inPlugs[inIndex]
        _connection = Connection(OutputNodeData, outputPlug, outputPlug.index, inputNodeData, inputPlug,
                                 inputPlug.index)
        _connection.outputNode.outConnect(_connection)
        _connection.inputNode.inConnect(_connection)
        self.connections.append(_connection)
        self.graphicScene.addItem(_connection)

    def deleteNode(self, node):
        for connection in self.connections:
            if node.nodeData in [connection.outputNode, connection.inputNode]:
                connection.disconnect()
                if connection in self.graphicScene.items():
                    self.graphicScene.removeItem(connection)

        self.nodesTitleList.remove(node.title)
        self.nodes.remove(node)

    def deleteConnection(self, connection):
        connection.disconnect()

    def getNodeByTitle(self, title):
        for node in self.nodes:
            if node.title == title:
                return node
        print(f"node title: {title} not found")
        return None

    def cleanTheScene(self):
        while self.nodes:
            self.deleteNode(self.nodes[0])
        self.graphicScene.clear()

    def copyNode(self, nodes):
        nodesList = []
        for node in nodes:
            nodesList.append(node.serialize())
        self.clipboard.setText(json.dumps(nodesList))

    def pasteNode(self):
        try:
            nodes = self.clipboard.text()
            currentPos = self.graphicScene.currentMousePos
            deserializeNodes = json.loads(nodes)
            for node in deserializeNodes:
                self.addSerializedNode(node, currentPos)
        except Exception as e:
            print(e)

    # ------------------ FROM CODE TO NODE ------------------

    def getNodeByName(self, name):
        """
        ITA:
            E' un metodo pericoloso, se due nodi hanno lo stesso nome, ritorna il primo che trova
            però può essere usato quando si sta facendo il codeToNode e si sa che non ci sono
            due nodi con lo stesso nome oppure ci si riferisce sempre alla stessa variabile.
        ENG:
            It is a dangerous method, if two nodes have the same name, it returns the first one it finds
            but it can be used when doing codeToNode and you know that there are not
            two nodes with the same name or you always refer to the same variable.
        :param name:
        :return:
        """
        for node in self.nodes:
            if node.nodeData.name == name:
                return node
        return None

    def createNodeFromCode(self):
        """
        This method create a list of nodes from a code
        :param code: code to convert
        :return: list of nodes
        """
        codeToNode = CodeToNode(self, self.parent())
        codeToNode.show()

    def createNodeFromCodeToNode(self, className, *args, **kwargs):
        """
        This method create a node from a codeToNode
        :param className: name of the class
        :param args: args of the class
        :param kwargs: kwargs of the class
        :return: node created
        """
        node = self.createNode(className, *args, **kwargs)
        if node:
            self.addNode(node)
            node.setPos(self.graphicScene.currentMousePos)
        return node

    def updateNodePosition(self, node, x, y):
        if node is not None:
            nodeToUpdate = self.getNodeByTitle(node.title)
            nodeToUpdate.setPos(QPointF(x, y))
        else:
            print(f"node {node} not found")

    # ------------------ SERIALIZATION ------------------

    def serialize(self):
        listOfNodeSerialized = []
        for node in self.nodes:
            listOfNodeSerialized.append(node.serialize())
        dicts = OrderedDict([
            ('name', self.fileName),
            ('sceneWidth', self.width),
            ('sceneHeight', self.height),
            ('Nodes', listOfNodeSerialized)])
        return json.dumps(dicts)

    def deserialize(self, serializedString):
        deserialized = json.loads(serializedString)
        self.fileName = deserialized['name']
        self.width = deserialized['sceneWidth']
        self.height = deserialized['sceneHeight']
        nodes = deserialized['Nodes']

        for node in nodes:
            if node is not None:
                self.addSerializedNode(node)
        for node in nodes:
            if node is not None:
                self.deserializeConnections(node)

    def addSerializedNode(self, serializedJsonDictionary, _position=None):
        deserialized = json.loads(serializedJsonDictionary)

        _className = deserialized["className"]
        _name = deserialized["name"]
        _title = deserialized["title"]
        _index = deserialized["index"]
        _pos = deserialized["pos"]
        _value = int(deserialized["node"])
        _inPlugsNumb = deserialized["inPlugsNumb"]
        _outPlugsNumb = deserialized["outPlugsNumb"]
        # se viene specificata la posizione, aumenta la pos corrente
        # del valore specificato
        # è utile quando si fa il paste di un nodo
        if _position:
            pos = QPointF(float(_pos[0] + _position.x()), float(_pos[1] + _position.y()))
        else:
            pos = QPointF(float(_pos[0]), float(_pos[1]))
        if "Number" in _className:
            node = self.createNode(_className, value=_value)
            node.setName(_name)
            node.changeInputValue(0, _value, True)
        else:
            node = self.createNode(_className)
            node.setName(_name)

        self.addNode(node)
        node.setPos(pos)

    def deserializeConnections(self, serializedJsonDictionary):
        deserialized = json.loads(serializedJsonDictionary)
        connections = deserialized["connections"]
        for connection in connections:
            deserializedLine = json.loads(connection)

            inputNodeName = deserializedLine["inputNodeName"]
            inIndex = int(deserializedLine["inputPlug"])
            outputNodeName = deserializedLine["outputNodeName"]
            outIndex = int(deserializedLine["outputPlug"])

            inputNode = self.getNodeByTitle(inputNodeName)
            outputNode = self.getNodeByTitle(outputNodeName)

            if inputNode and outputNode:
                self.addConnection(inputNode, inIndex, outputNode, outIndex)

