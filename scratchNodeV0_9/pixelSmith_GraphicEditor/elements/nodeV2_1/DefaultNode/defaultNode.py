from PyQt5.QtWidgets import QMenu

from scratchNodeV0_9.pixelSmith_GraphicEditor.elements.nodeV2_1.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface


class DefaultNode(AbstractNodeInterface):
    startValue = 0
    width = 50
    height = 120
    colorTrain = []

    def __init__(self, value= 20, inNum=2, outNum=1, parent=None):
        super().__init__(value, inNum, outNum, parent)
        self.setClassName("DefaultNode")
        self.setName("DefaultNode")
        self.changeSize(self.width, self.height)

    def calculateOutput(self, plugIndex):
        value = self.inPlugs[0].getValue()
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