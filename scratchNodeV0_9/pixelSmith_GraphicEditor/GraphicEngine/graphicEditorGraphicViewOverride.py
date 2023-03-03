from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class graphicEditor_GraphicViewOverride(QGraphicsView):

    scenePosChanged = pyqtSignal(int, int)
    isMiddleMouseButtonPressed = False
    lastMiddleMousePosition = None

    def __init__(self, graphicScene, parent=None):
        super().__init__(parent)
        self.graphicScene = graphicScene
        self.setScene(self.graphicScene)
        self.setRenderProperties()
        self.centerOn(80, 90)
        self.scaleScene(4)

    def setRenderProperties(self):
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.HighQualityAntialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)

    # #########################################
    #
    #               Mouse Override
    #

    def wheelEvent(self, event):
        # sourcery skip: assign-if-exp
        """
        Override the wheel event to zoom in and out the scene
        :param event:
        :return:
        """
        delta = event.angleDelta().y()
        self.scaleScene(1.5 ** (delta / 240.0))

    def scaleScene(self, scaleFactor):
        """
        Scale the scene
        :param scaleFactor:
        :return:
        """
        currentScale = self.transform().m11()
        if 0.13 < currentScale < 15:
            self.scale(scaleFactor, scaleFactor)
        elif currentScale <= 0.13:
            self.scale(0.2 / currentScale, 0.2 / currentScale)
        else:
            self.scale(0.8, 0.8)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.setDragMode(QGraphicsView.DragMode.NoDrag)
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.MouseButton.MiddleButton:
            self.middleMouseButtonPress(event)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.MouseButton.MiddleButton:
            self.middleMouseButtonRelease(event)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        mousePosition = self.mapToScene(event.pos())
        self.scenePosChanged.emit(int(mousePosition.x()), int(mousePosition.y()))
        if self.isMiddleMouseButtonPressed:
            self.panTheScene(event)

    # #########################################
    #
    #               Mouse Events
    #

    def leftMouseButtonPress(self, event):
        """
        Override the left mouse button press event
        :param event:
        :return:
        """
        pass

    def leftMouseButtonRelease(self, event):
        """
        Override the left mouse button release event
        :param event:
        :return:
        """
        pass

    def middleMouseButtonPress(self, event):
        self.isMiddleMouseButtonPressed = True
        self.lastMiddleMousePosition = event.pos()
        self.setCursor(Qt.CursorShape.OpenHandCursor)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)

    def middleMouseButtonRelease(self, event):
        self.isMiddleMouseButtonPressed = False
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)

    def panTheScene(self, event):
        # panning the scene!
        self.setCursor(Qt.CursorShape.ClosedHandCursor)
        currentPosition = event.pos()
        deltaPosition = currentPosition - self.lastMiddleMousePosition
        self.lastMiddleMousePosition = currentPosition
        hsBarValue = self.horizontalScrollBar().value()
        self.horizontalScrollBar().setValue(int(hsBarValue - (deltaPosition.x())))
        vsBarValue = self.verticalScrollBar().value()
        self.verticalScrollBar().setValue(int(vsBarValue - (deltaPosition.y())))
        event.accept()

    def getItemAtClick(self, event):
        """
        ITA:
            Ritorna l'oggetto cliccato
        ENG:
            Returns the clicked object
        :param event:
        :return:
        """
        return self.itemAt(event.pos())

    def centerObjectOnView(self, selectedObject=None):
        """
        ITA:
            Centra un oggetto nella scena. Se non viene passato nessun oggetto, ma
            sono presenti degli oggetti non selezionati, crea un rettangolo contenente tutti gli oggetti
            non selezionati e centra la scena su questo rettangolo, altrimenti centra la scena sul punto (0,0)
        ENG:
            Center an object in the scene. If no object is passed, but there are
            objects that are not selected, create a rectangle containing all the objects
            not selected and center the scene on this rectangle, otherwise center the scene on the point (0,0)
        :param selectedObject:
        :return:
        """
        if selectedObject is None:
            self.selectAllCenterSceneAndDeselect()
            return
        self.centerOn(selectedObject)
        self.scaleScene(1)

    def centerViewOnScene(self):
        """
        ITA:
            Centra la scena nella view
        ENG:
            Center the scene in the view
        :return:
        """
        if self.graphicScene.items():
            self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
            self.centerOn(self.sceneRect().center())

    def selectAllCenterSceneAndDeselect(self):
        """
        ITA:
            Seleziona tutti gli oggetti nella scena, centra la scena su uno di questi oggetti, la
            scala in modo che tutti gli oggetti siano visibili e deseleziona tutti gli oggetti
        ENG:
            Select all the objects in the scene, center the scene on one of these objects, scale it
            so that all objects are visible and deselect all objects.
        :return:
        """
        for item in self.graphicScene.items():
            item.setSelected(True)
        objsRect = self.graphicScene.itemsBoundingRect()
        self.fitInView(objsRect, Qt.AspectRatioMode.KeepAspectRatio)
        for item in self.graphicScene.items():
            item.setSelected(False)

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        menu = QMenu()
        actionCenterObject = menu.addAction("Center Object on View")

        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == actionCenterObject:
            self.centerObjectOnView(self.getItemAtClick(event))