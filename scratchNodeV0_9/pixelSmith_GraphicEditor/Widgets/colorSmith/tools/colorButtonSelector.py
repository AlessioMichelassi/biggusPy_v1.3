from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from scratchNodeV0_9.pixelSmith_GraphicEditor.Widgets.colorSmith.tools.roundBtn import RoundButton

"""
    Crea un gruppo di pulsanti per selezionare quale colore può essere modificato. 
    Consiste in una griglia due righe di 4 pulsanti ciascuna, ognuno dei quali ha una label che ne indica il nome. 
    Ogni pulsante è associato al colore di una parte del nodo, quindi cliccando su un pulsante viene abilitata 
    la modifica del colore di quella determinata parte. 
    
    Se il pulsante è abilitato tutti gli altri sono disabilitati, questo perchè è possibile cambiare il colore 
    del pulsante selezionato, con un override della finestra QDialog. 
    Se tutti i pulsanti sono disabilitati, allora è possibile cambiare il colore a tutti i pulsanti tramite 
    un altro selezionatore (colorTrainGenerator) che usa vari algoritmi per determinare i colori.
    
    Si può trascinare un colore da un pulsante a un altro e viceversa. Il pulsante selezionato viene utilizzato
    per settare il colore di partenza nell'override della QDialog.
"""


class ColorButtonsSelector(QWidget):
    btnList = []
    lblList = []
    colorSelectObj = None
    colorSwapObj = None
    colorFillObj = None
    colorCopy = None

    font = QFont("Lohit Gujarati", 8)
    currentColorChecked = pyqtSignal(QColor, name="currentColorChecked")
    currentBtnActive = pyqtSignal(int, name="currentBtnActive")
    canAcceptDict = {0: True, 1: True, 2: True, 3: True, 4: True, 5: True, 6: True, 7: True}
    colorSwapSignal = pyqtSignal(list, name="colorSwapSignal")

    def __init__(self, parent=None):
        super(ColorButtonsSelector, self).__init__(parent, Qt.WindowFlags())
        self.initUI()
        self.initConnection()
        self.setAcceptDrops(True)
        self.setFont(self.font)
        self.styleLblDefault = f"""
                    QLabel {{
                        background-color: transparent;
                        font-family: {self.font.family()};
                        font-size: {self.font.pointSize()}pt;
                        font-weight: normal;
                        color: rgb(100,100,100);
                    }}"""
        self.initStyle()

    def initUI(self):
        """
        Inizializza l'interfaccia grafica del widget creando una griglia di pulsanti
        e label, ognuno dei quali rappresenta un colore.
        :return:
        """
        gridLayout = QGridLayout()
        self.createButtons()
        for i in range(8):
            vLayout = QVBoxLayout()
            vLayout.addWidget(self.btnList[i], alignment=Qt.AlignmentFlag.AlignCenter)
            vLayout.addWidget(self.lblList[i], alignment=Qt.AlignmentFlag.AlignCenter)
            gridLayout.addLayout(vLayout, i // 4, i % 4)
        self.setLayout(gridLayout)

    def initConnection(self):
        """
        Inizializza le connessioni tra i pulsanti.
        Toggled è il segnale emesso quando un pulsante viene selezionato o deselezionato.
        Si usa per disabilitare tutti gli altri pulsanti.
        btColorChanged è il segnale emesso quando nel caso un cui un pulsante
        è selezionato, viene cambiato il colore, tramite trainGenerator o colorDialog.
        Quando un pulsante cambia colore, viene emesso un segnale con il cambio si
        colorTrain in modo che i colori possano essere associati al nodo nel grafico.
        :return:
        """
        for btn in self.btnList:
            btn.toggled.connect(self.btnToggled)
            btn.btnColorChanged.connect(self.onBtnColorChanged)

    def initStyle(self):
        for i in range(8):
            self.lblList[i].setStyleSheet(self.styleLblDefault)

    def createButtons(self):
        btnNameList = ["fill", "borderDefault", "borderSelected", "borderHover", "text", "ProxyFill", "ProxyBorder",
                       "ProxyBorderSelected"]
        self.btnList = []
        for i in range(8):
            btn = RoundButton(self, btnNameList[i])
            btn.name = btnNameList[i]
            lblName = btn.name
            if len(lblName) < 6:
                addSpace = (14 - len(lblName)) // 2
                lblName = f"{'  ' * addSpace}{lblName}{'  ' * addSpace}"

            lbl = QLabel(lblName)
            lbl.setObjectName(btn.name)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.btnList.append(btn)
            self.lblList.append(lbl)

    def btnToggled(self):
        """
        Quando un pulsante viene selezionato diventa l'unico pulsante che può cambiare colore,
        allora tutti gli altri pulsanti vengono deselezionati.
        Ma se l'unico pulsante selezionato viene deselezionato, allora tutti i pulsanti vengono
        abilitati a ricevere il colore.
        :param checked:
        :return:
        """
        if self.sender().isChecked():
            self.sender().canAcceptColor = True
            self.currentColorChecked.emit(self.sender().getColor())
            for btn in self.btnList:
                if btn != self.sender():
                    btn.setChecked(False)
                    btn.canAcceptColor = False

        else:
            for btn in self.btnList:
                btn.canAcceptColor = True

    def onBtnColorChanged(self, color):
        for btn in self.btnList:
            if btn.isChecked():
                btn.setColor(color)

    # ###################################################
    #
    #           Buttons Color
    #

    def setColorTrain(self, colorTrain: list):
        for i in range(8):
            if self.btnList[i].canAcceptColor:
                self.btnList[i].setColor(colorTrain[i])

    def getColorTrain(self):
        colorTrain = []
        for btn in self.btnList:
            colorTrain.append(btn.getColor())
        return colorTrain

    # ###################################################
    #
    #
    #  Override di metodi per gestire il drag and drop
    #
    #
    # ###################################################

    def mousePressEvent(self, event: QMouseEvent):
        """
            Se il mouse viene premuto su un pulsante, allora il colorFill del pulsante
            viene messo nella variabile colorSelector. Questa variabile viene utilizzata
            per fare lo scambio dei colori nel caso in cui si trascini un colore da un
            pulsante a un altro. Il colore del pulsante su cui viene trascinato il colore
            viene messo nella variabile colorSwap. Come nel problema della torre di Hanoi,
            abbiamo bisogno di una terza variabile: colorDestination.
        """
        super().mousePressEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            # se l'oggetto cliccato è un pulsante
            self.onLMBPressed(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        super().mouseReleaseEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            self.onLMBReleased(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        super().mouseMoveEvent(event)
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.onLMBMove(event)

    def onLMBPressed(self, event: QMouseEvent):
        self.setCursor(Qt.CursorShape.OpenHandCursor)
        # il pulsante selezionato
        btn = self.childAt(event.pos())
        if isinstance(btn, RoundButton):
            self.colorSelectObj = btn
            self.colorSwapObj = None
            self.colorFillObj = None

    def onLMBReleased(self, event: QMouseEvent):
        self.setCursor(Qt.CursorShape.ArrowCursor)
        btn = self.childAt(event.pos())
        if isinstance(btn, RoundButton):
            self.colorFillObj = btn
            self.swapColors()

    def onLMBMove(self, event: QMouseEvent):
        self.setCursor(Qt.CursorShape.ClosedHandCursor)
        btn = self.childAt(event.pos())
        if isinstance(btn, RoundButton):
            self.colorSwapObj = btn
            self.colorFillObj = None

    def swapColors(self):
        self.changeAcceptOnBtn(True)
        selectColor = self.colorSelectObj.getColor()
        swapColor = self.colorSwapObj.getColor()
        fillColor = self.colorFillObj.getColor()
        self.colorFillObj.setColor(selectColor)
        self.colorSelectObj.setColor(swapColor)
        self.changeAcceptOnBtn(False)
        self.colorSwapSignal.emit(self.getColorTrain())

    def changeAcceptOnBtn(self, boolean: bool):
        self.colorSwapObj.canAcceptColor = boolean
        self.colorSelectObj.canAcceptColor = boolean
        self.colorFillObj.canAcceptColor = boolean

    def contextMenuEvent(self, event) -> None:
        """
        ITA:
            Dal menu contestuale è possibile fare il copia incolla dei colori.
            Copia, mette in memoria il colore su cui è stato cliccato con il tasto destro,
            e incolla, sostituisce il colore del pulsante su cui è stato cliccato con il tasto destro
        :param event:
        :return:
        """
        menu = QMenu(self)
        copyAction = menu.addAction("Copy")
        pasteAction = menu.addAction("Paste")
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == copyAction:
            btn = self.childAt(event.pos())
            if isinstance(btn, RoundButton):
                self.colorCopy = btn.getColor()
        elif action == pasteAction:
            btn = self.childAt(event.pos())
            if isinstance(btn, RoundButton):
                btn.setColor(self.colorCopy)
                self.colorSwapSignal.emit(self.getColorTrain())
