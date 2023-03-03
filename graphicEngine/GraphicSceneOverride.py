
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class GraphicSceneOverride(QGraphicsScene):
    colorBackground: QColor = QColor(39, 39, 39, 255)
    greyLighter: QColor = QColor(47, 47, 47, 255)
    greyDarker = QColor = QColor(29, 29, 29, 255)
    currentMousePos = QPointF(0, 0)

    def __init__(self, parent=None):
        super().__init__(parent)

        # set the grid Size
        self.smallGridSize = 10
        self.bigGridSize = 50

        # set the color of the scene
        self.setBackgroundBrush(self.colorBackground)
        self._penLight = QPen(self.greyLighter)
        self._penLight.setWidth(1)
        self._penDark = QPen(self.greyDarker)
        self._penDark.setWidth(2)

    def setGraphicSceneSize(self, width, height):
        self.setSceneRect(-width // 2, -height // 2, width, height)

    def drawBackground(self, painter: QPainter, rect: QRectF) -> None:
        super().drawBackground(painter, rect)

        _left = int(rect.left())
        _right = int(rect.right())
        _top = int(rect.top())
        _bottom = int(rect.bottom())

        lightGreyLines, darkGreyLines = [], []
        firstVerticalLine = _left - (_left % self.smallGridSize)
        firstHorizontalLine = _top - (_top % self.smallGridSize)

        for x in range(firstVerticalLine, _right, self.smallGridSize):
            if x % self.bigGridSize == 0:
                darkGreyLines.append(QLine(x, _top, x, _bottom))
            else:
                lightGreyLines.append(QLine(x, _top, x, _bottom))

        for y in range(firstHorizontalLine, _bottom, self.smallGridSize):
            if y % self.bigGridSize == 0:
                darkGreyLines.append(QLine(_left, y, _right, y))
            else:
                lightGreyLines.append(QLine(_left, y, _right, y))
        painter.setPen(self._penLight)
        painter.drawLines(*lightGreyLines)
        painter.setPen(self._penDark)
        if darkGreyLines:
            painter.drawLines(*darkGreyLines)

    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        super().mouseMoveEvent(event)
        self.currentMousePos = event.scenePos()




