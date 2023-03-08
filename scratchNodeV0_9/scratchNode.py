import importlib
import os
import re
import sys
import types

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface
from scratchNodeV0_9.pixelSmith_GraphicEditor.CommonMenu.graphicEditorMenuBar import MenuBar

from scratchNodeV0_9.pixelSmith_GraphicEditor.pixelSmith import pixelSmith
from scratchNodeV0_9.ArguePy_CodeEditor.arguePy import ArguePy

"""
QMainWindow for pixelSmith
"""


class scratchNodeV0_9(QMainWindow):
    menu: MenuBar

    # variable for code Editor
    codeEditor: ArguePy
    dockCodeEditor: QDockWidget

    # variable for graphic Editor
    graphicEditor: pixelSmith
    dockGraphicEditor: QDockWidget

    node: AbstractNodeInterface = None
    valueChangedFromGraphicEditor = pyqtSignal(str, str, name="valueChangedFromGraphicEditor")
    fileName = None

    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowFlags(Qt.WindowType.Window))
        self.initUI()
        self.initGeometry()
        self.initStatusBar()
        self.initDockWidget()
        # self.loadSettings()
        self.initStatusBar()
        self.initConnections()
        self.loadUntitledNode()

    def closeEvent(self, event):
        self.saveSettings()
        event.accept()

    # ################################################
    #
    #       INIT MAIN WINDOWS
    #
    #

    def initUI(self):
        self.menu = MenuBar(self)
        self.setMenuBar(self.menu)

    def initGeometry(self):
        self.setWindowTitle("ScratchO!")
        self.setContentsMargins(10, 10, 10, 10)

    def initStatusBar(self):
        self.statusBar().showMessage("Ready")

    def initDockWidget(self):
        self.initDockForGraphicEditor()
        self.initDockForCodeEditor()
        self.resizeDocks([self.dockGraphicEditor, self.dockCodeEditor], [300, 300], Qt.Orientation.Horizontal)

    def initDockForGraphicEditor(self):
        self.graphicEditor = pixelSmith(self)
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.StyledPanel)
        frame.setStyleSheet("background-color: rgb(50, 50, 50);" 
                            "border: 1px solid rgb(20, 20, 20);" 
                            "border-radius: 5px;")

        frame.setContentsMargins(10, 10, 5, 10)
        frame.setLayout(QVBoxLayout())
        frame.layout().addWidget(self.graphicEditor)
        self.dockGraphicEditor = QDockWidget("", self)
        self.dockGraphicEditor.setObjectName("dockGraphicEditor")
        self.dockGraphicEditor.setWidget(frame)
        self.dockGraphicEditor.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable |
                                           QDockWidget.DockWidgetFeature.DockWidgetFloatable)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dockGraphicEditor)

    def initDockForCodeEditor(self):
        self.codeEditor = ArguePy(self)
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.StyledPanel)
        frame.setStyleSheet("background-color: rgb(50, 50, 50);" 
                            "border: 1px solid rgb(20, 20, 20);" 
                            "border-radius: 5px;")
        frame.setContentsMargins(20, 10, 5, 10)
        frame.setLayout(QVBoxLayout())
        frame.layout().addWidget(self.codeEditor)
        self.dockCodeEditor = QDockWidget("", self)
        self.dockCodeEditor.setWidget(frame)
        self.dockCodeEditor.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable
                                        | QDockWidget.DockWidgetFeature.DockWidgetFloatable)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dockCodeEditor)

    def initConnections(self):
        self.graphicEditor.nodeValueChangeForEditor.connect(self.onNodeChangeForEditor)
        self.graphicEditor.nodeLogoChangeForEditor.connect(self.onNodeLogoChangeForEditor)
        self.graphicEditor.nodeColorChangeForEditor.connect(self.onNodeColorChangeForEditor)

    # ################################################
    #
    #       LOAD/SAVE SETTINGS
    #
    #

    def loadSettings(self):
        pass

    def saveSettings(self):
        pass

    # ################################################
    #
    #       NEW/LOAD/SAVE NODE
    #
    #

    def newNode(self):
        self.graphicEditor.graphicScene.clear()
        self.loadUntitledNode()

    def loadUntitledNode(self):
        """
        ITA:
            Carica nel ArguePy_CodeEditor il codice del nodo vuoto e nell'editor grafico il nodo vuoto
        ENG:
            Load in ArguePy_CodeEditor the code of the empty node and in the graphic editor the empty node
        :return:
        """
        # controlla che il file esista:
        filepath = r"/biggusFolder/biggusCode/ImageCvNode.py"
        # cerca il file nella cartella da cui è stato lanciato lo script
        if not os.path.exists(filepath):
            print("file not found")
            return
        else:
            with open(filepath, "r") as f:
                code = f.read()
                self.codeEditor.codeEditor.setPlainText(code)
                mod = types.ModuleType("DefaultNode")
                exec(code, mod.__dict__)
                self.node = self.createNode("DefaultNode", mod, value=10)
                self.addNode(self.node)

    def openFile(self):
        """
        ITA:
            Carica nel ArguePy_CodeEditor il codice del nodo e nell'editor grafico il nodo.
        ENG:
            Load in ArguePy_CodeEditor the code of the node and in the graphic editor the node.
        :param node:
        :return:
        """
        loadDialog = QFileDialog(self)
        loadDialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        loadDialog.setNameFilter("Python Files (*.py)")
        loadDialog.setViewMode(QFileDialog.ViewMode.Detail)
        if loadDialog.exec():
            fileName = loadDialog.selectedFiles()[0]
            with open(fileName, "r") as f:
                self.createNodeFromExternalCode(f)

    def saveFile(self):
        if self.fileName is None:
            self.saveFileAs()
        else:
            with open(self.fileName, "w") as f:
                f.write(self.codeEditor.codeEditor.toPlainText())

    def saveFileAs(self):
        """
        ITA:
            Salva il nodo con un nome scelto dall'utente
        ENG:
            Save the node with a name chosen by the user
        :return:
        """
        saveDialog = QFileDialog(self)
        saveDialog.setFileMode(QFileDialog.FileMode.AnyFile)
        saveDialog.setNameFilter("Python Files (*.py)")
        saveDialog.setViewMode(QFileDialog.ViewMode.Detail)
        if saveDialog.exec():
            self.fileName = saveDialog.selectedFiles()[0]
            with open(self.fileName, "w") as f:
                f.write(self.codeEditor.codeEditor.toPlainText())

    # ################################################
    #
    #       NODES
    #
    #

    @staticmethod
    def createNode(className: str, mod, *args, **kwargs):
        """
        Crea un nodo a partire dal nome della classe e dal modulo
        :param className: In questo caso sarà sempre "DefaultNode"
        :param mod: mod invece è il modulo creato con exec che controlla che il codice sia corretto
        :param args: in args ci sono i parametri del costruttore tipo node=10
        :param kwargs: in kwargs ci sono i parametri del costruttore tipo node=10
        :return: l'oggetto nodo
        """
        nodeClass = getattr(mod, className)
        return nodeClass(*args, **kwargs)

    def createNodeFromExternalCode(self, f):
        """
        ITA:
            Crea un nodo a partire dal codice esterno
        ENG:
            Create a node from external code
        :param f:
        :return:
        """
        code = f.read()
        fileName = f.name
        # va cercare nel codice il nome del modulo che si trova fra class e (AbstractNodeInterface):
        # class DefaultNode(AbstractNodeInterface):
        #   ...
        moduleName = code.split("class ")[1].split("(")[0]
        # className invece è self.setClassName("DefaultNode")
        className = code.split("self.setClassName(\"")[1].split("\")")[0]
        self.codeEditor.codeEditor.clear()
        self.codeEditor.codeEditor.setPlainText(code)
        try:
            mod = types.ModuleType(moduleName)
            exec(code, mod.__dict__)
            self.node = self.createNode(className, mod, value=10)
            self.addNode(self.node)
        except Exception as e:
            print(e)

    def addNode(self, node):
        """
        Aggiunge il nodo all'editor grafico
        :param node:
        :return:
        """
        self.graphicEditor.addNodeToScene(node)
        self.graphicEditor.graphicView.selectAllCenterSceneAndDeselect()

    def updateNodeFromText(self):
        """
        ITA:
            Se il codice nel codeEditor è stato modificato, questo metodo aggiorna il nodo
            nel graphicEditor
        ENG:
            If the code in the codeEditor has been modified, this method updates the node
            in the graphicEditor
        :return:
        """
        code = self.codeEditor.codeEditor.toPlainText()
        mod = types.ModuleType("DefaultNode")
        try:
            exec(code, mod.__dict__)
            node = self.createNode("DefaultNode", mod, value=10)
            self.graphicEditor.changeNode(node)
            self.graphicEditor.graphicView.selectAllCenterSceneAndDeselect()
        except Exception as e:
            print("WARNING CANNOT UPDATE NODE FROM TEXT")
            print(e)
            return


    # ################################################
    #
    #         THIS PART IS FOR UPDATE NODE
    #             FROM GRAPHIC EDITOR
    #               TO CODE EDITOR
    #                AND VICEVERSA
    #
    #

    oldWidthString = None
    oldHeightString = None
    oldInputNumberString = None
    oldOutputNumberString = None
    oldTitleNumberString = None

    replaceWithCount = 0
    replaceHeightCount = 0
    replaceInputCount = 0
    replaceOutputCount = 0
    replaceTitleCount = 0

    def onNodeChangeForEditor(self, _type, value):
        """
        ITA:
            Nel graphicEditor è possibile variare l'aspetto del nodo, in particolare
            le dimensioni (Width, Height), in numero di input e output, il colore delle varie parti
            etc ect. Quando uno di questi parametri cambia nel graphicEditor viene emesso un segnale
            che viene catturato da questa funzione.
            il segnale è del tipo: _type, node
            dove _type è il tipo può essere Widht, Height, InputNumber, OutputNumber, ColorTrain
            e node è il valore del parametro.

        ENG:
            In the graphicEditor it is possible to change the appearance of the node, in particular
            the dimensions (Width, Height), the number of inputs and outputs, the color of the various parts
            etc etc. When one of these parameters changes in the graphicEditor a signal is emitted
            that is captured by this function.
            the signal is of the type: _type, node
            where _type is the type can be Widht, Height, InputNumber, OutputNumber, ColorTrain
            and node is the node of the parameter.

        ITA:
            Una volta intercettato il segnale, viene aggiornato il codice del nodo nel codeEditor.
            quindi se type è width e node è 100, il codice del nodo sarà aggiornato:

        ENG:
            Once the signal is intercepted, the code of the node in the codeEditor is updated.
            so if type is width and node is 100, the node code will be updated:

        class UntitledNode(AbstractNodeData):

            _className = "UntitledNode"
            resetValue = 0
            width = 50 <--- aggiornato il valore
            height = 50 <--- aggiornato il valore
            colorTrain = [] <--- aggiornato il valore

            def __init__(self, node, inNum=1, outNum=1): <--- aggiornato il valore inNum e outNum
                super().__init__(inNum, outNum)
                self.resetValue = node
                self.changeValue(node, type(node), 0, True)

        :return:
        """
        code = self.codeEditor.getCode()
        # print(f"Debuf from class {self.__class__.__name__} {_type} {node} ")
        if _type == "Width":
            pattern = r"width = \d+"
            self.seekAndReplace(pattern, "width", self.oldWidthString, self.replaceWithCount, value)
        elif _type == "Height":
            pattern = r"height = \d+"
            self.seekAndReplace(pattern, "height", self.oldHeightString, self.replaceHeightCount, value)
        elif _type == "InNumber":
            # inNum è asll'interno dell'init
            pattern = r"inNum=\d+"
            self.seekAndReplace(pattern, "inNum", self.oldInputNumberString, self.replaceInputCount, value)
        elif _type == "OutNumber":
            pattern = r"outNum=\d+"
            self.seekAndReplace(pattern, "outNum", self.oldOutputNumberString, self.replaceOutputCount, value)
        elif _type == "ColorTrain":
            pass
        elif _type == "Title":
            # self.setName("DefaultNode")
            # quando cambia il titolo vie rimpiazzata la scritta fra virgolette in setName
            pattern = r"setName\(\".*\"\)"
            self.seekAndSet(pattern, "setName", self.oldTitleNumberString, self.replaceTitleCount, value)
        self.updateNodeFromText()

    def seekAndReplace(self, pattern, string, oldStringReference, replaceVarReference, value):
        # sourcery skip: use-named-expression
        """
        ITA:
            SeekAndReplace cerca la stringa tipo width = oldValue e la sostituisce con width = newValue.
            Per farlo usa la regex pattern, che è una stringa che contiene la regex da cercare. Se la regex
            non viene trovata viene lanciata un'eccezione. Se la regex viene trovata, viene sostituita
            la stringa con la nuova stringa. La nuova stringa è formata da string, che è il nome della variabile
            e node, che è il valore della variabile. Se la stringa è inNum o outNum, la stringa non viene
            formattata con gli spazi prima e dopo il =. Se invece la stringa non è inNum o outNum, la stringa
            viene formattata con gli spazi prima e dopo il =.

        ENG:
            SeekAndReplace seeks the string type width = oldValue and replaces it with width = newValue.
            To do this it uses the regex pattern, which is a string that contains the regex to search for. If the regex
            is not found an exception is raised. If the regex is found, the string is replaced
            the string with the new string. The new string is formed by string, which is the name of the variable
            and node, which is the node of the variable. If the string is inNum or outNum, the string is not
            formatted with spaces before and after the =. If the string is not inNum or outNum, the string
            is formatted with spaces before and after the =.

        :return:
        """
        code = self.codeEditor.getCode()
        # Cerca la stringa di width solo se è la prima volta che viene effettuata la sostituzione
        if replaceVarReference == 0:
            match = re.search(pattern, code)
            if match:
                oldStringReference = match.group()
            else:
                raise ValueError(f"Cannot find '{pattern}' in node code")
        # Sostituisci la stringa di width solo se è stata trovata la stringa originale
        if oldStringReference:
            if "inNum" in string or "outNum" in string:
                newWidthString = f"{string}={value}"
            else:
                newWidthString = f"{string} = {value}"
            code = code.replace(oldStringReference, newWidthString, 1)
            replaceVarReference += 1
            oldStringReference = newWidthString
            self.codeEditor.setCode(code)

    def seekAndSet(self, pattern, string, oldStringReference, replaceVarReference, value):
        # sourcery skip: use-named-expression
        """
        ITA:
            SeekAndSet funziona come SeekAndReplace, ma la stringa da cercare è del tipo: setName("DefaultNode")
        ENG:
            SeekAndSet works like SeekAndReplace, but the string to search for is of the type: setName("DefaultNode")

        """
        code = self.codeEditor.getCode()
        # Cerca la stringa di width solo se è la prima volta che viene effettuata la sostituzione
        if replaceVarReference == 0:
            match = re.search(pattern, code)
            if match:
                oldStringReference = match.group()
            else:
                raise ValueError(f"Cannot find '{pattern}' in node code")
        # Sostituisci la stringa di width solo se è stata trovata la stringa originale
        # non vengono messe le virgolette!
        if oldStringReference:
            if "\"" in oldStringReference:
                newWidthString = f"{string}(\"{value}\")"
            else:
                newWidthString = f"{string}({value})"
            code = code.replace(oldStringReference, newWidthString, 1)
            replaceVarReference += 1
            oldStringReference = newWidthString
            self.codeEditor.setCode(code)

    oldColorTrainString = None
    replaceColorTrainCount = 0

    def onNodeColorChangeForEditor(self, colorList):
        """
        ITA:
            Questo metodo viene chiamato quando vengono cambiati i colori nel colorTool
            viene aggiornato il codice del nodo come avviene per width e height etc.
            nel codice viene cambiata la riga che contiene colorTrain = [] con la nuova lista di colori

        ENG:
            This method is called when the node color is changed in the property editor.
        :param colorList:
        :return:
        """
        pattern = r"colorTrain = \[.*\]"
        self.seekAndReplaceForColorTrain(pattern, "colorTrain", self.oldColorTrainString, self.replaceColorTrainCount,
                                         colorList)

    def seekAndReplaceForColorTrain(self, pattern, string, oldStringReference, replaceVarReference, colorList):
        # sourcery skip: use-named-expression
        """
        ITA:
            SeekAndSet funziona come SeekAndReplace, ma la stringa da cercare è del tipo: colorTrain = []
        ENG:
            SeekAndSet works like SeekAndReplace, but the string to search for is of the type: colorTrain = []

        """
        colorString = ""
        for value in colorList:
            colorString += f"QColor({value.red()}, {value.green()}, {value.blue()}),"
        code = self.codeEditor.getCode()
        # Cerca la stringa di width solo se è la prima volta che viene effettuata la sostituzione
        if replaceVarReference == 0:
            match = re.search(pattern, code)
            if match:
                oldStringReference = match.group()
            else:
                raise ValueError(f"Cannot find '{pattern}' in node code")
        # Sostituisci la stringa di width solo se è stata trovata la stringa originale
        # non vengono messe le virgolette!
        if oldStringReference:
            newWidthString = f"{string} = [{colorString}]"
            code = code.replace(oldStringReference, newWidthString, 1)
            replaceVarReference += 1
            oldStringReference = newWidthString
            self.codeEditor.setCode(code)

    def onNodeLogoChangeForEditor(self, path, isLogoVidible, isLogoBandW):
        """
        ITA:
            Questo metodo viene chiamato quando viene cambiato il logo del nodo nella property editor.
            Il logo può essere visibile/invisibile, a colori/monocromatico.
        ENG:
            This method is called when the node logo is changed in the property editor.
            The logo can be visible / invisible, in color / monochrome.
        :param path:
        :param isLogoVidible:
        :param isLogoBandW:
        :return:
        """
        self.node.nodeGraphic.setLogoVisible(isLogoVidible)
        self.node.nodeGraphic.setLogoBW(isLogoBandW)
        self.node.nodeGraphic.setLogo(path)
