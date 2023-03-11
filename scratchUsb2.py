from PyQt5.QtCore import Qt, QBuffer, QIODevice
from PyQt5.QtMultimediaWidgets import QCameraViewfinder
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtMultimedia import *
from PyQt5.QtGui import QImage, QPixmap


class CameraWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Creazione del visualizzatore di anteprima
        self.viewfinder = QCameraViewfinder(self)
        self.viewfinder.setFixedSize(640, 480)

        # Creazione dell'oggetto QCamera
        self.camera = QCamera()
        self.camera.setViewfinder(self.viewfinder)

        # Creazione dell'oggetto QCameraImageCapture per acquisire le immagini
        self.capture = QCameraImageCapture(self.camera)

        # Avvio della cattura del video
        self.camera.start()

        # Creazione del layout per organizzare i widget
        layout = QVBoxLayout(self)
        layout.addWidget(self.viewfinder)
        self.label = QLabel(self)
        layout.addWidget(self.label)

        # Avvio della cattura delle immagini in tempo reale
        self.capture.imageCaptured.connect(self.process_image)
        self.capture.capture()

    def process_image(self, id, image):
        # Conversione dell'immagine in una QPixmap per visualizzarla
        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication([])
    widget = CameraWidget()
    widget.show()
    app.exec_()
