import ast
import inspect

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface


class printWidget(QWidget):
    printCanvas: QPlainTextEdit
    lineEdit: QLineEdit

    def __init__(self, node, color: QColor, parent=None):
        super().__init__(parent)
        self.node: PrintNode = node
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.startingColor = color
        self.initWidget()
        self.setStyleX()

    def initWidget(self):
        self.printCanvas = QPlainTextEdit()
        self.lineEdit = QLineEdit()
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.StyledPanel)
        frame.setStyleSheet("background-color: rgb(50, 50, 50);"
                            "border: 1px solid rgb(20, 20, 20);"
                            "border-radius: 5px;")
        frame.setContentsMargins(2, 2, 2, 2)
        frame.setLayout(QVBoxLayout())
        frame.layout().addWidget(self.printCanvas)
        frame.layout().addWidget(self.lineEdit)
        self.layout.addWidget(frame)

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
        self.printCanvas.setStyleSheet(
            f"background-color: \
                                       {backgroundColor} \
                                       color: {textColor}; \
                                       border-style: solid; \
                                       border-radius: 4px; border-width: 1px; \
                                       border-color: {borderColor};"
            f"font-family: Arial;font-style: normal;font-size: 10pt;"
        )

    def setText(self, text):
        self.printCanvas.appendPlainText(str(text))


class PrintNode(AbstractNodeInterface):
    printWidget: printWidget
    resetValue = 0
    width = 300
    height = 300
    colorTrain = [QColor(144, 81, 81), QColor(242, 68, 100), QColor(242, 108, 115), QColor(197, 242, 232),
                  QColor(255, 255, 255), QColor(65, 52, 32), QColor(40, 39, 28), QColor(217, 141, 179), ]

    def __init__(self, value="", inNum=1, outNum=1, parent=None):
        super().__init__(value, inNum, outNum, parent)
        if value is None:
            value = ""
        self.setClassName("PrintNode")
        self.setName("PrintNode")
        self.addPrintWidget()
        self.changeSize(self.width, self.height)
        self.changeInputValue(0, value, True)

    def calculateOutput(self, plugIndex):
        value = self.inPlugs[0].getValue()
        self.outPlugs[plugIndex].setValue(value)
        self.printWidget.setText(str(value))
        return self.outPlugs[plugIndex].getValue()

    def getCode(self):
        inTitle, inCode = self.getCodeFromInput(0)
        return f"{inCode}\nprint({inTitle})"

    def redesign(self):
        self.changeSize(self.width, self.height)

    def showContextMenu(self, position):
        contextMenu = QMenu()
        contextMenu.addSection("PrintNode")

        action = contextMenu.exec(position)

    def addPrintWidget(self):
        self.printWidget = printWidget(self, self.colorTrain[0])
        self.printWidget.setText(self.resetValue)
        self.nodeGraphic.createProxyWidget(self.printWidget)
        self.printWidget.setFixedWidth(self.width - 20)
        self.printWidget.setFixedHeight(self.height - 50)
        self.printWidget.move(int(self.width // 2 - self.printWidget.width() // 2),
                              int(self.height // 2 - self.printWidget.height() // 2) + 20)
