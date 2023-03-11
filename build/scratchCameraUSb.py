from PyQt5.QtCore import Qt
from PyQt5.QtMultimediaWidgets import QCameraViewfinder
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtMultimedia import *


class CameraWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Creazione del visualizzatore di anteprima
        self.viewfinder = QCameraViewfinder(self)
        self.viewfinder.setFixedSize(640, 480)

        # Creazione del pulsante per avviare/fermare la cattura del video
        self.capture_button = QPushButton('Start', self)
        self.capture_button.clicked.connect(self.toggle_capture)

        # Creazione dell'oggetto QCamera
        self.camera = QCamera()
        self.camera.setViewfinder(self.viewfinder)

        # Creazione del layout per organizzare i widget
        layout = QVBoxLayout(self)
        layout.addWidget(self.viewfinder)
        layout.addWidget(self.capture_button)

    def toggle_capture(self):
        if self.camera.state() == QCamera.ActiveState:
            self.camera.stop()
            self.capture_button.setText('Start')
        else:
            self.camera.start()
            self.capture_button.setText('Stop')


if __name__ == '__main__':
    app = QApplication([])
    widget = CameraWidget()
    widget.show()
    app.exec_()