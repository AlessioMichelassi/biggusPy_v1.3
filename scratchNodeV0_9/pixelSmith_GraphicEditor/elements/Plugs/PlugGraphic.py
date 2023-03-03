from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class SuperTxtTitle(QGraphicsTextItem):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

    def setColor(self, color):
        self.setDefaultTextColor(color)

    def setText(self, txt):
        self.parent.plugData.setNameFromGraphic(txt)

    def eventFilter(self, obj, event):
        # Verifica se l'evento è una pressione del tasto Invio
        if event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Return:
            # Esegue l'azione desiderata (ad esempio, imposta il nuovo valore del testo)
            self.setText(self.toPlainText().strip())
            return True
        return super().eventFilter(obj, event)


class PlugGraphic(QGraphicsItem):
    txtTitle: QGraphicsTextItem
    plugData = None
    isLocked = True
    isGraphicalRenamePermitted = False
    nodeGraphic = None

    def __init__(self, plugData, diameter=8, parent=None):
        super().__init__(parent)
        self.diameter = diameter
        self.plugData = plugData
        self.nodeGraphic = parent
        self.nodeInterface = self.nodeGraphic.nodeInterface
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.boundingRectangle = QRectF(-self.diameter // 2, -self.diameter // 2, self.diameter * 2, self.diameter * 2)
        self.setZValue(2)
        self.createTitleText()

    def __str__(self):
        return f"[{self.title}] = {self.plugData.getValue()} index = {self.plugData.index}"

    @property
    def name(self):
        return self.plugData.className

    @property
    def title(self):
        return f"{self.plugData.getTitle()}"

    def createTitleText(self):
        font = QFont()
        font.setPointSize(10)
        self.txtTitle = SuperTxtTitle(self)
        self.txtTitle.setFont(font)
        self.txtTitle.installEventFilter(self.txtTitle)
        # self.txtTitle.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction)
        self.txtTitle.setPlainText(self.title)
        # Posiziona la label 20 pixel sopra il centro del nodo
        self.txtTitle.setDefaultTextColor(Qt.GlobalColor.white)
        self.defineTextPosition()
        self.txtTitle.setZValue(2)

    def defineTextPosition(self):
        x = self.txtTitle.boundingRect().width()
        if "In" in self.plugData.className:
            x = (x * -1) - 5
        elif "Out" in self.plugData.className:
            x = 10
        self.txtTitle.setPos(x, -10)

    def updateTitle(self):
        self.txtTitle.setPlainText(self.title)
        self.defineTextPosition()

    def boundingRect(self):
        return self.boundingRectangle.normalized()

    def paint(self, painter, option, widget=None):
        # Draw the plugs
        painter.setBrush(Qt.GlobalColor.white)
        if not self.isSelected():
            painter.setPen(Qt.GlobalColor.black)
        else:
            painter.setPen(Qt.GlobalColor.red)
        _centerPoint = QPoint(self.diameter // 2, self.diameter // 2)
        painter.drawEllipse(_centerPoint, self.diameter, self.diameter)
        # draw the center  of the circle
        painter.setPen(Qt.GlobalColor.black)
        painter.setBrush(Qt.GlobalColor.black)
        _radius = self.diameter // 2
        painter.drawEllipse(_centerPoint, 3, 3)

    def contextMenuEvent(self, event: 'QGraphicsSceneContextMenuEvent') -> None:
        if not self.nodeInterface.isEditable:
            return
        menu = QMenu()
        actionRename = menu.addAction("Enable ReTitle")
        actionDelete = menu.addAction("Delete")
        actionUnlock = (
            menu.addAction("Unlock") if self.isLocked else menu.addAction("Lock")
        )
        if actionRename == menu.exec_(event.screenPos()):
            self.rename()
        elif actionDelete == menu.exec_(event.screenPos()):
            self.delete()
        elif actionUnlock == menu.exec_(event.screenPos()):
            self.unlock()

    def rename(self):
        """
        This method is called when the user right click on the plug and select the rename option.
        Is possibile to rename the plug only if the node is in editing mode. If you enable
        :return:
        """
        self.isGraphicalRenamePermitted = not self.isGraphicalRenamePermitted
        if self.isGraphicalRenamePermitted:
            self.txtTitle.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction)
        else:
            self.txtTitle.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

    def delete(self):
        self.nodeInterface.deletePlug(self)

    def unlock(self):
        if self.isLocked:
            self.isLocked = False
            self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        else:
            self.isLocked = True
            self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
