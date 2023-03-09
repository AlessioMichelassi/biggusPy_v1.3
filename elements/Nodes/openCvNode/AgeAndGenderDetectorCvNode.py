import cv2
import numpy as np
from PyQt5.QtCore import QDir
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMenu, QFileDialog
import cv2 as cv
import sys
from elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
GENDER_LIST = ['F', 'M']
AGE_LIST = ['(0, 2)', '(4, 6)', '(8, 12)', '(15, 20)', '(25, 32)', '(38, 43)', '(48, 53)', '(60, 100)']
GENDER_MODEL = "Release/biggusFolder/dataForTraining/gender_net.caffemodel"
GENDER_PROTOTXT = "Release/biggusFolder/dataForTraining/deploy_gender.prototxt"
AGE_MODEL = "Release/biggusFolder/dataForTraining/age_net.caffemodel"
AGE_PROTOTXT = "Release/biggusFolder/dataForTraining/deploy_age.prototxt"


class AgeAndGenderDetectorCvNode(AbstractNodeInterface):
    startValue = ""
    width = 80
    height = 120
    colorTrain = [QColor(255, 234, 242), QColor(255, 91, 110), QColor(142, 255, 242), QColor(218, 255, 251),
                  QColor(110, 255, 91), QColor(170, 61, 73), QColor(52, 19, 23), QColor(142, 255, 242), ]
    logo = r"Release/biggusFolder/imgs/logos/openCvLogo.png"

    def __init__(self, value=0, inNum=1, outNum=1, parent=None):
        super().__init__(value, inNum, outNum, parent)
        self.setClassName("AgeGenderDetectorCvNode")
        self.setName("AgeGenderDetector")
        self.changeSize(80, 120)
        self.model = cv2.dnn.readNetFromCaffe(GENDER_PROTOTXT, GENDER_MODEL)
        self.age_model = cv2.dnn.readNetFromCaffe(AGE_PROTOTXT, AGE_MODEL)

    def calculateOutput(self, plugIndex):
        img = self.inPlugs[0].getValue()
        if isinstance(img, np.ndarray):
            # convert the image to a blob
            blob = cv2.dnn.blobFromImage(img, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)

            # classify gender
            self.model.setInput(blob)
            gender_preds = self.model.forward()
            gender = GENDER_LIST[gender_preds[0].argmax()]

            # classify age
            self.age_model.setInput(blob)
            age_preds = self.age_model.forward()
            age = AGE_LIST[age_preds[0].argmax()]
            outValue = f"{gender}, {age}"
            self.outPlugs[plugIndex].setValue(outValue)
            self.updateAll()
        return self.outPlugs[plugIndex].getValue()
