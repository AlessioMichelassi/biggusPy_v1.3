from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from graphicEngine.graphicViewOverride import GraphicViewOverride
from scratchNodeV0_9.pixelSmith_GraphicEditor.GraphicEngine.graphicEditorGraphicSceneOverride import graphicEditor_GraphicSceneOverride
from scratchNodeV0_9.pixelSmith_GraphicEditor.Widgets.PropertyEditor.propertyEditor import nodePropertyEditor
from scratchNodeV0_9.pixelSmith_GraphicEditor.Widgets.colorSmith.colorToolsWidget import colorToolsWidget


class pixelSmith(QWidget):
    #
    colorToolWidget: colorToolsWidget
    propertyEditor: nodePropertyEditor

    graphicScene: graphicEditor_GraphicSceneOverride
    graphicView: GraphicViewOverride
    position = QPoint(0, 0)

    # scene variables
    _filename = "untitled"
    sceneWidth = 1000
    sceneHeight = 1000
    node: 'AbstractNodeInterface' = None

    nodeValueChangeForEditor = pyqtSignal(str, str, name="nodeChangeForEditor")
    nodeColorChangeForEditor = pyqtSignal(list, name="nodeColorChangeForEditor")
    nodeLogoChangeForEditor = pyqtSignal(str, bool, bool, name="logoChanged")

    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowFlags(Qt.WindowType.Window))
        graphicLayout = self.initGraphicEditorWidget()
        toolLayout = self.initToolWidget()
        self.initUI([graphicLayout, toolLayout])
        self.initConnection()

    def initUI(self, layouts):
        layout = QHBoxLayout()
        for layout_ in layouts:
            layout.addLayout(layout_)
        self.setLayout(layout)

    def initConnection(self):
        self.colorToolWidget.changeOnColorTrainFormColorTools.connect(self.changeColorTrain)
        self.propertyEditor.valueChangedInPropertyEditor.connect(self.changeNodeValue)
        self.propertyEditor.logoChanged.connect(self.changeNodeLogo)

    def initGraphicEditorWidget(self):
        """
        Crea un layout con un graphicView
        :return:
        """
        self.graphicScene = graphicEditor_GraphicSceneOverride()
        self.graphicView = GraphicViewOverride(None, self.graphicScene)
        self.graphicScene.setGraphicScene(self.sceneWidth, self.sceneHeight)
        layout = QHBoxLayout()
        layout.addWidget(self.graphicView, 1, Qt.AlignmentFlag.AlignLeft)
        return layout

    def initToolWidget(self):
        """
        Crea un layout con i widget di tool
        :return:
        """
        self.colorToolWidget = colorToolsWidget(self)
        self.propertyEditor = nodePropertyEditor(self)
        self.colorToolWidget.setSize(380, None)
        self.propertyEditor.setSize(380, None)
        layout = QVBoxLayout()
        layout.addWidget(self.colorToolWidget, 0, Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.propertyEditor, 0, Qt.AlignmentFlag.AlignHCenter)
        return layout

    def addNodeToScene(self, node: 'AbstractNodeInterface'):
        self.node = node
        self.node.mainWidget = self
        self.node.isEditable = True
        self.graphicScene.addItem(self.node.nodeGraphic)
        self.node.setPos(self.position)
        self.node.setColorTrain(self.colorToolWidget.colorTrainGenerator.colorTrain)
        width = self.node.nodeGraphic.boundingRect().width()
        height = self.node.nodeGraphic.boundingRect().height()
        inputNumber = self.node.inPlugs.__len__()
        outputNumber = self.node.outPlugs.__len__()
        self.propertyEditor.setValue(int(width), int(height), inputNumber, outputNumber)

    def changeNode(self, node: 'AbstractNodeInterface'):
        self.graphicScene.clear()
        self.node = node
        self.node.mainWidget = self
        self.node.isEditable = True
        self.graphicScene.addItem(self.node.nodeGraphic)
        self.node.setPos(self.position)
        self.node.setColorTrain(self.colorToolWidget.colorTrainGenerator.colorTrain)
        width = self.node.nodeGraphic.boundingRect().width()
        height = self.node.nodeGraphic.boundingRect().height()
        inputNumber = self.node.inPlugs.__len__()
        outputNumber = self.node.outPlugs.__len__()
        self.propertyEditor.setValue(int(width), int(height), inputNumber, outputNumber)
        self.node.updateAll()

    def changeColorTrain(self, colorTrain):
        self.node.setColorTrain(colorTrain)
        self.nodeColorChangeForEditor.emit(colorTrain)

    def changeNodeValue(self, _type, value: str):
        """
        Quando vengono cambiate width e height del nodo, viene cambiata la dimensione del nodo
        nella scena e nel codeEditor.
        :param _type:
        :param value:
        :return:
        """
        if _type in ["Width", "Height", "InNumber", "OutNumber"]:
            self.nodeValueChangeForEditor.emit(_type, value)

    def changeNodeLogo(self, value, isLogoVisible, isLogoBandW):
        """
        ITA:
            Quando viene cambiato il logo nella propertyEditor, viene cambiato il logo del nodo
            nella scena e nel codeEditor.
        ENG:
            When the logo is changed in the propertyEditor, the logo of the node is changed
            in the scene and in the codeEditor.
        :param value: logo path
        :param isLogoVisible: hide/show logo
        :param isLogoBandW: set logo in black and white or in color
        :return:
        """
        self.nodeLogoChangeForEditor.emit(value, isLogoVisible, isLogoBandW)

    def changeNodeTitle(self, value):
        """
        Quando viene cambiato il Titolo nella scena viene settato
        anche nel codeEditor.
        :param value:
        :return:
        """
        self.nodeValueChangeForEditor.emit("Title", value)
