import importlib
import json
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


class Canvas(QWidget):
    node_name_list = ["NumberNode", "StringNode", "ListNode", "DictionaryNode", "MathNode",
                      "IfNode", "ForNode", "RangeNode", "FunctionNode", "BooleanNode", "WhileNode", "AndNode"]
    mainLayout: QVBoxLayout
    graphicScene: GraphicSceneOverride
    graphicView: QGraphicsView
    width: int = 5000
    height: int = 5000
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
        _addClassNode = contextMenu.addAction("Add Class Node")
        _nodeToCode = contextMenu.addAction("Node To Code")
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
        elif action == _addClassNode:
            rectangle = ResizableRectangle(0, 0, 1000, 1000)
            self.graphicScene.addItem(rectangle)
            rectangle.setPos(self.mapToGlobal(event.pos()))
        elif action == _nodeToCode:
            # test codeToNode
            codeToNode = CodeToNode(self)
            code2 = '''def SieveOfEratosthenes(n):
                        prime_list = []
                        for i in range(2, n+1):
                            if i not in prime_list:
                                print (i)
                                for j in range(i*i, n+1, i):
                                    prime_list.append(j)'''
            code = """a = 30\nb = 20\nc = [1,2,3,4,5,6]"""
            nodeList = codeToNode.createNodeFromCode(code)

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
        :param args:  value, name, inputNumber, outputNumber etc...
        :param kwargs:  value, name, inputNumber, outputNumber etc...
        :return:
        """
        module = importlib.import_module(f"elements.Nodes.PythonNodes.{className}")
        nodeInterface = AbstractNodeInterface()
        nodeClass = getattr(module, className)
        node = nodeClass(*args, **kwargs)
        value = kwargs.get("value", node.startValue)
        if value:
            node.startValue = value

        return node

    def addNode(self, node):
        _node = self.updateTitle(node)
        self.nodesTitleList.append(_node.title)
        self.nodes.append(_node)
        self.graphicScene.addItem(_node.nodeGraphic)

    def addNodeByName(self, name, value=None):
        node = self.createNode(name, value) if value else self.createNode(name)
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
            self.addSerializedNode(node)
        for node in nodes:
            self.deserializeConnections(node)

    def addSerializedNode(self, serializedJsonDictionary, _position=None):
        deserialized = json.loads(serializedJsonDictionary)

        _className = deserialized["className"]
        _title = deserialized["title"]
        _index = deserialized["index"]
        _pos = deserialized["pos"]
        _value = int(deserialized["value"])
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
        else:
            node = self.createNode(_className)

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
