from PyQt5.QtCore import QDir, pyqtSignal, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMenu, QFileDialog, QWidget, QHBoxLayout, QComboBox
import cv2
import dlib
import numpy as np
import sys
from elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface


class FacialDetectorCvNode(AbstractNodeInterface):
    startValue = ""
    width = 80
    height = 120
    colorTrain = [QColor(255, 234, 242),QColor(255, 91, 110),QColor(142, 255, 242),QColor(218, 255, 251),QColor(110, 255, 91),QColor(170, 61, 73),QColor(52, 19, 23),QColor(142, 255, 242),]
    logo = r"Release/biggusFolder/imgs/logos/openCvLogo.png"

    def __init__(self, value=None, inNum=1, outNum=1, parent=None):
        super().__init__(value, inNum, outNum, parent)
        self.setClassName("FacialDetectorCvNode")
        self.setName("FacialDetector")
        self.changeSize(self.width, self.height)
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(r"Release/biggusFolder/dataForTraining/dlib-models-master"
                                              r"/shape_predictor_68_face_landmarks_GTX.dat")

    def calculateOutput(self, plugIndex):
        path = self.inPlugs[0].getValue()
        value = self.inPlugs[0].getValue()
        if isinstance(value, np.ndarray):
            outValue = self.returnFace(value)
            self.outPlugs[plugIndex].setValue(outValue)
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

    def returnFace(self, npArray):
        gray = cv2.cvtColor(npArray, cv2.COLOR_BGR2GRAY)
        faces = self.detector(npArray, 0)

        # Draw rectangles around detected faces and return the image
        img_copy = npArray.copy()
        for face in faces:
            x1, y1, x2, y2 = face.left(), face.top(), face.right(), face.bottom()
            cv2.rectangle(img_copy, (x1, y1), (x2, y2), (0, 255, 0), 2)
        return img_copy

