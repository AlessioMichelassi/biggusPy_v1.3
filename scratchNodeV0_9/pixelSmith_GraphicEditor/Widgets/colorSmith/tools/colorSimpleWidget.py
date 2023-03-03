from PyQt5.QtWidgets import QColorDialog, QWidget


class ColorDialogSimple(QColorDialog):
    def __init__(self, parent=None, start_color=None):
        super().__init__(parent)
        self.setOptions(self.options() | QColorDialog.ColorDialogOption.DontUseNativeDialog)
        self.setStyleSheet("QColorDialog {background-color: transparent;}")
        for children in self.findChildren(QWidget):
            className = children.metaObject().className()
            if className not in ("QColorPicker", "QColorLuminancePicker"):
                children.hide()

        if start_color:
            self.setCurrentColor(start_color)
