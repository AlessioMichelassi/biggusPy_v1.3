from PyQt5.QtCore import QDir, QUrl
from PyQt5.QtGui import QClipboard
from PyQt5.QtWidgets import QFileDialog, QApplication, QMenu

from elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface


class VideoFileNode(AbstractNodeInterface):
    startValue = 0
    width = 50
    height = 120
    colorTrain = []
    logo = r"Release/biggusFolder/imgs/logos/Qt.png"

    def __init__(self, value="uriFile", inNum=2, outNum=1, parent=None):
        super().__init__(value, inNum, outNum, parent)
        self.setClassName("VideoFileNode")
        self.setName("VideoFileNode")
        self.changeSize(self.width, self.height)

    def openFile(self):
        openFileDialog = QFileDialog()
        openFileDialog.setFileMode(QFileDialog.AnyFile)
        openFileDialog.setFilter(QDir.Files)
        openFileDialog.setNameFilter("Video Files (*.mp4 *.avi *.mkv *.mov *.mpg *.mpeg *.wmv *.flv *.webm *.ogg *.ogv *.m4v *.3gp *.3g2 *.mxf *.mts *.m2ts *.ts *.vob *.drc *.gifv *.mng *.qt *.yuv *.rm *.rmvb *.asf *.amv *.m4p *.m4v *.svi *.viv *.f4v *.f4p *.f4a *.f4b)")
        openFileDialog.setViewMode(QFileDialog.Detail)
        if openFileDialog.exec():
            path = openFileDialog.selectedFiles()[0]
            uriPath = QUrl.fromLocalFile(path)
            self.changeInputValue(0, uriPath.toString())
            self.calculateOutput(0)
            self.redesign()

    def calculateOutput(self, plugIndex):
        value = self.inPlugs[0].getValue()
        self.outPlugs[plugIndex].setValue(value)
        return self.outPlugs[plugIndex].getValue()

    def redesign(self):
        self.changeSize(self.width, self.height)

    def showContextMenu(self, position):
        contextMenu = QMenu(self)
        contextMenu.addSection("load a video file")
        action1 = contextMenu.addAction("load file")
        action2 = contextMenu.addAction("set as URL")
        action = contextMenu.exec(position)
        if action == action1:
            self.openFile()
        elif action == action2:
            self.setAsUrl()

    def setAsUrl(self):
        # prende il testo della casella di testo e lo mette come valore di input
        text = QApplication.clipboard().text()
        self.updateTxtTitleFromGraphics(text)
        path = QUrl(text)
        self.changeInputValue(0, path.toString())
