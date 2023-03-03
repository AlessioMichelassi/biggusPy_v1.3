from elements.Plugs.PlugGraphic import PlugGraphic


class PlugData:
    resetValue = 0
    inConnection = None

    def __init__(self, _type: str, index: int, value: int = 0):
        self.className = _type
        self._name = _type
        self.index = index
        self.resetValue = value
        self._value = self.resetValue
        self.plugGraphic = None

    def __str__(self):
        return f"{self.getTitle}: {self.getValue()}"

    def setName(self, name):
        """
        ITA:
            Questo metodo viene chiamato quando si modifica il nome del plug e aggiorna il testo nella grafica
        ENG:
            This method is called when the name of the plug is modified and updates the text in the graphics
        :param name:
        :return:
        """
        self._name = name
        self.plugGraphic.updateTitle()
        print(f"Plug {self.getTitle()} renamed to {name}!")

    def setNameFromGraphic(self, name):
        """
        ITA:
            Questo metodo viene chiamato quando si modifica il nome del plug dalla finestra di dialogo
            che compare quando si clicca con il tasto destro del mouse sul plug.
        ENG:
            This method is called when the name of the plug is modified from the dialog window
            that appears when you right-click on the plug.
        :param name:
        :return:
        """
        self._name = name

    def resetName(self):
        self._name = self.className

    def getTitle(self):
        return f"{self._name}_{self.index}"

    def getValue(self):
        return self._value

    def setValue(self, value):
        self._value = value
        if self.plugGraphic:
            # aggiorna solo il valore basato sull'out[0]
            if "Out" in self.className and self.index == 0:
                self.plugGraphic.nodeGraphic.setTextValueOnQLineEdit(value)

    def resetPlug(self):
        self._value = self.resetValue

    def createPlugGraphic(self, graphicNode):
        self.plugGraphic = PlugGraphic(self, parent=graphicNode)
        return self.plugGraphic

    def deletePlugGraphic(self):
        self.plugGraphic = None
