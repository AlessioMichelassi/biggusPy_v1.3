from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class superCmb(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.addItem("Style Selector")
        self.addItem("Hide")
        self.addItem("B&W")
        self.show_action = QAction("Hide", self)
        self.show_action.triggered.connect(self.toggleShow)
        self.color_action = QAction("B&W", self)
        self.color_action.triggered.connect(self.toggleColor)
        self.addAction(self.show_action)
        self.addAction(self.color_action)

    def toggleShow(self):
        if self.show_action.text() == "Hide":
            self.show_action.setText("Show")
        else:
            self.show_action.setText("Hide")

    def toggleColor(self):
        if self.color_action.text() == "B&W":
            self.color_action.setText("Color")
        else:
            self.color_action.setText("B&W")


class nodePropertyEditor(QWidget):
    backgroundColor: QColor = QColor(30, 31, 34)
    textColor: QColor = QColor(167, 183, 198)
    systemFont: QFont = QFont("Lohit Gujarati", 12)

    mainLayout: QVBoxLayout
    grpBoxLayout: QVBoxLayout

    grpBox: QGroupBox
    lblLogo: QLabel
    sldWidth: QSlider
    sldHeight: QSlider
    lineTxtWidth: QLineEdit
    lineTxtHeight: QLineEdit
    lineTxtInNumber: QLineEdit
    lineTxtOutNumber: QLineEdit
    sldList: list = []
    lineTxtList: list = []

    isLogoVisible = True
    isLogoBandW = False

    valueChangedInPropertyEditor = pyqtSignal(str, str, name="valueChanged")
    logoChanged = pyqtSignal(str, bool, bool, name="logoChanged")

    _logoPath: str = ""

    def __init__(self, mainWidget, parent=None):
        super().__init__(parent, Qt.WindowType.FramelessWindowHint)
        self.mainWidget = mainWidget
        self.initUI()
        self.initConnections()
        self.setValue(50, 120, 1, 1)
        self.initStyle()

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
        self.setLayout(self.mainLayout)

    def initGrpBox(self):
        self.grpBox = QGroupBox("  Node Property  ")
        self.grpBoxLayout = QVBoxLayout()
        self.grpBoxLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.grpBox.setLayout(self.grpBoxLayout)
        layout1 = self.createWithWidget()
        layout2 = self.createHeightWidget()
        layout3 = self.createLogoWidget()
        self.grpBoxLayout.addLayout(layout1)
        self.grpBoxLayout.addLayout(layout2)
        self.grpBoxLayout.addLayout(layout3)

    def createWithWidget(self):
        """
        Crea un widget per modificare la dimensione del nodo.
        :param name: Nome del widget
        :return: layout
        """
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        lbl = QLabel("Width")
        layout.addWidget(lbl)
        self.sldWidth = QSlider(Qt.Orientation.Horizontal)
        self.sldWidth.setRange(0, 800)
        self.sldList.append(self.sldWidth)
        layout.addWidget(self.sldWidth)
        self.lineTxtWidth = QLineEdit()
        self.lineTxtList.append(self.lineTxtWidth)
        layout.addWidget(self.lineTxtWidth)
        return layout

    def createHeightWidget(self):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        lbl = QLabel("Height")
        layout.addWidget(lbl)
        self.sldHeight = QSlider(Qt.Orientation.Horizontal)
        self.sldHeight.setRange(0, 800)
        self.sldList.append(self.sldHeight)
        layout.addWidget(self.sldHeight)
        self.lineTxtHeight = QLineEdit()
        self.lineTxtList.append(self.lineTxtHeight)
        layout.addWidget(self.lineTxtHeight)
        return layout

    def createInAndOutLineEdits(self):
        layoutIn = QHBoxLayout()
        layoutIn.setAlignment(Qt.AlignmentFlag.AlignLeft)
        lbl = QLabel("In")
        layoutIn.addWidget(lbl)
        self.lineTxtInNumber = QLineEdit()
        layoutIn.addWidget(self.lineTxtInNumber)
        layoutOut = QHBoxLayout()
        lbl = QLabel("Out")
        layoutOut.addWidget(lbl)
        self.lineTxtOutNumber = QLineEdit()
        layoutOut.addWidget(self.lineTxtOutNumber)
        finalLayout = QVBoxLayout()
        finalLayout.addLayout(layoutIn)
        finalLayout.addLayout(layoutOut)
        return finalLayout

    def createLogoWidget(self):
        inAndOutLayout = self.createInAndOutLineEdits()

        self.lblLogo = QLabel()
        self._logoPath = "scratchNodeV0_9/logo/pythonLogo.png"
        self.lblLogo.setPixmap(QPixmap(self._logoPath))
        self.lblLogo.setScaledContents(True)
        self.lblLogo.setFixedWidth(100)
        self.lblLogo.setFixedHeight(100)
        self.lblLogo.setContentsMargins(0, 0, 0, 0)
        self.lblLogo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cmbBoxLogo = superCmb()
        self.cmbBoxLogo.setFixedHeight(30)
        self.cmbBoxLogo.setFixedWidth(100)
        self.cmbBoxLogo.setFont(QFont("Lohit Gujarati", 8))
        self.cmbBoxLogo.setStyleSheet(
            "QComboBox {color: rgb(167, 183, 198); "
            "background-color: rgb(30, 31, 34); "
            "border: 1px solid gray; "
            "border-radius: 5px;}")
        self.cmbBoxLogo.currentIndexChanged.connect(self.onChangeLogoStyle)
        layout = QVBoxLayout()
        layout.addWidget(self.lblLogo)
        layout.addWidget(self.cmbBoxLogo)
        lblLayout = QHBoxLayout()
        spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        lblLayout.addItem(spacer)
        lblLayout.addLayout(layout)
        hLayout = QHBoxLayout()
        hLayout.addLayout(inAndOutLayout)
        hLayout.addLayout(lblLayout)
        return hLayout

    def initStyle(self):
        self.setFont(self.systemFont)
        style = f"""
                    QGroupBox {{
                        color: rgb({self.textColor.red()}, {self.textColor.green()}, {self.textColor.blue()});
                        background-color: rgb({self.backgroundColor.red()}, {self.backgroundColor.green()}, {self.backgroundColor.blue()});
                        border: 1px solid gray;
                        border-radius: 5px;
                        margin-top: 0.5em;
                    }}
            QGroupBox::title {{ 
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 3px;
            }}
            QSlider {{
                    color: rgb({self.textColor.red()}, {self.textColor.green()}, {self.textColor.blue()});
                    border: 0px;
                    background-color: transparent;
            }}
            QSlider::groove:horizontal {{
                border: 1px solid rgb(0, 0, 0);
                height: 4px;
                background: rgb({self.textColor.red()}, {self.textColor.green()}, {self.textColor.blue()});
                margin: 2px 0;
            }}
            QSlider::handle:horizontal {{
                background: rgb({self.textColor.red()}, {self.textColor.green()}, {self.textColor.blue()});
                border: 1px solid #5c5c5c;
                width: 18px;
                margin: -2px 0;
                border-radius: 3px;
            }}

            QLabel {{
                    color: rgb({self.textColor.red()}, {self.textColor.green()}, {self.textColor.blue()});
                    border: 0px;
                    background-color: transparent;
                }}"""
        self.setStyleSheet(style)

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

    def initConnections(self):
        """
        Inizializza le connessioni tra i segnali e i relativi slot.
        :return:
        """
        self.sldWidth.sliderReleased.connect(self.onSldReleased)
        self.sldHeight.sliderReleased.connect(self.onSldReleased)
        self.lineTxtWidth.returnPressed.connect(self.onLineTxtValueChanged)
        self.lineTxtHeight.returnPressed.connect(self.onLineTxtValueChanged)
        self.lineTxtInNumber.returnPressed.connect(self.onLineTxtValueChanged)
        self.lineTxtOutNumber.returnPressed.connect(self.onLineTxtValueChanged)

        self.lblLogo.mouseDoubleClickEvent = self.onLogoDoubleClick

    def setValue(self, width: int, height: int, inNumber: int, outNumber: int):
        """
        Imposta i valori dei widget.
        :param width: larghezza del nodo
        :param height: altezza del nodo
        :param inNumber: numero di ingressi
        :param outNumber: numero di uscite
        :return:
        """
        self.sldWidth.setValue(width)
        self.sldHeight.setValue(height)
        self.lineTxtWidth.setText(str(width))
        self.lineTxtHeight.setText(str(height))
        self.lineTxtInNumber.setText(str(inNumber))
        self.lineTxtOutNumber.setText(str(outNumber))

    def getValue(self):
        """
        Ritorna i valori dei widget.
        :return: width, height, inNumber, outNumber
        """

        width = self.sldWidth.value()
        height = self.sldHeight.value()
        inNumber = int(self.lineTxtInNumber.text())
        outNumber = int(self.lineTxtOutNumber.text())
        logoPath = self.lblLogo.pixmap().cacheKey()
        return width, height, inNumber, outNumber, logoPath

    def onSldReleased(self):
        """
        Slot che viene chiamato quando cambia il valore di uno slider imposta il valore
        nella lineTxt corrispondente.
        :param value: valore dello slider
        :return:
        """
        if self.sender() == self.sldWidth:
            value = self.sldWidth.value()
            self.lineTxtWidth.setText(str(value))
            self.valueChangedInPropertyEditor.emit("Width", str(value))
        elif self.sender() == self.sldHeight:
            value = self.sldHeight.value()
            self.lineTxtHeight.setText(str(value))
            self.valueChangedInPropertyEditor.emit("Height", str(value))

    def onLineTxtValueChanged(self):
        """
        Slot che viene chiamato quando cambia il valore di una lineTxt imposta il valore
        :param value:
        :return:
        """
        sender = self.sender()
        if sender == self.lineTxtWidth:
            value = int(self.lineTxtWidth.text())
            self.sldWidth.setValue(value)
            self.valueChangedInPropertyEditor.emit("Width", str(value))
        elif sender == self.lineTxtHeight:
            value = int(self.lineTxtHeight.text())
            self.sldHeight.setValue(value)
            self.valueChangedInPropertyEditor.emit("Height", str(value))
        elif sender == self.lineTxtInNumber:
            value = int(self.lineTxtInNumber.text())
            self.valueChangedInPropertyEditor.emit("InNumber", str(value))
        elif sender == self.lineTxtOutNumber:
            value = int(self.lineTxtOutNumber.text())
            self.valueChangedInPropertyEditor.emit("OutNumber", str(value))

    def onLogoDoubleClick(self, event):
        """
        Slot che viene chiamato quando viene fatto doppio click sul logo.
        :param event:
        :return:
        """
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")
        if fileName:
            self._logoPath = fileName
            self.lblLogo.setPixmap(QPixmap(fileName))
            self.logoChanged.emit(self._logoPath, self.isLogoVisible, self.isLogoBandW)

    def onChangeLogoStyle(self):
        """
        Slot che viene chiamato quando viene usata la cmbBox
        cmbBox___
                 all'indice 1: mostra il logo
                all'indice 2: B&W
        :return:
        """
        if self.cmbBoxLogo.currentIndex() == 1:
            self.isLogoVisible = not self.isLogoVisible
        elif self.cmbBoxLogo.currentIndex() == 2:
            self.isLogoBandW = not self.isLogoBandW
        elif self.cmbBoxLogo.currentIndex() == 0:
            return
        self.cmbBoxLogo.setCurrentIndex(0)
        self.logoChanged.emit(self._logoPath, self.isLogoVisible, self.isLogoBandW)
