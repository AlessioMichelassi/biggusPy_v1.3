# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class ConvertToGrayscaleThread(QThread):
    converted = pyqtSignal(QPixmap, name="converted")

    def __init__(self, filename, grayStyle):
        super().__init__()
        self.filename = filename
        self.grayStyle = grayStyle
        self.stopped = False

    def run(self):
        # Carica l'immagine e ridimensiona se necessario
        image = QImage(self.filename)
        width = image.width()
        height = image.height()
        for y in range(height):
            for x in range(width):
                r, g, b, a = image.pixelColor(x, y).getRgb()
                if self.grayStyle == "Luminosity":
                    gray = int(0.21 * r + 0.72 * g + 0.07 * b)
                elif self.grayStyle == "Average":
                    gray = (r + g + b) // 3
                elif self.grayStyle == "gOnly":
                    gray = g + g + g // 3
                elif self.grayStyle == "rOnly":
                    gray = r
                elif self.grayStyle == "bOnly":
                    gray = b
                else:
                    gray = int(0.16 * r + 0.67 * g + 0.07 * b)
                image.setPixel(x, y, qRgba(gray, gray, gray, a))
                if self.stopped:
                    return
        pixmap = QPixmap.fromImage(image)

        # Emitti il segnale con l'immagine convertita
        self.converted.emit(pixmap)

    def stopThread(self):
        self.stopped = True
        self.wait()


class SuperTxtTitle(QGraphicsTextItem):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

    def setColor(self, color):
        self.setDefaultTextColor(color)

    def setText(self, txt):
        title = self.parent.nodeInterface.updateTxtTitleFromGraphics(txt)
        self.parent.updateTitlePosition()

    def eventFilter(self, obj, event):
        # Verifica se l'evento è una pressione del tasto Invio
        if event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Return:
            # Esegue l'azione desiderata (ad esempio, imposta il nuovo valore del testo)
            self.setText(self.toPlainText().strip())
            return True
        return super().eventFilter(obj, event)


class SuperQLineEdit(QLineEdit):
    font = QFont("Arial", 7)

    def __init__(self, graphicNode, parent=None):
        super().__init__(parent)
        self.graphicNode = graphicNode
        # rounded_rec è self.rect() +0.5 per evitare che il bordo del QLineEdit sia sfasato
        rect = QRectF(self.rect().x() - 0.5, self.rect().y() - 0.5, self.rect().width() + 0.5,
                      self.rect().height() + 0.5)
        self.rounded_rect = rect.normalized()
        self.setFrame(False)
        # il problema nella qLine è che si vede il rettangolo sotto nonostante il bordo
        # per risolverlo si può usare un background-clip: border-box; che non funziona, oppure
        # si può usare un background-color: transparent; che non funziona, oppure
        # si può usare un background-color: rgba(0,0,0,0); che funziona
        self.styleZ = f"""
                            QLineEdit 
                                    {{
                                        color: {self.graphicNode.proxyColorText.name()};
                                        background-color: {self.graphicNode.proxyColorFill.name()};
                                        border: 1px solid {self.graphicNode.proxyColorBorder.name()};
                                        border-radius: 2px;
                                        background-clip: border-box;
                                    }}
                            QLineEdit:hover
                                    {{
                                        border: 1px solid {self.graphicNode.proxyColorBorder.name()};
                                    }}
                        """
        self.setStyleSheet(self.styleZ)

    def updateStyle(self):
        r, g, b = self.graphicNode.proxyColorFill.red(), self.graphicNode.proxyColorFill.green(), \
            self.graphicNode.proxyColorFill.blue()
        self.styleZ = f"""
                        QLineEdit 
                                {{
                                    color: {self.graphicNode.proxyColorText.name()};
                                    background-color: rgba({r}, {g}, {b}, 100);
                                    border: 1px solid {self.graphicNode.proxyColorBorder.name()};
                                    border-radius: 2px;
                                    background-clip: border-box;
                                }}
                        QLineEdit:hover
                                {{
                                    border: 1px solid {self.graphicNode.proxyColorBorder.name()};
                                }}
                                """
        self.setStyleSheet(self.styleZ)

    def focusInEvent(self, event):
        self.setStyleSheet(self.styleZ)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self.setStyleSheet(self.styleZ)
        super().focusOutEvent(event)


class SizeGripZ(QGraphicsItem):
    def __init__(self, graphicNode, parent=None):
        super().__init__(parent)
        self.graphicNode = graphicNode
        self.setParentItem(self.graphicNode)
        # crea un rettangolo dal nodo
        self.boundingRectangle = QRectF(0, 0, 5, 5)
        self.rect = self.boundingRectangle.adjusted(1, 1, -1, -1)
        # disegna la diagonale del rettangolo dall'angolo in basso a sinistra
        # al vertice in alto a destra

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.setZValue(11)

    def boundingRect(self):
        return self.boundingRectangle.normalized()

    def paint(self, painter, option, widget=None):
        brush = QBrush(QColor(0, 0, 0, 40))
        pen = QPen(Qt.PenStyle.SolidLine)
        pen.setWidth(1)
        pen.setColor(QColor(70, 70, 70, 150))
        painter.setBrush(brush)
        painter.setPen(pen)
        bottom_right = self.rect.bottomRight()
        top_right = self.rect.topRight()
        bottom_left = self.rect.bottomLeft()

        delta_x = bottom_right.x() - bottom_left.x()
        delta_y = bottom_left.y() - top_right.y()

        # Disegna le tre linee parallele
        for i in range(3):
            start = QPointF(bottom_right.x() - delta_y / 3 * (i + 1), bottom_right.y() - delta_y / 3 * (i + 1))
            end = QPointF(top_right.x() - delta_y / 3 * (i + 1), top_right.y() - delta_y / 3 * (i + 1))
            painter.drawLine(QLineF(start, end))

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange and self.scene():
            delta = value - self.pos()
            self.scene().parentItem().resize(delta.x(), delta.y())
        return super().itemChange(change, value)


class AbstractNodeGraphic(QGraphicsItem):
    # NodeGraphic parameter
    width: int = 50
    height: int = 100

    logo: QLabel
    logoPath: str = "C:/Users/Andrea/Desktop/pixelSmith_GraphicEditor/elements/nodeV2_1/AbstractClass/logo.png"
    isLogoVisible: bool = True
    isLogoBandW: bool = False
    proxyLogo: QGraphicsProxyWidget
    logoSize: int = 20

    txtTitle: SuperTxtTitle
    txtValue: SuperQLineEdit
    txtValueProxy: QGraphicsProxyWidget

    contextMenu: QMenu

    # NodeGraphic colors
    borderColorDefault = QColor(10, 120, 10)
    borderColorSelect = QColor(255, 70, 10)
    borderColorHover = QColor(255, 255, 10)
    colorFill = QColor(10, 180, 40)
    proxyColorText = QColor(255, 255, 255)
    proxyColorFill = QColor(0, 0, 0)
    proxyColorBorder = QColor(255, 255, 255)
    proxyColorBorderSelect = QColor(255, 255, 255)

    inPlugs: list = []
    outPlugs: list = []
    isNodeCreated: bool = False

    def __init__(self, nodeInterface, parent=None):
        super(AbstractNodeGraphic, self).__init__(parent)
        self.nodeInterface = nodeInterface
        self.nodeData = self.nodeInterface.nodeData
        self.contextMenu = QMenu()
        self.inPlugs = []
        self.outPlugs = []
        # set flags
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        # set bounding rectangle
        self.boundingRectangle = QRectF(0, 0, self.width, self.height)
        self.setZValue(-20)
        self.isNodeCreated = True
        self.thread = None

    def boundingRect(self):
        return self.boundingRectangle.normalized()

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
            for connection in self.nodeInterface.outConnections:
                connection.adjust()
        return QGraphicsItem.itemChange(self, change, value)

    def paint(self, painter, option, widget=None):
        if not self.isSelected():
            painter.setPen(self.borderColorDefault)
        else:
            painter.setPen(self.borderColorSelect)
        if self.nodeInterface.isDisabled:
            painter.setBrush(QColor(20, 20, 20))
        else:
            painter.setBrush(self.colorFill)
        painter.drawRoundedRect(self.boundingRectangle, 5, 5)

    def contextMenuEvent(self, event):
        self.contextMenu.exec(event.screenPos())

    # ##########################################
    #
    #                Look & Feel
    #

    def setLogo(self, filePNG):
        self.logo = QLabel()
        self.logoPath = filePNG
        self.updateLogo()
        self.proxyLogo = QGraphicsProxyWidget(self)
        self.proxyLogo.setWidget(self.logo)
        self.proxyLogo.setPos(self.width - 28, 2)

    def updateLogo(self):
        pixmap = QPixmap()
        if self.isLogoBandW:
            pixmap = self.toGrayScale()
        else:
            pixmap.load(self.logoPath, "PNG", Qt.ImageConversionFlag.AutoColor)
        self.logo.setStyleSheet("background-color: transparent;")
        self.logo.setPixmap(pixmap)
        self.logo.setMaximumSize(25, 25)
        self.logo.setScaledContents(True)

    def updateLogoPosition(self):
        self.proxyLogo.setPos(self.width - 28, 2)

    def toGrayScale(self, grayStyle="Average"):
        image = QImage(self.logoPath)
        width = image.width()
        height = image.height()
        for y in range(height):
            for x in range(width):
                r, g, b, a = image.pixelColor(x, y).getRgb()
                if grayStyle == "Average":
                    gray = (r + g + b) // 3
                elif grayStyle == "Luminosity":
                    gray = int(0.21 * r + 0.72 * g + 0.07 * b)
                elif grayStyle == "bOnly":
                    gray = b
                elif grayStyle == "gOnly":
                    gray = g + g + g // 3
                elif grayStyle == "rOnly":
                    gray = r
                else:
                    gray = int(0.16 * r + 0.67 * g + 0.07 * b)
                image.setPixel(x, y, qRgba(gray, gray, gray, a))
        return QPixmap.fromImage(image)

    def setLogoBW(self, isBW: bool):
        """
        ITA: imposta il logo in bianco e nero mantenendo la trasparenza
        ENG: set the logo in black and white maintaining the transparency
        :param isBW:
        :return:
        """
        self.isLogoBandW = isBW
        self.updateLogo()

    def setLogoVisible(self, isVisible: bool):
        self.isLogoVisible = isVisible
        self.proxyLogo.setVisible(isVisible)

    def setColorTrain(self, colorTrain: list):
        self.colorFill = colorTrain[0]
        self.borderColorDefault = colorTrain[1]
        self.borderColorSelect = colorTrain[2]
        self.borderColorHover = colorTrain[3]
        self.proxyColorText = colorTrain[4]
        self.proxyColorFill = colorTrain[5]
        self.proxyColorBorder = colorTrain[6]
        self.proxyColorBorderSelect = colorTrain[7]
        self.txtValue.updateStyle()
        self.update()

    def getColorTrain(self):
        return [self.colorFill, self.borderColorDefault, self.borderColorSelect, self.borderColorHover,
                self.proxyColorText, self.proxyColorFill, self.proxyColorBorder, self.proxyColorBorderSelect]

    def changeSize(self, width, height):
        self.width = width
        self.height = height
        self.boundingRectangle = QRectF(0, 0, self.width, self.height)
        self.updatePlugsPos()
        self.updateTitlePosition()
        self.updateTxtValuePosition()
        self.update()

    # ##########################################
    #
    #                TITLE SECTION
    #

    def createTitle(self):
        self.txtTitle = SuperTxtTitle(self)
        self.txtTitle.installEventFilter(self.txtTitle)
        self.txtTitle.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction)
        self.txtTitle.setPlainText(self.nodeInterface.title)
        self.txtTitle.setDefaultTextColor(Qt.GlobalColor.white)
        self.txtTitle.setZValue(2)
        self.updateTitlePosition()

    def updateTitle(self, title):
        self.txtTitle.setPlainText(title)
        self.updateTitlePosition()

    def updateTitlePosition(self):
        x = self.txtTitle.boundingRect().width() // 2 - self.width // 2
        self.txtTitle.setPos(-x, -30)

    # ##########################################
    #
    #                VALUE SECTION
    #

    def createTxtValue(self):
        """
        laTxtValue è la QLineEdit che viene visualizzata sul Nodo e ne visualizza il valore
        dell'input 0 del nodo, oppure il valore di output 0 del nodo.
        :return:
        """
        self.txtValue = SuperQLineEdit(self)
        self.txtValueProxy = QGraphicsProxyWidget(self)
        self.txtValueProxy.setWidget(self.txtValue)
        self.txtValueProxy.setZValue(2)
        self.txtValue.setFocus()
        self.txtValue.returnPressed.connect(self.setTxtValue)
        self.initTxtValueProperties()
        self.updateTxtValuePosition()

    def setTxtValue(self):
        """
        Questo metodo viene chiamato quando viene premuto il tasto invio sulla QLineEdit.
        Generalmente in questo caso si vuole settare il valore della QLineEdit come input
        del nodo.
        :return:
        """
        self.nodeInterface.setInputValue(0, self.txtValue.text())
        self.txtValue.clearFocus()

    def initTxtValueProperties(self):
        self.txtValue.setFont(QFont("Arial", 9))
        self.txtValue.setFixedWidth(int(self.width * 1.4))
        self.txtValue.setFixedHeight(20)
        self.txtValue.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def setTextValueOnQLineEdit(self, value):
        """
        Questo metodo serve per settare il valore della QLineEdit
        dall'esterno.
        :param value:
        :return:
        """
        if not isinstance(value, str):
            value = str(value)
        self.txtValue.setText(value)

    def updateTxtValuePosition(self):
        """
        ITA:
            Questo metodo serve per aggiornare la larghezza della QLineEdit in base al testo
            che contiene. quello che può accadere in alcuni casi è che la Qline
            contenga una lista di valori, in questo caso la larghezza viene falsata da alcuni caratteri
            come le parentesi quadre e le virgole, quindi se la larghezza è maggiore
            del doppio rispetto alla larghezza del widget allora la larghezza viene ridotta.

        ENG:
            This method is used to update the width of the QLineEdit based on the text
            that contains. What happen in some cases is that the Qline
            contains a list, in this case the width is falsified by some characters
            such as square brackets and commas, so if the width is greater
        :return:
        """
        size = self.txtValue.sizeHint()
        newSize = QSize(size.width() * 2, size.height())
        self.txtValue.resize(newSize)
        if self.txtValue.width() > self.width * 2 - 40:
            self.txtValue.resize(self.width - 40, self.txtValue.height())
        x = (self.width - self.txtValue.width()) // 2
        y = self.height - (self.txtValue.height() * 1.2)
        self.txtValueProxy.setPos(x, y)

    def setTxtValueReadOnly(self, value):
        self.txtValue.setReadOnly(value)

    # ##########################################
    #
    #                PLUGS SECTION
    #

    def addPlug(self, _type, plug):
        if _type == "In":
            self.inPlugs.append(plug)
        elif _type == "Out":
            self.outPlugs.append(plug)

    def deleteInPlug(self, index):
        try:
            self.inPlugs.pop(index)
        except IndexError:
            print("warning from AbstractNodeGraphic.deleteInPlug: index out of range")

    def updatePlugsPos(self):
        self.updatePlugPosition(self.inPlugs)
        self.updatePlugPosition(self.outPlugs)

    def updatePlugPosition(self, plugReference):
        x = -8
        if "out" in plugReference[0].plugData.className.lower():
            x = self.width - 2
        if len(plugReference) == 1:
            y = self.height // 2
            plugReference[0].setPos(QPointF(x, y))
        else:
            # Quello che fa è calcolare la distanza tra i vari plug
            # in modo che siano sempre uguali
            y = (self.height - (len(plugReference) * plugReference[0].diameter * 3)) // 2
            for plug in plugReference:
                plug.setPos(QPointF(x, y))
                y += plug.diameter * 3
