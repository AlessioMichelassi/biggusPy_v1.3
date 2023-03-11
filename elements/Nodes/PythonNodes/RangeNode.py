from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface


class RangeNodeUI(QWidget):
    lneStart: QLineEdit
    lneEnd: QLineEdit
    lneStep: QLineEdit

    def __init__(self, node, parent=None):
        super(RangeNodeUI, self).__init__(parent)
        self.node = node
        self.initUI()
        self.initWidget()
        self.initConnection()
        self.initStyleSheet()

    def initUI(self):
        self.lneStart = QLineEdit()
        self.lneStart.setValidator(QIntValidator())
        self.lneEnd = QLineEdit()
        self.lneEnd.setValidator(QIntValidator())
        self.lneStep = QLineEdit()
        self.lneStep.setValidator(QIntValidator())

    def initWidget(self):
        layout = QVBoxLayout(self)
        lblStart = QLabel("Start:")
        startLayout = QHBoxLayout()
        startLayout.addWidget(lblStart, 0, Qt.AlignLeft)
        startLayout.addWidget(self.lneStart, 0, Qt.AlignRight)

        lblEnd = QLabel("End:")
        endLayout = QHBoxLayout()
        endLayout.addWidget(lblEnd, 0, Qt.AlignLeft)
        endLayout.addWidget(self.lneEnd, 0, Qt.AlignRight)

        lblStep = QLabel("Step:")
        stepLayout = QHBoxLayout()
        stepLayout.addWidget(lblStep, 0, Qt.AlignLeft)
        stepLayout.addWidget(self.lneStep, 0, Qt.AlignRight)

        layout.addLayout(startLayout)
        layout.addLayout(endLayout)
        layout.addLayout(stepLayout)

    def initConnection(self):
        self.lneStart.returnPressed.connect(self.onStartTextChanged)
        self.lneEnd.returnPressed.connect(self.onEndTextChanged)
        self.lneStep.returnPressed.connect(self.onStepTextChanged)

    def initStyleSheet(self):
        backgroundColor = self.node.colorTrain[6].darker(250)
        backGroundText = self.node.colorTrain[6].darker(200)
        textColor = self.node.colorTrain[5]
        borderColor = self.node.colorTrain[7]
        style = f"""
        QWidget {{
            background-color: rgba({backgroundColor.red()}, {backgroundColor.green()}, {backgroundColor.blue()}, 255);
        }}
        QLineEdit {{
            background-color: rgba({backGroundText.red()}, {backGroundText.green()}, {backGroundText.blue()}, 200);
            border: 1px solid rgb({borderColor.red()}, {borderColor.green()}, {borderColor.blue()});
            border-radius: 3px;
            color: rgba({textColor.red()}, {textColor.green()}, {textColor.blue()}, 255);
            font-size: 9px;
            font-family: Noto Sans;
        }}
        QLabel {{
            font-size: 9px;
            font-family: Noto Sans;
            color: rgba({textColor.red()}, {textColor.green()}, {textColor.blue()}, 255);
        }}
    """
        self.setStyleSheet(style)

    def onStartTextChanged(self):
        start = int(self.lneStart.text())
        self.node.changeInputValue(0, start, True)

    def onEndTextChanged(self):
        end = int(self.lneEnd.text())
        self.node.changeInputValue(1, end, True)

    def onStepTextChanged(self):
        step = int(self.lneStep.text())
        self.node.changeInputValue(2, step, True)


class RangeNode(AbstractNodeInterface):
    resetValue = 0
    startValue = True
    width = 120
    height = 180
    colorTrain = [QColor(87, 255, 157), QColor(255, 87, 185), QColor(255, 138, 206), QColor(255, 214, 238),
                  QColor(157, 87, 255), QColor(58, 170, 105), QColor(255, 87, 185), QColor(255, 138, 206),
                  QColor(255, 214, 238)]
    proxyWidget: RangeNodeUI

    def __init__(self, start: int = 0, value: int = 10, step: int = 1, inNum=3, outNum=1, parent=None):
        super().__init__(value, inNum, outNum, parent)
        self.setClassName("RangeNode")
        self.setName("RangeNode")
        self.changeSize(self.width, self.height)
        self.changeInputValue(0, start, True)
        self.changeInputValue(1, value, True)
        self.changeInputValue(2, step, True)
        self.setPlugInTitle(0, "start")
        self.setPlugInTitle(1, "end")
        self.setPlugInTitle(2, "step")
        self.AddProxyWidget()

    def calculateOutput(self, plugIndex):
        start = self.inPlugs[0].getValue()
        end = self.inPlugs[1].getValue()
        step = self.inPlugs[2].getValue()
        try:
            value = range(start, end, step)
        except ValueError:
            value = []
        self.outPlugs[plugIndex].setValue(value)
        return self.outPlugs[plugIndex].getValue()

    def getCode(self):
        return self.returnRangeCode()

    def redesign(self):
        self.changeSize(self.width, self.height)

    def AddProxyWidget(self):
        self.proxyWidget = RangeNodeUI(self)
        self.proxyWidget.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.proxyWidget.setFixedSize(self.width - 20, self.height - 50)
        self.nodeGraphic.createProxyWidget(self.proxyWidget)
        self.proxyWidget.setFixedWidth(self.width - 20)
        self.proxyWidget.setFixedHeight(self.height - 80)
        self.proxyWidget.move(int(self.width // 2 - self.proxyWidget.width() // 2),
                              int(self.height // 2 - self.proxyWidget.height() // 2) + 20)
        self.setDefaultParameters()

    def setDefaultParameters(self):
        self.proxyWidget.lneStart.setText(str(self.inPlugs[0].getValue()))
        self.proxyWidget.lneEnd.setText(str(self.inPlugs[1].getValue()))
        self.proxyWidget.lneStep.setText(str(self.inPlugs[2].getValue()))

    def returnRangeCode(self):
        startTitle, startCode = self.getCodeFromInput(0)
        endTitle, endCode = self.getCodeFromInput(1)
        stepTitle, stepCode = self.getCodeFromInput(2)
        return f'{startCode}\n{endCode}\n{stepCode}\n{self.getTitle()} = range({startTitle}, {endTitle}, {stepTitle})'