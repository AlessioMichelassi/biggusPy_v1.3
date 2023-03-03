from scratchNodeV0_9.ArguePy_CodeEditor.editorWidgetTool.tools.codeEditor import *


class ArguePy(QWidget):
    colorList = []
    mainLayout = None
    fileName = "untitled"

    def __init__(self, parent=None):
        super(ArguePy, self).__init__(parent)
        self.codeEditor = pythonCodeEditor(self)
        self.searchWidget = searchAndReplaceWidget(self.codeEditor)
        self.pythonHighlighter = self.codeEditor.pythonHighlighter

        self.initUI()
        self.initConnection()

    def initUI(self):
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.codeEditor)
        self.mainLayout.addWidget(self.searchWidget)
        self.searchWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.mainLayout.setContentsMargins(10, 20, 10, 5)
        self.searchWidget.hide()
        self.setLayout(self.mainLayout)

    def initColorList(self):
        SyntaxHighlighter = self.codeEditor.pythonHighlighter
        self.colorList = [SyntaxHighlighter.keywordColor, SyntaxHighlighter.functionColor,
                          SyntaxHighlighter.builtInColor, SyntaxHighlighter.functionColor,
                          SyntaxHighlighter.selfColor, SyntaxHighlighter.classFunctionColor,
                          SyntaxHighlighter.methodColor, SyntaxHighlighter.braceColor,
                          SyntaxHighlighter.numberColor, SyntaxHighlighter.stringColor,
                          SyntaxHighlighter.commentColor, SyntaxHighlighter.comment2Color]

    def initConnection(self):
        pass

    def setCode(self, code):
        self.codeEditor.setPlainText(code)

    def getCode(self):
        return self.codeEditor.toPlainText()

    def changeColor(self, color, name):
        txt = self.codeEditor.toPlainText()
        self.codeEditor.clear()
        self.pythonHighlighter.setColor(color, name)
        self.codeEditor.insertPlainText(txt)
        self.pythonHighlighter.highlightBlock(self.codeEditor.toPlainText())

    def onNew(self):
        """
        Questo metodo viene chiamato quando si clicca su new
        :return:
        """
        self.fileName = "untitled"
        self.codeEditor.clear()

    def onOpen(self):
        """
        Questo metodo carica il codice dal file con una qDialog
        :return:
        """

        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")
        if fileName:
            self.onNew()
            with open(fileName, "r") as file:
                self.codeEditor.setPlainText(file.read())
                self.fileName = fileName

    def onSave(self):
        """
        Questo metodo salva il codice nel file con una qDialog
        :return:
        """
        if self.fileName == "untitled":
            self.onSaveAs()
        else:
            with open(self.fileName, "w") as file:
                file.write(self.codeEditor.toPlainText())

    def onSaveAs(self):
        """
        Questo metodo salva il codice nel file con una qDialog
        :return:
        """
        fileName, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Python Files (*.py)")
        if fileName:
            with open(fileName, "w") as file:
                file.write(self.codeEditor.toPlainText())

    def onPreferences(self):
        """
        Questo metodo mostra il widget per cambiare i colori
        :return:
        """
        self.colorWidget.show()

    def onRun(self):
        """
        Questo metodo esegue il codice
        :return:
        """
        try:
            exec(self.codeEditor.toPlainText())
        except Exception as e:
            print(e)
