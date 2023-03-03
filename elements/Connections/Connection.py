import json

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QGraphicsItem


class Connection(QGraphicsItem):
    outputNode = None
    outputPlug = None
    outIndex = None
    inputNode = None
    inputPlug = None
    inIndex = None

    def __init__(self, outputNode: 'AbstractNodeInterface', outputPlug: 'PlugData', outIndex,
                 inputNode: 'AbstractNodeInterface', inputPlug: 'PlugData', inIndex):
        super().__init__()

        self.checkTheRightPlugType(outputNode, outputPlug, outIndex, inputNode, inputPlug, inIndex)
        self.setFlag(QGraphicsItem.ItemIsSelectable)

    def checkTheRightPlugType(self, outputNode, outputPlug, outIndex, inputNode, inputPlug, inIndex):
        if "Out" in outputPlug.className:
            self.outputNode = outputNode
            self.outputPlug = outputPlug
            self.outIndex = outIndex
            self.inputNode = inputNode
            self.inputPlug = inputPlug
            self.inIndex = inIndex
        elif "In" in inputPlug.className:
            self.outputNode = inputNode
            self.outputPlug = inputPlug
            self.outIndex = inIndex
            self.inputNode = outputNode
            self.inputPlug = outputPlug
            self.inIndex = outIndex

    def __str__(self):
        return f"{self.outputNode.getTitle()}[{self.outputPlug.getTitle()}] -> [{self.inputPlug.getTitle()}]{self.inputNode.getTitle()}"

    def updateValue(self):
        self.outputNode.calculate()
        value = self.outputNode.outPlugs[self.outIndex].getValue()
        self.inputNode.inPlugs[self.inIndex].setValue(value[0], value[1], value[2])
        self.inputNode.calculate()
        if self.inputNode.outConnections:
            for connection in self.inputNode.outConnections:
                connection.updateValue()

    def disconnect(self):
        if self in self.inputNode.outConnections:
            self.inputNode.outConnections.remove(self)
        if self in self.outputNode.outConnections:
            self.outputNode.outConnections.remove(self)

        resetValue = self.inputNode.inPlugs[self.inIndex].resetValue
        self.inputNode.inPlugs[self.inIndex].setValue(resetValue, type(resetValue), resetValue)
        self.inputNode.calculate()
        if self.inputNode.outConnections:
            for connection in self.inputNode.outConnections:
                connection.updateValue()

    def boundingRect(self):
        return QRectF(self.outputPlug.plugGraphic.scenePos(), self.inputPlug.plugGraphic.scenePos()).normalized()

    def paint(self, painter, _QStyleOptionGraphicsItem, widget=None):
        if not self.isSelected():
            painter.setPen(QPen(QColor(0, 20, 20), 3))
        else:
            painter.setPen(QPen(QColor(250, 50, 50), 3))
        painter.drawLine(self.outputPlug.plugGraphic.scenePos(), self.inputPlug.plugGraphic.scenePos())

    def serialize(self):
        dicts = {
            'inputNodeName': self.inputNode.getTitle(),
            'inputPlug': self.inputPlug.index,
            'outputNodeName': self.outputNode.getTitle(),
            'outputPlug': self.outputPlug.index,
        }
        return json.dumps(dicts, indent=4)
