import random

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from scratchNodeV0_9.pixelSmith_GraphicEditor.Widgets.colorSmith.tools.colorSimpleWidget import ColorDialogSimple
from scratchNodeV0_9.pixelSmith_GraphicEditor.Widgets.colorSmith.tools.ColorTrainGenerator import ColorTrainGenerator
from scratchNodeV0_9.pixelSmith_GraphicEditor.Widgets.colorSmith.tools.colorButtonSelector import ColorButtonsSelector


class colorToolsWidget(QWidget):
    backgroundColor: QColor = QColor(30, 31, 34)
    textColor: QColor = QColor(167, 183, 198)
    systemFont: QFont = QFont("Lohit Gujarati", 12)

    mainLayout: QVBoxLayout
    grpBoxLayout: QVBoxLayout
    grpBox: QGroupBox

    colorDialog: ColorDialogSimple
    colorTrainGenerator: ColorTrainGenerator
    colorSelector: ColorButtonsSelector
    lblColor: QLabel
    changeOnColorTrainFormColorTools = pyqtSignal(list, name="changeOnColorTrain")

    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowType.FramelessWindowHint)
        self.initUI()
        self.initConnection()
        self.setColorStart(None)

    def setColorStart(self, colorStart: None):
        if colorStart is None:
            colorStart = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.colorDialog.setCurrentColor(colorStart)
        self.colorTrainGenerator.onMonoChromaticColorFromStartingColor(colorStart)

    def initUI(self):
        """
        Inizializza l'interfaccia grafica del widget.
        Crea per prima cosa la grpBox e la mainLayout.
        Quindi crea il colorDialog, i pulsanti per scegliere i colori di partenza
        e i pulsanti per rappresentare i colori.
        :return:
        """
        self.mainLayout = QVBoxLayout()
        self.initGrpBox()

        self.mainLayout.addWidget(self.grpBox, 0, Qt.AlignmentFlag.AlignTop)
        self.initWidgetStyle()
        self.setLayout(self.mainLayout)

        self.initColorDialog()
        self.initColorTrainGenerator()
        self.initColorSelector()
        self.colorTrainGenerator.btnColorWidget = self.colorSelector

    def initGrpBox(self):
        self.grpBox = QGroupBox("  ColorTool  ")
        self.grpBoxLayout = QVBoxLayout()
        self.grpBoxLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.grpBox.setLayout(self.grpBoxLayout)

    def initColorDialog(self):
        """
        Inizializza il colorDialog classico per scegliere i colori.
        :return:
        """
        self.colorDialog = ColorDialogSimple()
        self.grpBoxLayout.addWidget(self.colorDialog, 0,
                                    alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        # la lblColor deve essere allineata centralmente rispetto al gruppo
        self.lblColor = QLabel("")
        self.lblColor.setFixedHeight(20)
        self.lblColor.setFixedWidth(300)
        self.grpBoxLayout.addWidget(self.lblColor, 1,
                                    alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.grpBoxLayout.addStretch(1)
        self.grpBoxLayout.setSpacing(0)

    def initColorTrainGenerator(self):
        """
        Inizializza il colorTrainGenerator per generare i colori.
        :return:
        """
        self.colorTrainGenerator = ColorTrainGenerator(self)
        self.grpBoxLayout.addWidget(self.colorTrainGenerator, 0, alignment=Qt.AlignmentFlag.AlignHCenter)

    def initColorSelector(self):
        self.colorSelector = ColorButtonsSelector()
        self.grpBoxLayout.addWidget(self.colorSelector, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.grpBoxLayout.addStretch(1)
        self.grpBoxLayout.setSpacing(0)

    def initConnection(self):
        """
        Inizializza le connessioni tra i vari widget.
        :return:
        """
        self.colorDialog.currentColorChanged.connect(self.onCurrentColorChanged)
        self.colorTrainGenerator.colorTrainChanged.connect(self.onColorTrainChanged)
        self.colorSelector.currentColorChecked.connect(self.onCurrentColorChecked)
        self.colorSelector.colorSwapSignal.connect(self.onColorSwap)

    def setWidgetColor(self, colorList: list):
        """
        Imposta il colore del widget
        :param colorList[colore di sfondo, colore del testo]
        :return:
        """
        self.backgroundColor = colorList[0]
        self.textColor = colorList[1]

    def initWidgetStyle(self):
        """
        Inizializza lo stile del widget
        :return:
        """
        # la scritta del grpBox ha troppo poco margine a destra
        style = f"""
                    QGroupBox {{
                        color: rgb({self.textColor.red()}, {self.textColor.green()}, {self.textColor.blue()});
                        text-align: vcenter;
                        background-color: rgb({self.backgroundColor.red()}, {self.backgroundColor.green()}, {self.backgroundColor.blue()});
                        border: 1px solid gray;
                        border-radius: 9px;
                        margin-top: 0.5em;
                        text-align: center;
                        }}"""
        self.grpBox.setStyleSheet(style)
        self.setFont(self.systemFont)

    def setSize(self, width: int = None, height: int = None):
        """
        Imposta la dimensione del widget.
        :param width:
        :param height:
        :return:
        """
        if width is not None:
            self.setFixedWidth(width)
        if height is not None:
            self.setFixedHeight(height)

    # #########################################
    #
    #                   SLOTS
    #

    def onCurrentColorChanged(self, color: QColor):
        """
        Slot che viene attivato quando cambia il colore corrente.
        :param color:
        :return:
        """
        self.colorDialog.setCurrentColor(color)
        self.lblColor.setStyleSheet(f"background-color: rgb({color.red()}, {color.green()}, {color.blue()});")
        for btn in self.colorSelector.btnList:
            if btn.isChecked():
                btn.setColor(color)
                self.changeOnColorTrainFormColorTools.emit(self.colorSelector.getColorTrain())

    def onCurrentColorChecked(self, color: QColor):
        """
        Slot che viene attivato quando viene selezionato un colore.
        :param color:
        :return:
        """
        self.colorDialog.setCurrentColor(color)

    def onColorTrainChanged(self, colorTrain: list):
        """
        Slot che viene attivato quando cambia il colorTrain.
        :param colorTrain:
        :return:
        """
        self.colorSelector.setColorTrain(colorTrain)
        self.changeOnColorTrainFormColorTools.emit(colorTrain)

    def onColorSwap(self, colorTrain: list):
        """
        Slot che viene attivato quando viene scambiato un colore con un altro.
        :param colorTrain:
        :return:
        """
        self.colorSelector.setColorTrain(colorTrain)
        self.changeOnColorTrainFormColorTools.emit(colorTrain)
