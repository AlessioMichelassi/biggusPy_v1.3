from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from scratchNodeV0_9.ArguePy_CodeEditor.editorWidgetTool.tools.SintaxHighlighters.pyHighLighter import pythonHighLighter
from scratchNodeV0_9.ArguePy_CodeEditor.editorWidgetTool.tools.lineNumberWidget import LineNumberArea


class searchAndReplaceWidget(QWidget):
    grpBox: QGroupBox
    mainLayout: QVBoxLayout

    # VARIABLES FOR SEARCH
    lblSearch: QLabel
    vSpacer: QSpacerItem
    chkCaseSensitive: QCheckBox
    chkWholeWord: QCheckBox
    btnUseRegex: QCheckBox

    txtSearch: QLineEdit
    btnSearch: QPushButton
    searchLayout: QVBoxLayout
    layoutSearchText: QHBoxLayout
    layoutSearchLabel: QHBoxLayout

    # VARIABLES FOR REPLACE
    lblReplace: QLabel
    txtReplace: QLineEdit
    btnReplace: QPushButton
    btnReplaceAll: QPushButton
    replaceLayout: QVBoxLayout
    layoutReplaceText: QHBoxLayout
    layoutReplaceLabel: QHBoxLayout

    foundWordsList = []

    def __init__(self, editor: 'pythonCodeEditor', parent=None):
        QWidget.__init__(self, parent)

        self.editor = editor
        self.initUI()
        self.initStyle()
        self.initConnections()
        self.setMaximumHeight(200)

    def initUI(self):
        """
        Inizializza l'interfaccia
        :return:
        """
        # mette i layout di search e replace in una group Box
        self.grpBox = QGroupBox("Search and Replace")

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.grpBox)
        # crea i layout per search e replace
        self.SearchAndReplaceLayout()

        self.grpBox.setLayout(self.layoutMain)
        self.grpBox.setMinimumWidth(self.editor.width() - 20)
        self.setLayout(self.mainLayout)

    def createSearchBox(self):
        """
        Crea il blocco per la ricerca del testo
        :return:
        """
        closeButton = QPushButton(QIcon('close.png'), 'X')
        closeButton.setFixedSize(10, 10)
        closeButton.setStyleSheet('''
                            QPushButton {
                                border: none;
                                background-color: transparent;
                            }
                            QPushButton:hover {
                                background-color: #f0f0f0;
                            }
                        ''')
        closeButton.clicked.connect(self.close)
        closeLayout = QHBoxLayout()
        closeLayout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))
        closeLayout.addStretch()
        closeLayout.setContentsMargins(0, 0, 0, 0)
        closeLayout.addWidget(closeButton)
        self.lblSearch = QLabel("Search")
        self.vSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.chkCaseSensitive = QCheckBox("case Sensitive")
        self.chkCaseSensitive.setToolTip("means that if you search for \"test\", it will not match \"Test\".")
        self.chkWholeWord = QCheckBox("Whole Word")
        self.chkWholeWord.setToolTip("means that if you search for \"test\", it will not match \"testing\".")

        self.btnUseRegex = QCheckBox("Regex")
        self.btnUseRegex.setDisabled(True)
        # create layout
        self.layoutSearchLabel = QHBoxLayout()
        self.layoutSearchLabel.addWidget(self.lblSearch)
        self.layoutSearchLabel.addSpacerItem(self.vSpacer)
        self.layoutSearchLabel.addWidget(self.chkCaseSensitive)
        self.layoutSearchLabel.addWidget(self.chkWholeWord)
        self.layoutSearchLabel.addWidget(self.btnUseRegex)

        self.txtSearch = QLineEdit()
        self.txtSearch.setPlaceholderText("Search")
        self.txtSearch.setFixedHeight(30)
        self.btnSearch = QPushButton("Search")
        self.btnSearch.setFixedWidth(80)
        self.btnSearch.setFixedHeight(30)
        self.btnPrev = QPushButton("Prev")
        self.btnPrev.setFixedWidth(50)
        self.btnPrev.setFixedHeight(30)
        self.btnNext = QPushButton("Next")
        self.btnNext.setFixedWidth(50)
        self.btnNext.setFixedHeight(30)
        self.layoutSearchText = QHBoxLayout()
        self.layoutSearchText.addWidget(self.txtSearch)
        self.layoutSearchText.addWidget(self.btnSearch)
        self.layoutSearchText.addWidget(self.btnPrev)
        self.layoutSearchText.addWidget(self.btnNext)
        self.layoutSearchText.setContentsMargins(0, 0, 0, 0)

        self.searchLayout = QVBoxLayout()
        self.searchLayout.addLayout(closeLayout)
        self.searchLayout.addLayout(self.layoutSearchLabel)
        self.searchLayout.addLayout(self.layoutSearchText)

    def createReplaceBox(self):
        self.lblReplace = QLabel("Replace")

        layoutReplaceLabel = QHBoxLayout()
        layoutReplaceLabel.addWidget(self.lblReplace)
        layoutReplaceLabel.addSpacerItem(self.vSpacer)

        self.txtReplace = QLineEdit()
        # il placeholder text deve essere italic

        self.txtReplace.setPlaceholderText("Replace")
        self.txtReplace.setFixedHeight(30)
        self.btnReplace = QPushButton("Replace")
        self.btnReplace.setFixedWidth(80)
        self.btnReplace.setFixedHeight(30)
        self.replaceAllButton = QPushButton("Replace All")
        self.replaceAllButton.setFixedHeight(30)
        self.layoutReplaceText = QHBoxLayout()
        self.layoutReplaceText.addWidget(self.txtReplace)
        self.layoutReplaceText.addWidget(self.btnReplace)
        self.layoutReplaceText.addWidget(self.replaceAllButton)
        self.replaceLayout = QVBoxLayout()
        self.replaceLayout.addLayout(layoutReplaceLabel)
        self.replaceLayout.addLayout(self.layoutReplaceText)

    def SearchAndReplaceLayout(self):
        self.createSearchBox()
        self.createReplaceBox()
        self.layoutMain = QVBoxLayout()
        self.layoutMain.addLayout(self.searchLayout)
        self.layoutMain.addLayout(self.replaceLayout)
        self.layoutMain.setContentsMargins(10, 10, 10, 10)

    def initStyle(self):
        self.setFont(QFont("Consolas", 8))
        backGroundColor = self.editor.backgroundColor
        textColor = self.editor.textColor
        grpBoxStyle = f"""
                        QGroupBox {{
                            background-color: {backGroundColor.name()};
                            color: {textColor.name()};
                            border: 1px solid {textColor.name()};
                            border-radius: 5px;
                            margin-top: 0.5em;
                        }}"""
        lblStyle = f"""
                    QLabel {{   
                        color: {textColor.name()};
                        font-size: 11px;
                    }}"""
        txtLineEditStyle = f"""
                            QLineEdit {{
                                background-color: {backGroundColor.name()};
                                color: {textColor.name()};
                                border: 1px solid {textColor.name()};
                                border-radius: 5px;
                                padding: 0 8px;
                                font-size: 12px;
                            }}
                QLineEdit::placeholder {{
                    color: {textColor.name()};
                    font-size: 10px;
                    font-style: italic;
                }}
        """
        allStyle = grpBoxStyle + lblStyle + txtLineEditStyle
        self.setStyleSheet(allStyle)

    def initConnections(self):
        self.txtSearch.textChanged.connect(self.onTxtSearchClicked)
        self.txtSearch.returnPressed.connect(self.search)
        self.btnSearch.clicked.connect(self.search)
        self.btnPrev.clicked.connect(self.searchPrev)
        self.btnNext.clicked.connect(self.searchNext)
        self.btnReplace.clicked.connect(self.replace)
        self.replaceAllButton.clicked.connect(self.replaceAll)

    def onTxtSearchClicked(self, text):
        if text:
            self.txtSearch.setPlaceholderText("")
        else:
            self.txtSearch.setPlaceholderText("Search")

    def search(self):
        txt = self.txtSearch.text()
        machCase = self.chkCaseSensitive.isChecked()
        matchWholeWord = self.chkWholeWord.isChecked()
        self.editor.onSearchText(txt, machCase, matchWholeWord)

    def searchPrev(self):
        """
        search for the previous word of the list
        :return:
        """
        txt = self.txtSearch.text()
        self.editor.onSearchPrevious(txt)

    def searchNext(self):
        """
        search for the next word of the list
        :return:
        """
        txt = self.txtSearch.text()
        self.editor.onSearchNext(txt)

    def replace(self):
        """
        replace the selected text with the text in the replace box
        onReplaceText(self, _type, text, newText):
        :return:
        """
        _type = "single"
        text = self.txtSearch.text()
        newText = self.txtReplace.text()
        print(_type, text, newText)
        self.editor.onReplaceText(_type, text, newText)

    def replaceAll(self):
        """
        replace all the text in the editor with the text in the replace box
        :return:
        """
        _type = "all"
        text = self.txtSearch.text()
        newText = self.txtReplace.text()
        self.editor.onReplaceText(_type, text, newText)

    def showEvent(self, event):
        self.txtSearch.setFocus()
        self.txtSearch.selectAll()
        super().showEvent(event)


class pythonCodeEditor(QPlainTextEdit):
    # color variables for editor
    backgroundColor: QColor = QColor(30, 31, 34)
    textColor: QColor = QColor(167, 183, 198)
    lineNumberColor: QColor = QColor(200, 200, 240, 255)
    lineNumberBackgroundColor: QColor = backgroundColor.darker(110)
    indentationLineColor: QColor = QColor(255, 100, 100, 255)
    indentationLineWidth: int = 1
    indentationWidth: int = 4
    indentationLinesList = []
    # colori di sistema
    selectionColor: QColor = QColor(0, 122, 204)
    selectionBackgroundColor: QColor = backgroundColor.lighter(120)
    caretColor: QColor = QColor(255, 255, 255)
    caretBackgroundColor: QColor = QColor(255, 255, 255)
    marginColor: QColor = QColor(255, 255, 255)
    marginTextColor: QColor = QColor(255, 255, 255)
    marginBackgroundColor: QColor = QColor(255, 255, 255)

    # fonts variable for editor
    systemFont: QFont = QFont("Lohit Gujarati", 12)

    lineNumberFont: QFont = QFont("Consolas", 8)
    lineNumberArea: LineNumberArea
    completer: QCompleter
    caretHeight = 0
    searchResult = []
    searchIndex = 0

    def __init__(self, mainWidget: 'ArguePy_CodeEditor', parent=None):
        QPlainTextEdit.__init__(self, parent)
        self.mainWidget = mainWidget
        self.initUI()
        self.initFont()
        self.updateSystemColors()
        self.initLineNumberArea()
        self.pythonHighlighter = pythonHighLighter(self.document(), self)

        self.initCompleter()
        self.document().contentsChanged.connect(self.searchIndentation)
        self.zoomLevel = 1.0

    def initUI(self):
        self.setTabStopWidth(4)
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.setWordWrapMode(QTextOption.WrapMode.NoWrap)
        self.setTabChangesFocus(True)
        self.setCenterOnScroll(True)
        self.setUndoRedoEnabled(True)
        # setta l'altezza del testo doppia rispetto alla font size
        self.setCursorWidth(3)

    def initFont(self):
        self.systemFont = QFont("Curier New", 12)
        self.systemFont.setStyleHint(QFont.TypeWriter)
        self.systemFont.setPointSize(12)
        self.setFont(self.systemFont)

    def updateSystemColors(self):
        # dovrebbe cambiare solo lo sfondo non tutto il colore del widget
        style = f"QPlainTextEdit {{background-color: {self.backgroundColor.name()}; color: {self.textColor.name()};}}"
        self.setStyleSheet(style)

    def contextMenuEvent(self, event) -> None:
        menu = QMenu(self)
        _new = QAction("New", self)
        _new.triggered.connect(self.mainWidget.onNew)
        _open = QAction("Open", self)
        _open.triggered.connect(self.mainWidget.onOpen)
        _save = QAction("Save", self)
        _save.triggered.connect(self.mainWidget.onSave)
        _saveAs = QAction("Save As", self)
        _saveAs.triggered.connect(self.mainWidget.onSaveAs)
        _color = QAction("preferences", self)
        _color.triggered.connect(self.mainWidget.onPreferences)
        _run = QAction("Run", self)
        _run.triggered.connect(self.mainWidget.onRun)
        _search = QAction("Search", self)
        _search.triggered.connect(self.onSearch)
        menu.addAction(_new)
        menu.addAction(_open)
        menu.addAction(_save)
        menu.addAction(_saveAs)
        menu.addAction(_color)
        menu.addAction(_run)
        menu.addAction(_search)
        action = menu.exec_(self.mapToGlobal(event.pos()))

    def event(self, QEvent):
        if QEvent.type() == QEvent.Type.KeyPress:
            if QEvent.key() == Qt.Key.Key_Tab:
                if self.textCursor().hasSelection():  # se una parte del testo è selezionata
                    self.indentSelectedText()
                else:
                    self.insertPlainText("    ")
                return True
            # se viene premuto shift + tab fa l'indent alla rovescia
            elif QEvent.key() == Qt.Key.Key_Backtab:
                self.unIndentSelectedText()
                return True
        return super().event(QEvent)

    def keyPressEvent(self, event):
        # Auto completamento delle parentesi
        if event.key() in [Qt.Key.Key_BraceLeft, Qt.Key.Key_BracketLeft, Qt.Key.Key_ParenLeft, Qt.Key.Key_QuoteDbl,
                           Qt.Key.Key_Apostrophe]:
            self.parenthesesAutoComplete(event)
        elif event.key() == Qt.Key.Key_Return:
            self.insertNewLine()
        # se viene premuto il tasto #
        elif event.key() == Qt.Key.Key_NumberSign:
            if self.textCursor().hasSelection():
                self.commentBlock()
            else:
                super().keyPressEvent(event)
        else:
            super(pythonCodeEditor, self).keyPressEvent(event)

    def parenthesesAutoComplete(self, event):
        """
        Questa funzione si occupa di inserire le parentesi corrispondenti
        Se proviamo a scrive una parentesi e non è segnato nessun testo crea la parentsesi corrispondente e sponsta
        il cursore al centro. Se invece sotto sottolieiamo una porzione di testo, e clicchiamo su una parentesi di
        apertura inserisce automaticamente la parentesi di chiusura e sposta il cursore alla fine del testo selezionato
        :param event:
        :return:
        """
        matching = {Qt.Key.Key_BraceLeft: "}", Qt.Key.Key_BracketLeft: "]",
                    Qt.Key.Key_ParenLeft: ")", Qt.Key.Key_QuoteDbl: "\"", Qt.Key.Key_Apostrophe: "'"}
        if selectedText := self.textCursor().selectedText():
            self.insertPlainText(f"{event.text()}{selectedText}{matching[event.key()]}")
            # sposta il cursore alla fine del testo selezionato
            self.moveCursor(QTextCursor.MoveOperation.EndOfBlock)
            # se non è segnato nessun testo crea la parentesi corrispondente
            # e sposta il cursore al centro
        elif not selectedText:
            self.insertPlainText(f"{event.text()}{matching[event.key()]}")
            self.moveCursor(QTextCursor.MoveOperation.Left)

    def indentSelectedText(self):
        """
        Indenta il testo selezionato
        :return:
        """
        text = self.textCursor().selectedText()
        lines = text.splitlines()
        for i in range(len(lines)):
            lines[i] = f"    {lines[i]}\n"
        self.insertPlainText("".join(lines))

    def searchIndentationInFirstLineOfSelection(self, text):
        """
        Quando viene premuto shift + tab se l'utente ha selezionato la prima linea
        solo parzialmente, l'indentazione non risulterebbe corretta. Questa funzione
        cerca l'indentazione della prima linea ritorna il testo completo indentato.
        :param text:
        :return:
        """
        endPosition = self.textCursor().selectionEnd()
        cursor = self.textCursor()
        newStartPosition = cursor.movePosition(QTextCursor.MoveOperation.StartOfLine)
        startPosition = cursor.selectionStart()
        # crea una nuova selezione che va dall'inizio della prima riga
        # alla fine della selezione corrente
        cursor.setPosition(startPosition)
        cursor.setPosition(endPosition, QTextCursor.MoveMode.KeepAnchor)
        self.setTextCursor(cursor)
        text = self.textCursor().selectedText()
        return text

    def unIndentSelectedText(self):
        """
        Sposta a sinistra il testo selezionato di quattro spazi
        """
        text = self.searchIndentationInFirstLineOfSelection(self.textCursor().selectedText())
        # rimuove i primi quattro caratteri di ogni riga
        lines = text.splitlines()
        for i in range(len(lines)):
            if lines[i][:4] == "    ":
                lines[i] = f"{lines[i][4:]}\n"
        self.insertPlainText("".join(lines))

    def insertNewLine(self):
        """
        Se viene premuto invio e la riga precedente aveva
        una o più indentazioni la mette anche alla linea successiva
        """
        indentation = ""
        # calcola il numero di spazi all'inizio della righa
        indentationNumber = len(self.textCursor().block().text()) - len(self.textCursor().block().text().lstrip())
        indentation = " " * indentationNumber
        # se l'ultimo carattere della riga è : allora aggiunge un'altra indentazione
        # se la riga non è vuota
        if len(self.textCursor().block().text()) > 0:
            if self.textCursor().block().text()[-1] == ":":
                indentation += "    "
            self.insertPlainText(f"\n{indentation}")
        else:
            self.insertPlainText("\n")

    def commentBlock(self):
        """
        Commenta il testo selezionato
        """

        text = self.searchIndentationInFirstLineOfSelection(self.textCursor().selectedText())
        lines = text.splitlines()
        for i in range(len(lines)):
            if lines[i].startswith("    "):
                lines[i] = f"    # {lines[i][4:]}\n"
            else:
                lines[i] = f"# {lines[i]}\n"
        self.insertPlainText("".join(lines))

    def onSearch(self):
        """
        Quando viene premuto il tasto cerca
        :return:
        """
        self.mainWidget.searchWidget.show()

    def onSearchText(self, text, caseSensitive=False, wholeWords=False):
        """
        Quando viene premuto il tasto cerca, cerca il testo. Nel caso in cui
        sia selezionato caseSensitive o wholeWords, cerca il testo in base a
        questi parametri.
        :param text:
        :param caseSensitive:
        :param wholeWords:
        :return:
        """
        # posiziona il cursore all'inizio del testo
        self.moveCursor(QTextCursor.MoveOperation.Start)
        # Il Flag di ricerca è un intero che può essere combinato con l'operatore |

        flags = QTextDocument.FindFlag(0)
        if caseSensitive:
            print("caseSensitive")
            flags |= QTextDocument.FindFlag.FindCaseSensitively
        if wholeWords:
            print("wholeWords")
            flags |= QTextDocument.FindFlag.FindWholeWords

        # Cerca tutte le occorrenze della parola
        self.searchResult = []
        cursor = self.textCursor()
        while not cursor.isNull():
            cursor = self.document().find(text, cursor, flags)
            if not cursor.isNull():
                self.searchResult.append(cursor.selectionStart())
        # Se sono state trovate occorrenze, evidenzia la prima
        if self.searchResult:
            self.searchIndex = 0
            self.highlightCurrentSearchResult(text)

    def highlightCurrentSearchResult(self, text):
        # Rimuovi l'evidenziazione dalle precedenti occorrenze
        cursor = self.textCursor()
        cursor.clearSelection()
        self.setTextCursor(cursor)

        # Evidenzia la nuova occorrenza
        if len(self.searchResult) > 0:
            cursor.setPosition(self.searchResult[self.searchIndex])
            cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor, len(text))
            self.setTextCursor(cursor)

    def onSearchNext(self, text):
        """
        Quando viene premuto il tasto cerca successivo
        :return:
        """
        if self.searchResult:
            self.searchIndex += 1
            cursor = self.textCursor()
            cursor.clearSelection()
            self.setTextCursor(cursor)
            cursor.setPosition(self.searchResult[self.searchIndex])
            cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor, len(text))
            self.setTextCursor(cursor)

    def onSearchPrevious(self, text):
        """
        Quando viene premuto il tasto cerca precedente
        :return:
        """
        if self.searchResult:
            self.searchIndex -= 1
            cursor = self.textCursor()
            cursor.clearSelection()
            self.setTextCursor(cursor)
            cursor.setPosition(self.searchResult[self.searchIndex])
            cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor, len(text))
            self.setTextCursor(cursor)

    def onReplaceText(self, _type, text, newText):
        """
        Sostituisce il testo selezionato con il nuovo testo
        :param text:
        :param newText:
        :return:
        """
        if _type == "single":
            if not self.textCursor().hasSelection():
                self.find(text)
            self.textCursor().insertText(newText)
        elif _type == "all":
            if not self.searchResult:
                self.onSearchText(text)
            if self.searchResult:
                self.replaceAll(text, newText)

    def replaceAll(self, text, newText):
        """
        Sostituisce tutte le occorrenze del testo con il nuovo testo
        :param text:
        :param newText:
        :return:
        """
        while self.find(text):
            self.textCursor().insertText(newText)

    def paintEvent(self, e: QPaintEvent) -> None:
        super().paintEvent(e)
        painter = QPainter(self.viewport())
        # disegna una linea orizzontale per ogni riga di testo
        height = self.fontMetrics().height()
        for i in range(self.document().blockCount()):
            top = self.blockBoundingGeometry(self.document().findBlockByNumber(i)).translated(
                self.contentOffset()).top()
            color = QColor(20, 20, 40, 90)
            pen = QPen(color, 1)
            # long dash line
            pen.setStyle(Qt.PenStyle.DotLine)
            painter.setPen(pen)
            line = QLine(0, int(top + height), int(self.width()), int(top + height))
            painter.drawLine(line)

    def searchIndentation(self):
        """
        Restituisce una lista linee QLine() che verrano poi disegnate per rappresentare l'indentazione.
        L'indentazione viene mostrata solo se la riga inizia con "def".
        Se le righe successive fanno parte della stessa funzione allora non viene mostrata la linea di indentazione,
        altrimenti no.
        """
        indentation = 0
        returnPressed = 0
        isFoundADef = False
        linesOfCode = self.toPlainText().splitlines()
        for row, line in enumerate(linesOfCode):
            # se la riga inizia con "def" allora aggiungiamo l'indentazione e la coordinata x
            if "def " in line and not isFoundADef:
                indentation = len(line) - len(line.lstrip())
                self.appendToLineIndentationList(indentation, row)
                isFoundADef = True
            # se la riga non inizia con "def" ma abbiamo già registrato l'indentazione
            elif line.startswith(" ") and isFoundADef:
                self.appendToLineIndentationList(indentation, row)

            # se la riga è vuota ma c'è già un'indentazione registrata
            elif line == "" and isFoundADef:
                if returnPressed == 0:
                    self.appendToLineIndentationList(indentation, row)
                    returnPressed += 1
                else:
                    self.indentationLinesList.pop()
                    returnPressed = 0
            if "def " in line and isFoundADef:
                # E' una nuova definizione
                self.indentationLinesList.pop()
                if self.indentationLinesList:
                    self.indentationLinesList.pop()
                self.appendToLineIndentationList(indentation, row)

    def appendToLineIndentationList(self, indentation, row):

        fontMetrics = QFontMetrics(self.systemFont)
        x = indentation * fontMetrics.averageCharWidth()
        self.indentationLinesList.append((row, indentation, x))

    def drawLine(self):
        """
        Disegna le linee di indentazione per le righe contenenti la keyword "def".
        """
        painter = QPainter(self.viewport())
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen = QPen(self.indentationLineColor, self.indentationLineWidth)
        pen.setStyle(Qt.PenStyle.DotLine)
        painter.setPen(pen)

        for row, indentation, x in self.indentationLinesList:
            top = self.blockBoundingGeometry(self.document().findBlockByNumber(row)).translated(
                self.contentOffset()).top()
            bottom = top + self.blockBoundingRect(self.document().findBlockByNumber(row)).height()
            h = self.fontMetrics().height() * self.zoomLevel
            line = QLineF(int(x), int(bottom), int(x), int(bottom + h))
            painter.drawLine(line)
        painter.end()

    def wheelEvent(self, event):
        """
        Questo metodo è stato ridefinito per permettere di usare la rotellina del mouse per lo zoom
        :param event:
        :return:
        """
        if event.modifiers() == Qt.ControlModifier:
            if event.angleDelta().y() > 0:
                self.zoomIn()
                self.lineNumberFont.setPointSize(self.lineNumberFont.pointSize() + 1)
                self.zoomLevel += 0.1
            else:
                self.zoomOut()
                self.lineNumberFont.setPointSize(self.lineNumberFont.pointSize() - 1)
                self.zoomLevel -= 0.1
        else:
            super().wheelEvent(event)

    def initCompleter(self):
        """
        Inizializza il completer
        :return:
        """
        self.completer = QCompleter(self)
        self.completer.setWidget(self)
        # PopupCompletion mostra la lista dei completamenti
        self.completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.activated.connect(self.insertCompletion)

    def insertCompletion(self, completion):
        """
        Inserisce il completamento. In pratica prende il testo selezionato
        e lo sostituisce con il completamento
        :param completion:
        :return:
        """
        if self.completer.widget() != self:
            return
        extra = len(completion) - len(self.completer.completionPrefix())
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Left)
        cursor.movePosition(QTextCursor.MoveOperation.EndOfWord)
        cursor.insertText(completion[-extra:])
        self.setTextCursor(cursor)

    def textUnderCursor(self):
        """
        Ritorna il testo sotto il cursore, ovvero il testo che si sta scrivendo
        :return:
        """
        cursor = self.textCursor()
        cursor.select(QTextCursor.SelectionType.WordUnderCursor)
        return cursor.selectedText()

    def initLineNumberArea(self):
        self.lineNumberArea = LineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.updateLineNumberAreaWidth(0)
        self.highlightCurrentLine()

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.setFont(self.lineNumberFont)
        painter.setPen(self.lineNumberColor)
        painter.fillRect(event.rect(), self.lineNumberBackgroundColor)

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                rect = QRectF(0, top, self.lineNumberArea.width(), self.fontMetrics().height())
                painter.drawText(rect, Qt.AlignmentFlag.AlignHCenter, number)
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

    def lineNumberAreaWidth(self):
        digits = len(str(self.blockCount()))
        return 4 + self.fontMetrics().width('9') * digits

    def resizeEvent(self, event):
        QPlainTextEdit.resizeEvent(self, event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    @pyqtSlot(int)
    def updateLineNumberAreaWidth(self, newBlockCount):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    @pyqtSlot()
    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = self.selectionBackgroundColor
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

    @pyqtSlot(QRect, int)
    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def doCompletion(self):
        """
        Esegue il completamento. In pratica prende il testo sotto il cursore e
        lo confronta con la lista dei completamenti, se c'è un match allora
        mostra la lista dei completamenti nella finestra di completamento
        :return:
        """
        completionPrefix = self.textUnderCursor()
        if completionPrefix != self.completer.completionPrefix():
            self.completer.setCompletionPrefix(completionPrefix)
            popup = self.completer.popup()
            popup.setCurrentIndex(self.completer.completionModel().index(0, 0))

            cr = self.cursorRect()
            cr.setWidth(self.completer.popup().sizeHintForColumn(0)
                        + self.completer.popup().verticalScrollBar().sizeHint().width())
            self.completer.complete(cr)
