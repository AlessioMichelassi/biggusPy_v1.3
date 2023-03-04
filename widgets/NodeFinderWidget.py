from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class NodeFinderWidget(QWidget):
    def __init__(self, canvas, view, centerPoint, parent=None):
        super().__init__(parent)
        self.canvas = canvas
        self.graphicView = view
        self.centerPoint = centerPoint
        self.node_name_list = self.canvas.node_name_list

        self.completer = QCompleter(self.node_name_list)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

        self.lndInput = QLineEdit()
        self.lndInput.setCompleter(self.completer)
        self.lndInput.returnPressed.connect(self.returnName)
        self.okButton = QPushButton("Create")
        self.okButton.clicked.connect(self.returnName)
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.closeWin)

        # Create and set the layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.okButton)
        button_layout.addWidget(self.cancelButton)
        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(self.lndInput)
        mainLayout.addLayout(button_layout)
        self.setLayout(mainLayout)
        self.lndInput.setFocus()

    def returnName(self):
        # sourcery skip: use-named-expression
        node_name = self.sender().parent().lndInput.text()
        # Create the node using the name
        if node_name:
            self.canvas.addNodeByName(node_name)
        self.graphicView.isTabWindowsOpen = False
        self.close()

    def closeWin(self):
        self.graphicView.isTabWindowsOpen = False
        self.close()
