from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class sliderBox(QWidget):
    lblName: QLabel  # Name of the slider
    txtValue: QLineEdit  # Value of the slider
    sldValue: QSlider  # Slider
    lblOption1: QLabel  # Label for the first option
    lblOption2: QLabel  # Label for the second option
    lblOption3: QLabel  # Label for the third option

    systemFont = QFont("Arial", 7)
    widgetStyle = f"""
    QSlider::groove:horizontal {{
        border: 1px solid #bbb;
        background: white;
        height: 10px;
        border-radius: 4px;
    }}
    QSlider::handle:horizontal {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #eee, stop:1 #ccc);
        border: 1px solid #777;
        width: 13px;
        margin-top: -2px;
        margin-bottom: -2px;
        border-radius: 4px;
    }}
    QSlider::add-page:horizontal {{
        background: #575757;
    }}
    QSlider::sub-page:horizontal {{
        background: #575757;
    }}
    QSlider::handle:horizontal:hover {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #fff, stop:1 #ddd);
        border: 1px solid #444;
        border-radius: 4px;
    }}
    QSlider::add-page:horizontal:disabled {{
        background: #bbb;
    }}
    """
    labelStyle = "background-color: rgb(90,90, 90); " \
                 "color: (190, 190, 195); " \
                 "border: 1px solid rgb(240,240, " \
                 "245); border-radius: 3px;"

    labelNameStyle = """QLabel {{
        font: bold 7pt Ubuntu;
        
        background-color: rgb(30,30, 30);
        color: white;
    }}"""

    txtEditStyle = f"""QLineEdit {{
        background-color: rgb(50,50, 50);
        border: 1px solid rgb(250,240, 245);
        border-radius: 3px;
        color: white;
    }}"""
    valueChanged = pyqtSignal(int)

    def __init__(self, name, value=None, parent=None):
        super().__init__(parent)
        self.name = name
        if value is None:
            self.value = 0
        self.initUI()

    def initUI(self):
        self.setStyleSheet(self.widgetStyle)
        self.setFont(self.systemFont)
        self.initWidget()
        self.initWidgetSize()
        self.initConnection()

    def initWidget(self):
        # Create the widgets compatible with PyQt6
        self.lblName = QLabel(self.name)
        self.lblName.setStyleSheet(self.labelNameStyle)
        self.txtValue = QLineEdit("")
        self.txtValue.setValidator(QIntValidator())
        self.txtValue.setStyleSheet(self.txtEditStyle)
        self.sldValue = QSlider(Qt.Orientation.Horizontal)
        self.sldValue.setRange(0, (self.value+1)*10)
        self.sldValue.setTickPosition(QSlider.TicksBelow)

        self.lblOption1 = QLabel()
        self.lblOption1.setStyleSheet(self.labelStyle)
        self.lblOption2 = QLabel()
        self.lblOption2.setStyleSheet(self.labelStyle)
        self.lblOption3 = QLabel()
        self.lblOption3.setStyleSheet(self.labelStyle)
        hLayout = QHBoxLayout()
        hLayout.addWidget(self.lblName)
        hLayout.addWidget(self.txtValue)
        hLayout.addWidget(self.sldValue)
        hLayout.addWidget(self.lblOption1)
        hLayout.addWidget(self.lblOption2)
        hLayout.addWidget(self.lblOption3)
        self.setLayout(hLayout)

    def initWidgetSize(self):
        self.lblName.setFixedWidth(56)
        self.txtValue.setFixedWidth(50)
        self.sldValue.setMinimumWidth(200)
        self.sldValue.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.lblOption1.setFixedSize(20, 20)
        self.lblOption2.setFixedSize(14, 14)
        self.lblOption3.setFixedSize(14, 14)

    def initConnection(self):
        self.sldValue.valueChanged.connect(self.onSliderChanged)
        self.sldValue.setValue(self.value)
        self.txtValue.returnPressed.connect(self.onTextChanged)

    def setSliderRange(self, _min, _max):
        self.sldValue.setRange(_min, _max)

    def setValue(self, value):
        self.sldValue.setValue(value)

    def getValue(self):
        return self.sldValue.value()

    def onSliderChanged(self, value):
        self.txtValue.setText(str(value))
        self.valueChanged.emit(value)

    def onTextChanged(self):
        value = self.txtValue.text()
        self.sldValue.setValue(int(value))

    def onOption1Clicked(self, event):
        pass

    def onOption2Clicked(self, event):
        pass

    def onOption3Clicked(self, event):
        pass


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    slider = sliderBox("Test")
    slider.show()
    sys.exit(app.exec())
