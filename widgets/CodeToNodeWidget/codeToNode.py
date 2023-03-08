from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow

from widgets.CodeToNodeWidget.codeToNodeWidget import CodeToNodeWidget


class CodeToNode(QMainWindow):

    def __init__(self, canvas, parent=None):
        super(CodeToNode, self).__init__(parent, Qt.WindowType.Window)
        self.setWindowTitle("Code to Node")
        self.setMinimumSize(500, 500)
        self.codeToNode = CodeToNodeWidget(canvas)
        self.setCentralWidget(self.codeToNode)