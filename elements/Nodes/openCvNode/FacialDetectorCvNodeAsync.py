import queue
import time

from PyQt5.QtCore import pyqtSignal, QThread, QObject
from PyQt5.QtGui import QColor
import cv2
import dlib
import numpy as np
from elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface


class FacialDetectorCvThread(QObject):
    def __init__(self, detector, predictor):
        super().__init__()
        self.detector = detector
        self.predictor = predictor
        self.image = None
        self.queue = queue.Queue()

    def setImage(self, image):
        self.image = image

    def run(self):
        while True:
            if self.image is not None:
                gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
                faces = self.detector(self.image, 0)

                # Draw rectangles around detected faces and return the image
                img_copy = self.image.copy()
                for face in faces:
                    x1, y1, x2, y2 = face.left(), face.top(), face.right(), face.bottom()
                    cv2.rectangle(img_copy, (x1, y1), (x2, y2), (0, 255, 0), 2)
                self.queue.put(img_copy)
                self.image = None
            time.sleep(0.01)


class FacialDetectorCvNodeAsync(AbstractNodeInterface):
    startValue = ""
    width = 80
    height = 120
    colorTrain = [QColor(255, 234, 242), QColor(255, 91, 110), QColor(142, 255, 242), QColor(218, 255, 251),
                  QColor(110, 255, 91), QColor(170, 61, 73), QColor(52, 19, 23), QColor(142, 255, 242), ]
    logo = r"Release/biggusFolder/imgs/logos/openCvLogo.png"
    output_signal = pyqtSignal(np.ndarray)

    def __init__(self, value=None, inNum=1, outNum=1, parent=None):
        super().__init__(value, inNum, outNum, parent)
        self.setClassName("FacialDetectorCvNode")
        self.setName("FacialDetector")
        self.changeSize(self.width, self.height)
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(r"Release/biggusFolder/dataForTraining/dlib-models-master"
                                              r"/shape_predictor_68_face_landmarks_GTX.dat")
        self.thread = FacialDetectorCvThread(self.detector, self.predictor)
        self.thread.moveToThread(self)
        self.thread.queue = queue.Queue()
        self.thread.start()

    def calculateOutput(self, plugIndex):
        path = self.inPlugs[0].getValue()
        value = self.inPlugs[0].getValue()
        if isinstance(value, np.ndarray):
            self.thread.setImage(value)
            if not self.thread.queue.empty():
                output = self.thread.queue.get()
                self.output_signal.emit(output)
        return self.outPlugs[plugIndex].getValue

    def redesign(self):
        self.changeSize(self.width, self.height)
