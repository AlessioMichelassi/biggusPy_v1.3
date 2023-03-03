from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from elements.Connections.Connection import Connection


class Arrow(QGraphicsItem):
    currentNode = None

    def __init__(self, startPlug: 'PlugGraphic', end_point, parent=None):
        super().__init__(parent)
        self.startPlug = startPlug
        self.endPlug = None
        self.startPoint = startPlug.scenePos()
        self.endPoint = end_point
        self.setZValue(-1)

    def updatePosition(self, pos):
        self.endPoint = pos
        self.update()

    def establishConnection(self, endPlug: 'PlugGraphic'):
        if self.checkIfConnectionIsPossible(endPlug):
            # controlla che lo start plug sia di Out altrimenti inverte i nodi
            if self.startPlug.name == "Out":
                # Crea una nuova freccia
                outputNode = self.startPlug.nodeGraphic.nodeData
                outputPlug = self.startPlug.plugData
                inputNode = endPlug.nodeGraphic.nodeData
                inputPlug = endPlug.plugData
            else:
                # Crea una nuova freccia
                outputNode = endPlug.nodeGraphic.nodeData
                outputPlug = endPlug.plugData
                inputNode = self.startPlug.nodeGraphic.nodeData
                inputPlug = self.startPlug.plugData
            conn = Connection(outputNode, outputPlug, outputPlug.index, inputNode, inputPlug, inputPlug.index)
            # Aggiungi la freccia alla scena
            self.scene().addItem(conn)
            return conn

    def checkIfConnectionIsPossible(self, endPlug: 'PlugGraphic'):
        """
        Controlla se la connessione è possibile.
        Una connessione è possibile se i due plug sono di sue nodi diversi
        e se i plug non sono dello stesso seme: In con In o Out con Out
        :param endPlug: Plug di destinazione
        """
        if self.startPlug.nodeGraphic == endPlug.nodeGraphic:
            print("you can't connected plug of the same node")
            return False
        elif self.startPlug.name == endPlug.name:
            print("you can't connected plug of the same type")
            return False
        else:
            return True

    def boundingRect(self):
        # Definiamo un bounding rectangle che include entrambe i punti della freccia
        return QRectF(self.startPoint, self.endPoint).normalized()

    def paint(self, painter, _QStyleOptionGraphicsItem, widget=None):
        # Disegniamo la freccia utilizzando un QPainter
        painter.setPen(QPen(Qt.GlobalColor.black, 2, Qt.PenStyle.DashLine))
        painter.drawLine(self.startPoint, self.endPoint)

