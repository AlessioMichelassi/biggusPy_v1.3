import random

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class ResizeHandle(QGraphicsItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)

    def boundingRect(self):
        return QRectF(0, 0, 50, 50)

    def paint(self, painter, option, widget=None):
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(Qt.BrushStyle.BDiagPattern)
        #painter.setBrush(QColor(40, 40, 40))
        painter.drawRect(0, 0, 50, 50)


class ResizableRectangle(QGraphicsItem):
    resizing = False
    mouse_press_pos = None

    def __init__(self, x, y, width, height, color=None, parent=None):
        super().__init__(parent)
        self.boundingRect = QRectF(x, y, width, height)
        if color is None:
            self.backColor = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 100)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.handle = ResizeHandle(self)
        self.handle.setPos(self.boundingRect.bottomRight() - QPointF(50, 50))
        self.original_rect = self.boundingRect

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if event.scenePos() in self.handle.sceneBoundingRect():
                self.setCursor(Qt.CursorShape.SizeFDiagCursor)
                self.resizing = True
                self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.resizing:
            topSize = self.boundingRect.topLeft()
            self.prepareGeometryChange()
            self.boundingRect = QRectF(topSize, event.scenePos() * 0.5)
            self.handle.setPos(self.boundingRect.bottomRight() - QPointF(50, 50))
            self.update()

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.resizing:
            self.resizing = False
            self.setCursor(Qt.CursorShape.ArrowCursor)
            self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        else:
            super().mouseReleaseEvent(event)

    def boundingRect(self):
        return self.boundingRect.normalized()

    def paint(self, paint, option, widget=None):
        if self.isSelected():
            paint.setPen(QPen(Qt.GlobalColor.red))
        else:
            paint.setPen(QPen(Qt.GlobalColor.black))
        paint.setBrush(self.backColor)
        paint.drawRoundedRect(self.boundingRect, 5, 5)
