import random

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class ColorTrainGenerator(QWidget):
    btnRandomizeColor: QPushButton
    btnSaveColor: QPushButton

    btnColorWidgetBorder: QPushButton
    btnColorWidgetText: QPushButton
    btnAnalogousColor: QPushButton
    btnComplementaryColor: QPushButton
    btnTriadicColor: QPushButton
    btnTetradicColor: QPushButton
    btnMonoChromaticColor: QPushButton
    btnTriadColor: QPushButton
    btnCompoundColor: QPushButton
    btnShadesColor: QPushButton
    btnTetradColor: QPushButton
    btnSquareColor: QPushButton

    grpBoxLayout: QVBoxLayout
    colorTrainChanged = pyqtSignal(list, name="colorTrainChanged")
    colorTrain = []

    def __init__(self, colorWidget, parent=None):
        super().__init__(parent)
        self.colorWidget = colorWidget
        self.btnColorWidget = None
        self.initUI()

    def initUI(self):
        self.initBtnColorCreator()
        self.setFixedSize(340,self.sizeHint().height())

    def initBtnColorCreator(self):
        """
        Inizializza i bottoni per la creazione dei colori su un layer di tre righe.
        :return:
        """
        self.grpBoxLayout = QVBoxLayout()
        btn1RowLayout = QHBoxLayout()
        btn2RowLayout = QHBoxLayout()
        btn3RowLayout = QHBoxLayout()
        btn4RowLayout = QHBoxLayout()
        self.btnRandomizeColor = QPushButton("Randomize")
        self.btnRandomizeColor.setFont(QFont("Lohit Gujarati", 8))
        self.btnRandomizeColor.setToolTip("Generate a random color variation.")
        self.btnRandomizeColor.clicked.connect(self.onRandomizeColor)
        self.btnAnalogousColor = QPushButton("Analogous")
        self.btnAnalogousColor.setFont(QFont("Lohit Gujarati", 8))
        self.btnAnalogousColor.setToolTip("Generate a random analogous color variation.")
        self.btnAnalogousColor.clicked.connect(self.onAnalogousColor)
        self.btnMonoChromaticColor = QPushButton("MonoChromatic")
        self.btnMonoChromaticColor.setFont(QFont("Lohit Gujarati", 8))
        self.btnMonoChromaticColor.setToolTip("Generate a random monochromatic color variation.")
        self.btnMonoChromaticColor.clicked.connect(self.onMonoChromaticColor)
        self.btnTriadColor = QPushButton("Triad")
        self.btnTriadColor.setFont(QFont("Lohit Gujarati", 8))
        self.btnTriadColor.setToolTip("Generate a random triad color variation.")
        self.btnTriadColor.clicked.connect(self.onTriadColor)
        self.btnComplementaryColor = QPushButton("Complementary")
        self.btnComplementaryColor.setFont(QFont("Lohit Gujarati", 8))
        self.btnComplementaryColor.setToolTip("Generate a random complementary color variation.")
        self.btnComplementaryColor.clicked.connect(self.onComplementaryColor)
        self.btnCompoundColor = QPushButton("Compound")
        self.btnCompoundColor.setFont(QFont("Lohit Gujarati", 8))
        self.btnCompoundColor.setToolTip("Generate a random compound color variation.")
        self.btnCompoundColor.clicked.connect(self.onCompoundColor)
        self.btnShadesColor = QPushButton("Shades")
        self.btnShadesColor.setFont(QFont("Lohit Gujarati", 8))
        self.btnShadesColor.setToolTip("Generate a random shades color variation.")
        self.btnShadesColor.clicked.connect(self.onShadesColor)
        self.btnTetradColor = QPushButton("Tetrad")
        self.btnTetradColor.setFont(QFont("Lohit Gujarati", 8))
        self.btnTetradColor.setToolTip("Generate a random tetrad color variation.")
        self.btnTetradColor.clicked.connect(self.onTetradColor)
        self.btnSquareColor = QPushButton("Square")
        self.btnSquareColor.setFont(QFont("Lohit Gujarati", 8))
        self.btnSquareColor.setToolTip("Generate a random square color variation.")
        self.btnSquareColor.clicked.connect(self.onSquareColor)

        self.btnSaveColor = QPushButton("Save Color")
        self.btnSaveColor.setFont(QFont("Lohit Gujarati", 8))
        self.btnSaveColor.clicked.connect(self.onSaveColor)
        self.btnSaveColor.setToolTip("Copy the colorSet in the ClipBoardMemory.")
        btn1RowLayout.addWidget(self.btnRandomizeColor)
        btn1RowLayout.addWidget(self.btnAnalogousColor)
        btn1RowLayout.addWidget(self.btnMonoChromaticColor)
        btn2RowLayout.addWidget(self.btnTriadColor)
        btn2RowLayout.addWidget(self.btnComplementaryColor)
        btn2RowLayout.addWidget(self.btnCompoundColor)
        btn3RowLayout.addWidget(self.btnShadesColor)
        btn3RowLayout.addWidget(self.btnTetradColor)
        btn3RowLayout.addWidget(self.btnSquareColor)

        btn4RowLayout.addWidget(self.btnSaveColor)
        self.grpBoxLayout.addLayout(btn1RowLayout)
        self.grpBoxLayout.addLayout(btn2RowLayout)
        self.grpBoxLayout.addLayout(btn3RowLayout)
        self.grpBoxLayout.addLayout(btn4RowLayout)
        self.setLayout(self.grpBoxLayout)

    def onSaveColor(self):
        colorTrain = self.btnColorWidget.getColorTrain()
        colorTrainStr = ""
        colorTrainStr += f"colorObject: QColor = QColor{colorTrain[0].getRgb()}\n"
        colorTrainStr += f"colorBorderDefault: QColor = QColor{colorTrain[1].getRgb()}\n"
        colorTrainStr += f"colorBorderSelected: QColor = QColor{colorTrain[2].getRgb()}\n"
        colorTrainStr += f"colorBorderHover: QColor = QColor{colorTrain[3].getRgb()}\n"
        colorTrainStr += f"colorText: QColor = QColor{colorTrain[4].getRgb()}\n"
        colorTrainStr += f"colorTextFill: QColor = QColor{colorTrain[5].getRgb()}\n"
        colorTrainStr += f"colorTextSelected: QColor = QColor{colorTrain[6].getRgb()}\n"
        colorTrainStr += f"colorTextHover: QColor = QColor{colorTrain[7].getRgb()}\n"

        clipboard = QApplication.clipboard()
        clipboard.setText(colorTrainStr)

    @staticmethod
    def calculateAnalogousDegree(degrees: int, variance: int):
        """
        Calcola la rotazione che deve fare nella palette di colori
        per ottenere il colore successivo in base alla varianza
        se il valore dei gradini supera i 360 gradi, allora resetta
        i gradi a 0 perchè valore negativi o superiori a 360 non vengono
        accettati da QColor.fromHsv
        :param degrees:
        :param variance:
        :return:
        """
        # se sommando variance a degrees supera i 360 gradi, allora resetto degrees a 0
        # e calcola l'avanzo di variance che non è stato utilizzato
        if degrees + variance > 360:
            variance = degrees + variance - 360
            degrees = 0 + variance
        elif degrees + variance < 0:
            variance = degrees + variance + 360
            degrees = 360 - variance
        return degrees + variance

    @staticmethod
    def complementaryColor(color: QColor, degrees: int = 180):
        """
        Calcola il colore complementare di un colore
        :param degrees: di quanti gradi deve ruotare il colore. 180 gradi trova il complementare
        :param color: colore di partenza
        :return: colore complementare
        """
        hue = color.hue()
        hue = (hue + degrees) % 360
        return QColor.fromHsv(hue, color.saturation(), color.value())

    @staticmethod
    def invertColor(color: QColor):
        return QColor(255 - color.red(), 255 - color.green(), 255 - color.blue())

    @staticmethod
    def prevent_RGB_OutOfRange(color: QColor):
        """
        Controlla che i valori dei colori siano compresi tra 0 e 255
        :param color:
        :return:
        """
        red = max(0, min(color.red(), 200))
        green = max(0, min(color.green(), 200))
        blue = max(0, min(color.blue(), 200))
        return QColor(red, green, blue)

    @staticmethod
    def prevent_HSV_OutOfRange(value: int):
        if value > 360:
            return value - 360
        elif value < 0:
            return 360 + value
        return value

    def onRandomizeColor(self):
        self.colorTrain = []
        for _ in range(8):
            color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.colorTrain.append(color)
        self.colorTrainChanged.emit(self.colorTrain)

    def onAnalogousColor(self):
        """
        Genera una palette di colori analoghi. I colori analogi sono colori che si trovano
        vicini tra loro nella palette di colori. Si può immaginare una curva che parte da
        un colore e che si allontana da esso di una certa varianza. I colori analoghi sono
        colori che si trovano sulla curva. In base alla funzione che avranno i colori
        Testo, piuttosto che sfondo, sono stati resi più o meno luminosi.
        :return:
        """
        degreesStart = random.randint(0, 360)
        variance = 15
        saturationStart = 150
        valueStart = 200
        self.colorTrain = []
        for _ in range(8):
            color = QColor.fromHsv(degreesStart, saturationStart, valueStart)
            self.colorTrain.append(color)
            degreesStart = self.calculateAnalogousDegree(degreesStart, variance)

        self.colorTrain[0] = self.colorTrain[0].darker(150)
        self.colorTrain[4] = self.colorTrain[1].lighter(150)
        self.colorTrain[6] = self.colorTrain[1].darker(150)
        self.colorTrainChanged.emit(self.colorTrain)

    def onMonoChromaticColor(self):
        """
        Genera una palette di colori monocromatici, ovvero partendo da un colore
        si genera una serie di colori che si differenziano per la luminosità in
        base alla funzione che avranno i colori Testo, piuttosto che sfondo.
        :return:
        """
        startColor = QColor(random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
        colorBorder = startColor.darker(150)
        colorBorderSelected = startColor.lighter(130)
        colorBorderHover = startColor.lighter(150)
        colorText = startColor.lighter(180)
        colorProxyFill = startColor.darker(120)
        colorProxyBorder = startColor.darker(150)
        colorProxyBorderSelected = startColor.lighter(130)
        self.colorTrain = [startColor, colorBorder, colorBorderSelected, colorBorderHover, colorText, colorProxyFill,
                      colorProxyBorder, colorProxyBorderSelected]
        self.colorTrainChanged.emit(self.colorTrain)

    def onMonoChromaticColorFromStartingColor(self, startColor: QColor):
        """
        Genera una palette di colori monocromatici, partendo da un colore
        :return:
        """
        startColor = startColor
        colorBorder = startColor.darker(150)
        colorBorderSelected = startColor.lighter(130)
        colorBorderHover = startColor.lighter(150)
        colorText = startColor.lighter(180)
        colorProxyFill = startColor.darker(120)
        colorProxyBorder = startColor.darker(150)
        colorProxyBorderSelected = startColor.lighter(130)
        self.colorTrain = [startColor, colorBorder, colorBorderSelected, colorBorderHover, colorText, colorProxyFill,
                      colorProxyBorder, colorProxyBorderSelected]
        self.colorTrainChanged.emit(self.colorTrain)

    def onTriadColor(self):
        colors = [QColor(255, 0, 0), QColor(255, 128, 0), QColor(255, 255, 0),
                  QColor(0, 255, 0), QColor(0, 255, 255), QColor(0, 0, 255),
                  QColor(128, 0, 255), QColor(255, 0, 255)]

        startColor = colors[random.randint(0, 7)]
        # trova i colori basandosi un ipotetico triangolo equilatero
        # in cui il colore di partenza è il vertice
        vertex1 = self.calculateAnalogousDegree(startColor.hue(), 30)
        vertex2 = self.calculateAnalogousDegree(startColor.hue(), 90)
        vertex3 = self.calculateAnalogousDegree(startColor.hue(), 150)

        # filtra i parametri in modo da non avere QColor::fromHsv: HSV parameters out of range

        vertex1 = self.prevent_HSV_OutOfRange(vertex1)
        vertex2 = self.prevent_HSV_OutOfRange(vertex2)
        vertex3 = self.prevent_HSV_OutOfRange(vertex3)
        color1 = QColor.fromHsv(vertex1, 80, 120)
        color2 = QColor.fromHsv(vertex2, 80, 120)
        color3 = QColor.fromHsv(vertex3, 80, 120)

        colorBorder = color1.darker(150)
        colorBorderSelected = color1.lighter(130)
        colorBorderHover = color1.lighter(150)
        colorText = color2.lighter(180)
        colorProxyFill = color3.darker(120)
        colorProxyBorder = color1.darker(150)
        colorProxyBorderSelected = color1.lighter(130)
        self.colorTrain = [color1, colorBorder, colorBorderSelected, colorBorderHover, colorText, colorProxyFill,
                      colorProxyBorder, colorProxyBorderSelected]
        self.colorTrainChanged.emit(self.colorTrain)

    def onComplementaryColor(self):
        """
        Genera una palette di colori complementari, la palette dei primi 4 colori
        si differenzia in base alla luminosità, mentre la palette dei colori successivi
        viene invertita utilizzando come colore di artenza il colore complementare.
        :return:
        """
        startColor = QColor(random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
        colorBorder = self.invertColor(startColor).darker(150)
        colorBorderSelected = startColor.lighter(130)
        colorBorderHover = startColor.lighter(150)
        colorText = self.invertColor(startColor).lighter(180)
        colorProxyFill = self.invertColor(startColor).darker(150)
        colorProxyBorder = colorProxyFill.darker(120)
        colorProxyBorderSelected = self.invertColor(startColor).lighter(180)
        self.colorTrain = [startColor, colorBorder, colorBorderSelected, colorBorderHover, colorText, colorProxyFill,
                      colorProxyBorder, colorProxyBorderSelected]
        self.colorTrainChanged.emit(self.colorTrain)

    def onCompoundColor(self):
        """
        L'algoritmo di "Compound Color" di Adobe Color Wheel si basa sulla scelta di tre colori distinti,
        di cui il primo è il colore principale e gli altri due sono i colori complementari. Questi colori
        complementari sono selezionati in modo tale che siano posizionati alle estremità del segmento opposto del
        cerchio cromatico rispetto al colore principale.

        Successivamente, l'algoritmo sceglie un quarto colore, noto come "accent color", che si trova a circa 120 gradi
        sul cerchio cromatico dal colore principale. Questo colore è scelto per creare un effetto visivo di contrasto
        con i colori complementari.

        Infine, l'algoritmo di Adobe Color Wheel utilizza un quinto colore come sfondo, selezionato in modo tale da
        armonizzare con gli altri quattro colori scelti in precedenza.

        In sintesi, l'algoritmo di "Compound Color" di Adobe Color Wheel si basa sull'utilizzo di colori complementari
        e un colore di accento, scelti in modo tale da creare un effetto visivo di contrasto, insieme ad un colore di
        sfondo per completare l'armonia complessiva del set di colori scelti.
        """
        colorStart = QColor(random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
        colorStart.setHsv(colorStart.hue(), colorStart.saturation(), 255)
        colorStart.setAlpha(255)
        complement1 = self.complementaryColor(colorStart, 180)
        complement2 = self.complementaryColor(colorStart, -180)
        accentColor = self.complementaryColor(colorStart, 120)
        backgroundColor = colorStart.darker(150)

        self.colorTrain = [colorStart, complement1, complement1.lighter(120), complement1.lighter(150), accentColor,
                      backgroundColor, complement2, complement2.lighter(120), complement2.lighter(150)]
        self.colorTrainChanged.emit(self.colorTrain)

    def onShadesColor(self):
        """
        L'algoritmo di "Shades Color" si basa sulla scelta di due colori principali uno per i primi quattro e
        uno per i secondi 4  e di una serie di colori derivati da essi ottenuti attraverso
        la modifica della luminosità del colore principale.
        :return:
        """
        firstColor = QColor(random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
        firstColor.setHsv(firstColor.hue(), firstColor.saturation(), 255)
        firstColor.setAlpha(255)
        secondColor = self.complementaryColor(firstColor, 180)
        self.colorTrain = [firstColor, firstColor.darker(180), firstColor.lighter(120), firstColor.lighter(150),
                      secondColor, secondColor.darker(180), secondColor.lighter(120), secondColor.lighter(150)]
        self.colorTrainChanged.emit(self.colorTrain)

    def onTetradColor(self):
        """
        L'algoritmo di "Tetrad Color" si basa sulla scelta di quattro colori distinti, di cui il primo è il colore
        principale e gli altri tre sono i colori complementari. Questi colori complementari sono selezionati in modo
        tale che siano posizionati alle estremità del segmento opposto del cerchio cromatico rispetto al colore
        principale.
        :return:
        """
        colorStart = QColor(random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
        colorStart.setHsv(colorStart.hue(), colorStart.saturation(), 255)
        colorStart.setAlpha(255)
        complement1 = self.complementaryColor(colorStart, 180)
        complement2 = self.complementaryColor(colorStart, -180)
        complement3 = self.complementaryColor(colorStart, 90)

        colorStart2 = QColor(random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
        colorStart2.setHsv(colorStart2.hue(), colorStart2.saturation(), 255)
        colorStart2.setAlpha(255)
        complement4 = self.complementaryColor(colorStart2, 180)
        complement5 = self.complementaryColor(colorStart2, -180)
        complement6 = self.complementaryColor(colorStart2, 90)
        self.colorTrain = [colorStart, complement1, complement2,
                      complement3, colorStart2, complement4, complement5, complement6]
        self.colorTrainChanged.emit(self.colorTrain)

    def onSquareColor(self):
        """
        L'algoritmo di "Square Color" si basa sulla scelta di otto colori distinti, partend0 da un colore principale
        i primi quattro colori sono i colori spostati di 90 gradi sul cerchio cromatico, mentre gli ultimi quattro

        di cui il primo è il colore principale e gli altri tre sono i colori complementari. Questi colori
        :return:
        """
        colorStart = QColor(random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
        colorStart.setHsv(colorStart.hue(), colorStart.saturation(), 255)
        colorStart.setAlpha(255)
        firstVertex = self.complementaryColor(colorStart, 90)
        secondVertex = self.complementaryColor(firstVertex, 90)
        thirdVertex = self.complementaryColor(secondVertex, 90)
        complement1 = self.complementaryColor(colorStart, 45)
        compVertex1 = self.complementaryColor(complement1, 90)
        compVertex2 = self.complementaryColor(compVertex1, 90)
        compVertex3 = self.complementaryColor(compVertex2, 90)

        self.colorTrain = [colorStart, firstVertex, secondVertex, thirdVertex, complement1, compVertex1, compVertex2,
                      compVertex3]
        self.colorTrainChanged.emit(self.colorTrain)