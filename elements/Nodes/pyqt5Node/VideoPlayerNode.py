from PyQt5.QtCore import Qt, QDir, QUrl
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtWidgets import *

from elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface


class VideoPlayerWidget(QWidget):

    def __init__(self, parent=None):
        super(VideoPlayerWidget, self).__init__(parent)

        self.mediaPlayer = QMediaPlayer(self, QMediaPlayer.VideoSurface)

        self.videoWidget = QVideoWidget(self)
        self.videoWidget.resize(100, 100)
        openButton = QPushButton("Open...")
        openButton.clicked.connect(self.openFile)

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                                      QSizePolicy.Maximum)

        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(openButton)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)

        layout = QVBoxLayout(self)
        layout.addWidget(self.videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.errorLabel)

        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.mediaPlayer.state() == QMediaPlayer.StoppedState:
            painter.drawText(self.rect(), Qt.AlignCenter, "VideoPlayer")
            return

        if self.mediaPlayer.state() == QMediaPlayer.InvalidMedia:
            painter.drawText(self.rect(), Qt.AlignCenter, "Invalid Media")
            return

        super().paintEvent(event)

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                                                  QDir.homePath())

        if fileName != '':
            self.mediaPlayer.setMedia(
                QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())


class videoPlayerTest(QGraphicsVideoItem):

    def __init__(self, parent=None):
        super(videoPlayerTest, self).__init__(parent)
        self.setParentItem(parent)
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.mediaPlayer.setVideoOutput(self)


class VideoPlayerView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.verticalScrollBar().setDisabled(True)
        self.horizontalScrollBar().setDisabled(True)
        self.setStyleSheet("background:rgb(20,20,20); border: 6px;")
        # create video player widget
        self.videoPlayer = videoPlayerTest()

        # add video widget to the scene
        self.scene.addItem(self.videoPlayer)
        self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

    def setVideo(self, uri):
        self.videoPlayer.mediaPlayer.setMedia(QMediaContent(QUrl(uri)))
        self.videoPlayer.mediaPlayer.play()


class VideoPlayerNode(AbstractNodeInterface):
    startValue = 0
    width = 400
    height = 250
    colorTrain = []
    proxyWidget: VideoPlayerView
    logo = r"Release/biggusFolder/imgs/logos/Qt.png"

    def __init__(self, value=20, inNum=2, outNum=1, parent=None):
        super().__init__(value, inNum, outNum, parent)
        self.setClassName("VideoPlayer")
        self.setName("VideoPlayer")
        self.changeSize(self.width, self.height)
        self.AddProxyWidget()

    def calculateOutput(self, plugIndex):
        value = self.inPlugs[0].getValue()
        try:
            self.proxyWidget.setVideo(value)
        except Exception as e:
            print(f"invalid video path: {value}")
        self.outPlugs[plugIndex].setValue(value)
        return self.outPlugs[plugIndex].getValue()

    def redesign(self):
        self.changeSize(self.width, self.height)

    def showContextMenu(self, position):
        contextMenu = QMenu(self)
        contextMenu.addSection("change name of menu here")
        action1 = contextMenu.addAction("action1")
        action2 = contextMenu.addAction("action2")
        action3 = contextMenu.addAction("action3")

        action = contextMenu.exec(position)
        if action == action1:
            self.doAction1()
        elif action == action2:
            self.doAction2()
        elif action == action3:
            self.doAction3()

    def doAction1(self):
        pass

    def doAction2(self):
        pass

    def doAction3(self):
        pass

    def AddProxyWidget(self):
        self.proxyWidget = VideoPlayerView()
        self.proxyWidget.setFixedSize(self.width - 20, self.height - 50)
        self.nodeGraphic.createProxyWidget(self.proxyWidget)
        self.proxyWidget.setFixedWidth(self.width - 20)
        self.proxyWidget.setFixedHeight(self.height - 50)
        self.proxyWidget.move(int(self.width // 2 - self.proxyWidget.width() // 2),
                              int(self.height // 2 - self.proxyWidget.height() // 2) + 20)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    player = VideoPlayerWidget()
    player.resize(320, 240)
    player.show()

    sys.exit(app.exec_())
