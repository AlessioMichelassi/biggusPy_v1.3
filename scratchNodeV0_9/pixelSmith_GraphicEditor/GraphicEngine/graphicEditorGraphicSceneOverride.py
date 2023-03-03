from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class graphicEditor_GraphicSceneOverride(QGraphicsScene):
    colorBackground: QColor = QColor(39, 39, 39, 255)
    greyLighter: QColor = QColor(47, 47, 47, 255)
    greyDarker: QColor = QColor(29, 29, 29, 255)
    axisColor: QColor = QColor(150, 0, 0, 70)
    currentMousePos = QPointF(0, 0)
    isAxisVisible = True

    def __init__(self, parent=None):
        super(graphicEditor_GraphicSceneOverride, self).__init__(parent)
        self.setSceneRect(0, 0, 1000, 1000)
        # set the grid Size
        self.smallGridSize = 10
        self.bigGridSize = 50

        # set the color of the scene
        self.setBackgroundBrush(self.colorBackground)
        self._penLight = QPen(self.greyLighter)
        self._penLight.setWidth(1)
        self._penDark = QPen(self.greyDarker)
        self._penDark.setWidth(2)

    def setGraphicScene(self, width, height):
        self.setSceneRect(-width // 2, -height // 2, width, height)

    def drawBackground(self, painter: QPainter, rect: QRectF) -> None:
        super().drawBackground(painter, rect)
        self.drawGrid(painter, rect)
        if self.isAxisVisible:
            self.drawAxis(painter, rect)

    def drawAxis(self, painter, rect):
        _left = int(rect.left())
        _right = int(rect.right())
        _top = int(rect.top())
        _bottom = int(rect.bottom())
        # Draw the red line
        painter.setPen(QPen(self.axisColor, 1))
        horizontalAxis = QLine(_left, 0, _right, 0)
        verticalAxis = QLine(0, _top, 0, _bottom)
        painter.drawLine(horizontalAxis)
        painter.drawLine(verticalAxis)

    def drawGrid(self, painter, rect):
        _left = int(rect.left())
        _right = int(rect.right())
        _top = int(rect.top())
        _bottom = int(rect.bottom())
        redLines = []
        lightGreyLines, darkGreyLines = [], []
        firstVerticalLine = _left - (_left % self.smallGridSize) - 20
        firstHorizontalLine = _top - (_top % self.smallGridSize) - 20

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


