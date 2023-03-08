import os

from PyQt5.QtWidgets import *


class PythonNodeMenu(QMenu):
    nodeFolderPath: str = r"/home/tedk/Desktop/python/biggusPy_v1.3/elements/Nodes/PythonNodes"
    creatorString: str = "Created by BiggusPy"

    def __init__(self, mainMenu, mainWindows, parent=None):
        super().__init__(parent)
        self.mainMenu = mainMenu
        self.biggusPy = mainWindows
        self.setTitle('python')
        self.createNodeMenu()

    def createNodeMenu(self):
        """
        ITA:
            Crea il menu dei nodi python
        ENG:
            Create the python nodes menu
        :return:
        """
        self.createNodeList()
        for _node in Nodes:
            _action = QAction(_node, self)
            _action.triggered.connect(self.makeDoNode(_node))
            self.addAction(_action)

    def createNodeList(self):
        """
        ITA:
            Crea la lista dei nodi python
        ENG:
            Create the list of python nodes
        :return:
        """
        global Nodes
        Nodes = []
        for _file in os.listdir(self.nodeFolderPath):
            if _file.endswith('.py'):
                Nodes.append(_file[:-3])

    def updateNodeMenu(self):
        """
        ITA:
            Aggiorna la lista dei nodi python
        ENG:
            Update the list of python nodes
        :return:
        """
        self.clear()
        self.createNodeMenu()

    def doNode(self, nodeName):
        """
        ITA:
            Crea un nodo python
        ENG:
            Create a python node
        :param nodeName:
        :return:
        """
        print(nodeName)
        self.biggusPy.canvas.addNodeFromMenu(self.nodeFolderPath, nodeName)

    def makeDoNode(self, nodeName):
        """
        ITA:
            Crea una funzione che richiama doNode con il nome del nodo specificato come argomento
        ENG:
            Create a function that calls doNode with the specified node name as an argument
        :param nodeName:
        :return:
        """
        return lambda: self.doNode(nodeName)