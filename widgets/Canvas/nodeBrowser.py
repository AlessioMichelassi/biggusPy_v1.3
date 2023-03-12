import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

openCvNodeFolderPath: str = r"/home/tedk/Desktop/python/biggusPy_v1.3/elements/Nodes/pyqt5Node"
pythonNodeFolderPath: str = r"/home/tedk/Desktop/python/biggusPy_v1.3/elements/Nodes/PythonNodes"
pyQt5NodeFolderPath: str = r"/home/tedk/Desktop/python/biggusPy_v1.3/elements/Nodes/openCvNode"


class tabPage(QListWidget):
    drag_start_position = None
    selected_node = None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragEnabled(True)
        self.setSelectionMode(QListWidget.SingleSelection)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Inizia a tenere traccia della posizione del mouse e dell'elemento selezionato
            self.drag_start_position = event.pos()
            self.selected_node = self.itemAt(self.drag_start_position)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            # Crea un'istanza della classe QDrag
            drag = QDrag(self)

            # Aggiungi i dati necessari per trasferire l'oggetto nella canvas
            mime_data = QMimeData()
            mime_data.setText(self.selected_node.text())
            drag.setMimeData(mime_data)

            # Avvia il drag and drop
            drag.exec_(Qt.DropAction.CopyAction | Qt.DropAction.MoveAction)
        super().mouseMoveEvent(event)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
        super().dragEnterEvent(event)


class NodeBrowser(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowType.Window)

        self.tabWidget = QTabWidget()

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.tabWidget)
        self.setLayout(mainLayout)
        self.addTabPage("python", pythonNodeFolderPath)
        self.addTabPage("pyqt5", pyQt5NodeFolderPath)
        self.addTabPage("opencv", openCvNodeFolderPath)

    def addTabPage(self, name, itemList):
        widgetGridLayout = QGridLayout()
        widget = QWidget()
        self.tabWidget.addTab(widget, name)
        widget.setLayout(widgetGridLayout)

        Nodes = []
        for _file in os.listdir(itemList):
            if _file.endswith('.py'):
                Nodes.append(_file[:-3])
                # Creiamo un nuovo QPushButton per il nodo e lo aggiungiamo alla griglia
                nodeButton = QPushButton(QIcon(r"<path-to-node-icon>"), _file[:-3])
                nodeButton.setIconSize(QSize(64, 64))
                nodeButton.setFixedSize(80, 20)
                nodeButton.setFont(QFont("Arial", 7))
                row, col = divmod(len(Nodes), 4)
                widgetGridLayout.addWidget(nodeButton, row, col)


if __name__ == '__main__':
    app = QApplication([])
    node_browser = NodeBrowser()
    node_browser.show()
    app.exec_()