from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

cssKeywords = [
    'color', 'background-color', 'border', 'border-color', 'border-style', 'border-width', 'border-top',
    'border-top-color', 'border-top-style', 'border-top-width', 'border-right', 'border-right-color',
    'border-right-style', 'border-right-width', 'border-bottom', 'border-bottom-color', 'border-bottom-style',
    'border-bottom-width', 'border-left', 'border-left-color', 'border-left-style', 'border-left-width',
    'outline',
    'outline-color', 'outline-style', 'outline-width', 'margin', 'margin-top', 'margin-right', 'margin-bottom',
    'margin-left', 'padding', 'padding-top', 'padding-right', 'padding-bottom', 'padding-left', 'font',
    'font-family',
    'font-size', 'font-weight', 'font-style', 'text-align', 'text-decoration', 'text-transform', 'line-height',
    'vertical-align', 'white-space', 'display', 'width', 'height', 'max-width', 'max-height', 'min-width',
    'min-height',
    'position', 'top', 'right', 'bottom', 'left', 'float', 'clear', 'overflow', 'z-index', 'visibility',
    'opacity'
]

pythonKeywords = [
    'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else',
    'except', 'False', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'None',
    'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'self', 'True', 'try', 'while', 'with', 'yield']

predefinedFunctionNames = ['abs', 'all', 'any', 'ascii', 'bin', 'bool', 'bytearray', 'bytes', 'callable',
                           'chr', 'classmethod', 'compile', 'complex', 'delattr', 'dict', 'dir', 'divmod', 'enumerate',
                           'eval', 'exec', 'filter', 'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr',
                           'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass', 'iter', 'len',
                           'list', 'locals', 'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord',
                           'pow', 'print', 'property', 'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice',
                           'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip']

operators = [
    '=',
    # Comparison
    '==', '!=', '<', '<=', '>', '>=',
    # Arithmetic
    '\+', '-', '\*', '/', '//', '\%', '\*\*',
    # In-place
    '\+=', '-=', '\*=', '/=', '\%=',
    # Bitwise
    '\^', '\|', '\&', '\~', '>>', '<<',
]

braces = [
    '\{', '\}', '\(', '\)', '\[', '\]',
]


def _format(color, style=''):
    """Return a QTextCharFormat with the given attributes.
    """
    characterFormat = QTextCharFormat()
    if color is not None:
        _color = QColor()
        _color.setRgb(color[0], color[1], color[2])
        characterFormat.setForeground(_color)
    if 'bold' in style:
        characterFormat.setFontWeight(QFont.Weight.Bold)
    if 'italic' in style:
        characterFormat.setFontItalic(True)
    if 'error' in style:
        characterFormat.setUnderlineColor(Qt.GlobalColor.red)
        characterFormat.setUnderlineStyle(QTextCharFormat.UnderlineStyle.SpellCheckUnderline)
    return characterFormat


styles = {
    'keyword': _format((255, 153, 0)),
    'operator': _format((255, 169, 102)),
    'brace': _format((128, 128, 128)),
    'defclass': _format((255, 255, 102), 'bold'),
    'string': _format((201, 160, 220)),
    'string2': _format((244, 0, 161)),
    'functionKeyword': _format((255, 255, 102), 'bold'),
    'CssKeyword': _format((255, 255, 102), 'bold'),
    'triple-single': _format((201, 160, 220)),
    'triple-double': _format((244, 0, 161)),
    'comment': _format((153, 51, 102), 'italic'),
    'self': _format((204, 204, 255), 'italic'),
    'numbers': _format((173, 223, 173)),
    'wrongWord': _format(None, 'error'),
}


class lineNumberArea(QWidget):
    """
    questa classe crea un widgetEditor che contiene il numero di riga
    che sarà poi utilizzato nel code editor
    """

    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor

    def sizeHint(self):
        return QSize(self.codeEditor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)


class superSyntaxHighLighter(QSyntaxHighlighter):
    tripleQuotesWithinStrings = []
    tri_single = (QRegExp("'''"), 1, styles['string2'])
    tri_double = (QRegExp('"""'), 2, styles['string2'])
    rules = []

    def __init__(self, parent=None):
        super().__init__(parent)
        self.keywords = cssKeywords + pythonKeywords + braces + operators + predefinedFunctionNames
        self.pythonPatternRules()

    def pythonPatternRules(self):
        # Regole per la sintassi
        self.rules = []
        # Keyword, operator, braces
        self.rules += [(r'\b%s\b' % w, 0, styles['keyword'])
                       for w in pythonKeywords]
        self.rules += [(f'{o}', 0, styles['operator']) for o in operators]
        self.rules += [(f'{b}', 0, styles['brace']) for b in braces]
        # Predefined functions
        self.rules += [(r'\b%s\b' % f, 0, styles['functionKeyword']) for f in predefinedFunctionNames]

        # All other rules
        self.rules += [
            # 'self'
            (r'\bself\b', 0, styles['self']),

            # 'def' followed by an identifier
            (r'\bdef\b\s*(\w+)', 1, styles['defclass']),
            # 'class' followed by an identifier
            (r'\bclass\b\s*(\w+)', 1, styles['defclass']),

            # Numeric literals
            (r'\b[+-]?[0-9]+[lL]?\b', 0, styles['numbers']),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, styles['numbers']),
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][0-9]+)?\b', 0, styles['numbers']),

            # Double-quoted string, possibly containing escape sequences
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, styles['string']),
            # Single-quoted string, possibly containing escape sequences
            (r"'[^'\\]*(\\.[^'\\]*)*'", 0, styles['string']),

            # Predefined function calls
            (r'\b(%s)\s*\(' % '|'.join(predefinedFunctionNames), 1, styles['functionKeyword']),

            # From '#' until a newline
            (r'#[^\n]*$', 0, styles['comment'])

        ]
        # Build a QRegExp for each pattern
        self.rules = [(QRegExp(pat), index, fmt)
                      for (pat, index, fmt) in self.rules]

    def highlightBlock(self, text):
        self.checkPythonCode(text)

    def checkPythonCode(self, text):
        self.tripleQuotesWithinStrings = []
        # Do other syntax formatting
        for expression, nth, format in self.rules:
            index = expression.indexIn(text, 0)

            if index >= 0:
                # if there is a string we check
                # if there are some triple quotes within the string
                # they will be ignored if they are matched again
                if expression.pattern() in [r'"[^"\\]*(\\.[^"\\]*)*"', r"'[^'\\]*(\\.[^'\\]*)*'"]:
                    innerIndex = self.tri_single[0].indexIn(text, index + 1)
                    if innerIndex == -1:
                        innerIndex = self.tri_double[0].indexIn(text, index + 1)

                    if innerIndex != -1:
                        tripleQuoteIndexes = range(innerIndex, innerIndex + 3)
                        self.tripleQuotesWithinStrings.extend(tripleQuoteIndexes)

            while index >= 0:
                # skipping triple quotes within strings
                if index in self.tripleQuotesWithinStrings:
                    index += 1
                    expression.indexIn(text, index)
                    continue
                # We actually want the index of the nth match
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)
        self.setCurrentBlockState(0)
        # Do multi-line strings
        in_multiline = self.matchMultiline(text, *self.tri_single)
        if not in_multiline:
            in_multiline = self.matchMultiline(text, *self.tri_double)

    def matchMultiline(self, text, delimiter, in_state, style):
        # If inside triple-single quotes, start at 0
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        # Otherwise, look for the delimiter on this line
        else:
            start = delimiter.indexIn(text)
            # Move past this match
            add = delimiter.matchedLength()
        # As long as there's a delimiter match on this line...
        while start >= 0:
            # Look for the ending delimiter
            end = delimiter.indexIn(text, start + add)
            # Ending delimiter on this line?
            if end >= add:
                length = end - start + add + delimiter.matchedLength()
                self.setCurrentBlockState(0)
            # No; multi-line string
            else:
                self.setCurrentBlockState(in_state)
                length = len(text) - start + add
            # Apply formatting
            self.setFormat(start, length, style)
            # Look for the next match
            start = delimiter.indexIn(text, start + length)
        # Return True if still inside a multi-line string, False otherwise
        if self.currentBlockState() == in_state:
            return True
        else:
            return False


class textEditorWithLineNumber(QPlainTextEdit):
    fontLineNumber: QFont
    fontCodeEditor: QFont
    isFontLineNumberBold = False
    fontLineColorDefault = QColor(50, 50, 90)
    LineBorderColor = QColor(50, 50, 50)
    lineWidth = 20

    def __init__(self, parent=None):
        super().__init__(parent)
        """
        Questa classe è un override della classe QPlainTextEdit
        che aggiunge la funzionalità di avere il numero di riga

        """
        self.initLookAndFeel()
        self.lineNumberArea = lineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.updateLineNumberAreaWidth(0)
        self.highlighter = superSyntaxHighLighter(self.document())

    def initLookAndFeel(self):
        self.fontLineNumber = QFont("Ubuntu Mono", 11)
        self.isFontLineNumberBold = True
        self.fontLineNumber.setBold(self.isFontLineNumberBold)
        self.fontCodeEditor = QFont("Consolas", 12)

    def lineNumberAreaWidth(self):
        digits = 2
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1
        return 3 + self.fontMetrics().width('9') * digits

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaPaintEvent(self, event):
        """
        Questo metodo viene chiamato ogni volta che viene aggiornato il numero di riga

        :param event:
        :return:
        """
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), self.LineBorderColor)
        painter.setFont(self.fontLineNumber)
        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()
        height = self.fontMetrics().height()
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(f"{blockNumber + 1} ")
                painter.setPen(self.LineBorderColor.lighter(150))
                rect = QRectF(0, int(top), int(self.lineNumberArea.width()), int(self.fontMetrics().height()))
                painter.drawText(rect, height, number)
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

    def wheelEvent(self, event):
        """
        Questo metodo è stato ridefinito per permettere di usare la rotellina del mouse per lo zoom
        :param event:
        :return:
        """
        if event.modifiers() == Qt.ControlModifier:
            if event.angleDelta().y() > 0:
                self.zoomIn()
                self.fontLineNumber.setPointSize(self.fontLineNumber.pointSize() + 1)
            else:
                self.zoomOut()
                self.fontLineNumber.setPointSize(self.fontLineNumber.pointSize() - 1)
        else:
            super().wheelEvent(event)


class CodeEditor(QWidget):
    codeEditor: textEditorWithLineNumber
    fileName = "untitled"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.codeEditor = textEditorWithLineNumber()
        self.codeEditor.textChangedSignal.connect(self.node.updateNodeFromText)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.addWidget(self.codeEditor)
        self.setLayout(layout)

    def contextMenuEvent(self, QContextMenuEvent):
        menu = QMenu(self)
        _loadCode = menu.addAction("loadCode")
        _saveCode = menu.addAction("saveCode")
        _saveAsCode = menu.addAction("saveAsCode")

        menu.exec_(QContextMenuEvent.globalPos())

    def onNew(self):
        """
        Questo metodo viene chiamato quando si clicca su new
        :return:
        """
        self.fileName = "untitled"
        self.codeEditor.clear()

    def loadCode(self):
        """
        Questo metodo carica il codice dal file con una qDialog
        :return:
        """
        self.onNew()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Python Files (*.py)")
        if fileName:
            with open(fileName, "r") as file:
                self.codeEditor.setPlainText(file.read())
                self.fileName = fileName

    def saveCode(self):
        """
        Questo metodo salva il codice nel file con una qDialog
        :return:
        """
        if self.fileName == "untitled":
            self.saveAsCode()
        else:
            with open(self.fileName, "w") as file:
                file.write(self.codeEditor.toPlainText())

    def saveAsCode(self):
        """
        Questo metodo salva il codice nel file con una qDialog
        :return:
        """
        fileName, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Python Files (*.py)")
        if fileName:
            with open(fileName, "w") as file:
                file.write(self.codeEditor.toPlainText())

