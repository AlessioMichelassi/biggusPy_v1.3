import ast
import inspect

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from elements.Nodes.AbstractClass.AbstractNodeDataV1_2 import AbstractNodeData
from elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface
from scratchNodeV0_9.ArguePy_CodeEditor.arguePy import ArguePy


class ForBodyWidget(QWidget):
    arguePy: ArguePy
    lineEdit: QLineEdit

    def __init__(self, node, color: QColor, parent=None):
        super().__init__(parent)
        self.node: FunctionNode = node
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.startingColor = color
        self.initWidget()
        self.setStyleX()

    def initWidget(self):
        self.arguePy = ArguePy()
        self.lineEdit = QLineEdit()
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.StyledPanel)
        frame.setStyleSheet("background-color: rgb(50, 50, 50);"
                            "border: 1px solid rgb(20, 20, 20);"
                            "border-radius: 5px;")
        frame.setContentsMargins(2, 2, 2, 2)
        frame.setLayout(QVBoxLayout())
        frame.layout().addWidget(self.arguePy)
        frame.layout().addWidget(self.lineEdit)
        self.layout.addWidget(frame)

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        contextMenu = QMenu(self)
        contextMenu.addSection("ForBody Context Menu")
        _updateFunction = contextMenu.addAction("Update Function")
        contextMenu.addSeparator()

        action = contextMenu.exec(self.mapToGlobal(event.pos()))

        if action == _updateFunction:
            function_string = self.arguePy.getCode()
            self.node.functionString = function_string
            self.node.createFunction(function_string)
            self.node.nodeData.calculate()

    def updateFunctionText(self, value):
        self.arguePy.setCode(str(value))

    def updateResultText(self, value):
        self.lineEdit.setText(str(value))

    def setStyleX(self):
        startColor = self.startingColor.getRgb()
        widgetBackgroundColor = f"rgba({min(150, max(startColor[0] - 60, 20))}, {min(150, max(startColor[1] - 60, 20))}, {min(150, max(startColor[2] - 60, 20))}, 255);"
        backgroundColor = f"rgba({min(255, max(startColor[0] - 40, 20))}, {min(255, max(startColor[1] - 40, 20))}, {min(255, max(startColor[2] - 40, 20))}, 90);"
        borderColor = f"rgba({min(255, max(startColor[0] + 40, 0))}, {min(255, max(startColor[1] + 40, 0))}, {min(255, max(startColor[2] + 40, 0))}, 255);"
        textColor = "white"

        self.setStyleSheet(f"""
            background-color: {widgetBackgroundColor};
            border: 1px solid {borderColor};
            border-radius: 4px; border-width: 1px;
        """)

        self.lineEdit.setStyleSheet(
            f"background-color: \
                                       {backgroundColor} \
                                       color: {textColor}; \
                                       border-style: solid; \
                                       border-radius: 4px; border-width: 1px; \
                                       border-color: {borderColor}"
        )
        self.arguePy.setStyleSheet(
            f"background-color: \
                                       {backgroundColor} \
                                       color: {textColor}; \
                                       border-style: solid; \
                                       border-radius: 4px; border-width: 1px; \
                                       border-color: {borderColor};"
            f"font-family: Arial;font-style: normal;font-size: 10pt;"
        )


class ForBodyNode(AbstractNodeInterface):
    resetValue = lambda x: x
    functionString = resetValue
    menuReturnValue = ""
    function = None
    functionWidget: ForBodyWidget
    isProxied = False
    width = 400
    height = 250
    colorTrain = [QColor(210, 96, 170), QColor(216, 172, 190), QColor(68, 126, 176), QColor(112, 159, 116),
                  QColor(164, 145, 176), QColor(90, 65, 121), QColor(60, 41, 182), QColor(120, 245, 250), ]

    def __init__(self, value: str = None, inNum=1, outNum=1, parent=None):
        super().__init__(value, inNum, outNum, parent)
        self.setClassName("ForBodyNode")
        self.setName("ForBodyNode")
        if value is not None:
            self.functionString = value
        self.function = None
        self.createFunction(self.functionString)
        self.AddFunctionWidget()
        self.changeSize(self.width, self.height)

    def AddFunctionWidget(self):
        self.functionWidget = ForBodyWidget(self, self.colorTrain[0])
        self.functionWidget.updateFunctionText(self.functionString)
        self.nodeGraphic.createProxyWidget(self.functionWidget)
        self.functionWidget.setFixedWidth(self.width - 20)
        self.functionWidget.setFixedHeight(self.height - 50)
        self.functionWidget.move(int(self.width // 2 - self.functionWidget.width() // 2),
                                 int(self.height // 2 - self.functionWidget.height() // 2) + 20)

    def createFunction(self, _functionString):
        try:
            # calculate function
            functionCode = _functionString
            functionGlobals = {}
            exec(functionCode, functionGlobals)
            self.function = functionGlobals["function"]
        except Exception as e:
            print("this function not working for biggus", e)

    def calculateOutput(self, plugIndex):
        if self.function is not None:
            self.outPlugs[plugIndex].setValue(self.function())
        return self.outPlugs[plugIndex].getValue()

    def createProxyWidget(self):
        self.functionWidget = ForBodyWidget(self, self.nodeGraphic.colorFill)
        self.nodeGraphic.setProxyWidget(self.functionWidget)
        self.functionWidget.arguePy.setCode(str(self.functionString))
        width = 400
        height = 250
        self.functionWidget.setFixedWidth(width - 20)
        self.functionWidget.setFixedHeight(height - 50)
        self.functionWidget.move(int(width // 2 - self.functionWidget.width() // 2),
                                 int(height // 2 - self.functionWidget.height() // 2) + 20)


