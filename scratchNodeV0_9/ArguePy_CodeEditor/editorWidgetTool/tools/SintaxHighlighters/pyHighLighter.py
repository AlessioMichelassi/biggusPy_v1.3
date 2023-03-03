import io
import os
import re
import tempfile

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


pythonKeywords = [
    'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else',
    'except', 'False', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'None',
    'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'True', 'try', 'while', 'with', 'yield', ',']

predefinedFunctionNames = ['abs', 'all', 'any', 'ascii', 'bin', 'bool', 'bytearray', 'bytes', 'callable',
                           'chr', 'classmethod', 'compile', 'complex', 'delattr', 'dict', 'dir', 'divmod', 'enumerate',
                           'eval', 'exec', 'filter', 'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr',
                           'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass', 'iter', 'len',
                           'list', 'locals', 'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord',
                           'pow', 'print', 'property', 'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice',
                           'sorted', 'staticmethod', 'str', 'sum', 'tuple', 'type', 'vars', 'zip']

classFunction = ['__init__', '__del__', '__repr__', '__str__', '__cmp__', '__call__', '__len__', '__getitem__',
                 '__setitem__', '__delitem__',
                 '__iter__', '__contains__', '__getslice__', '__setslice__', '__delslice__', '__add__', '__sub__',
                 '__mul__', '__div__', '__mod__',
                 '__pow__', '__lshift__', '__rshift__', '__and__', '__xor__', '__or__', '__iadd__', '__isub__',
                 '__imul__', '__idiv__', '__imod__',
                 '__ipow__', '__ilshift__', '__irshift__', '__iand__', '__ixor__', '__ior__', '__neg__', '__pos__',
                 '__abs__', '__invert__',
                 '__complex__', '__int__', '__long__', '__float__', '__oct__', '__hex__', '__index__', '__coerce__',
                 '__enter__', '__exit__']

decorators = ['@staticmethod', '@classmethod', '@property']

mathFunction = ['acos', 'acosh', 'asin', 'asinh', 'atan', 'atan2', 'atanh', 'ceil', 'copysign', 'cos', 'cosh',
                'degrees', 'e', 'erf', 'erfc',
                'exp', 'expm1', 'fabs', 'factorial', 'floor', 'fmod', 'frexp', 'fsum', 'gamma', 'hypot', 'inf',
                'isclose', 'isfinite', 'isinf',
                'isnan', 'ldexp', 'lgamma', 'log', 'log10', 'log1p', 'log2', 'modf', 'nan', 'pi', 'pow', 'radians',
                'sin', 'sinh', 'sqrt', 'tan',
                'tanh', 'tau', 'trunc']

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

braces = ['\{', '\}', '\(', '\)', '\[', '\]']


def find_triple_quotes(text):
    """
    Trova le posizioni di inizio e fine dei commenti multilinea
    :param text:
    :return: una lista di tuple contenenti l'inizio e la fine dei commenti multilinea
    """
    positions = []
    start = None
    inside_triple_quoted = False
    for i in range(len(text)):
        if text[i:i + 3] in ('"""', "'''"):
            if inside_triple_quoted:
                positions.append((start, i + 3))
                inside_triple_quoted = False
            else:
                start = i
                inside_triple_quoted = True
    if inside_triple_quoted:
        positions.append((start, len(text)))
    return positions


class pythonHighLighter(QSyntaxHighlighter):
    keywordColor: QColor = QColor(255, 91, 0, 255)
    functionColor: QColor = QColor(178, 101, 100, 255)
    builtInColor: QColor = QColor(233, 118, 51, 255)
    # color melanzana
    selfColor: QColor = QColor(191, 0, 127, 255)
    classFunctionColor: QColor = QColor(239, 0, 159, 255)
    methodColor: QColor = QColor(220, 158, 0, 255)
    braceColor: QColor = QColor(200, 200, 200, 255)
    numberColor: QColor = QColor(103, 151, 187, 255)
    stringColor: QColor = QColor(99, 99, 181, 255)
    commentColor: QColor = QColor(113, 128, 147, 255)  # grigio bluastro
    comment2Color: QColor = QColor(113, 128, 147)  # grigio bluastro
    operatorColor: QColor = QColor(255, 255, 255)  # bianco
    identifierColor: QColor = QColor(255, 255, 255)  # bianco
    commentLineColor: QColor = QColor(113, 128, 147)  # grigio bluastro
    commentDocColor: QColor = QColor(113, 128, 147)  # grigio bluastro
    commentDocKeywordColor: QColor = QColor(255, 195, 0)  # giallo dorato
    errorColor: QColor = QColor(255, 0, 0)  # rosso
    pepColor: QColor = QColor(40, 100, 40)  # verde

    def __init__(self, document, editor):
        super().__init__(document)
        self.document = document
        self.editor = editor
        self.rules = []
        self.comment_state = 0
        # crea error underline le setta come colore a rosso
        self.errorUnderline = QTextCharFormat()
        self.errorUnderline.setUnderlineStyle(QTextCharFormat.UnderlineStyle.SpellCheckUnderline)
        self.errorUnderline.setUnderlineColor(self.errorColor)
        self.knownWords = pythonKeywords + predefinedFunctionNames + classFunction + decorators + \
                          mathFunction + operators + braces + ['self']
        self.errorList = []
        self.pythonPatternRules()

    def pythonPatternRules(self):
        self.rules = []
        self.rules += [(r'\b%s\b' % w, 0, self.keywordColor) for w in pythonKeywords]
        # se la parola è "self" è di un colore diverso
        self.rules += [(r'\b%s\b' % w, 0, self.selfColor) for w in ['self']]

        self.rules += [(r'\b%s\b' % w, 0, self.functionColor) for w in predefinedFunctionNames]
        # se una parola è preceduta da def o class e non è in classFunction allora è un metodo
        self.rules += [(r'\bdef\b\s*(\w+)', 1, self.methodColor)]
        self.rules += [(r'\b%s\b' % w, 0, self.classFunctionColor) for w in classFunction]
        self.rules += [(f'{b}', 0, self.braceColor) for b in braces]
        self.rules += [(f'{o}', 0, self.operatorColor) for o in operators]

        self.rules += [(r'\b[+-]?[0-9]+[lL]?\b', 0, self.numberColor),
                       (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, self.numberColor),
                       (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, self.numberColor)]

        self.rules += [(r'"(?:\\.|[^"])*"', 0, self.stringColor)]
        self.rules += [(r"'(?:\\.|[^'])*'", 0, self.stringColor)]

        self.commentRules = [(r'#.*$', 0, self.commentColor), (r'#.*$', 0, self.comment2Color),
                             (r'#.*$', 0, self.commentLineColor), (r'#.*$', 0, self.commentDocColor),
                             (r'#.*$', 0, self.commentDocKeywordColor), (r'#.*$', 0, self.commentColor)]

    def highlightBlock(self, text):
        """
        Fa gli highlight del testo in base alle regole definite in self.rules
        :param text:
        :return:
        """
        rulez = [(QRegExp(pat), index, fmt)
                 for (pat, index, fmt) in self.rules]
        for expression, nth, color in rulez:
            index = expression.indexIn(text, 0)
            while index >= 0:
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, color)
                index = expression.indexIn(text, index + length)

        self.searchForMultilineComment(text)
        # Evidenzia le parole non riconosciute in rosso

    def searchForMultilineComment(self, text):
        self.setCurrentBlockState(0)
        # Gestione dei commenti multilinea
        start_index = 0
        while start_index >= 0:
            if self.comment_state == 0:
                # Stato fuori dai commenti multilinea
                start_index = text.find('"""', start_index)
                if start_index >= 0:
                    self.comment_state = 1
                    end_index = text.find('"""', start_index + 3)
                    if end_index < 0:
                        end_index = len(text)
                    else:
                        end_index += 3
                    self.setFormat(start_index, end_index - start_index, self.commentDocColor)
                    start_index = end_index
            elif self.comment_state == 1:
                # Stato dentro a un commento multilinea con tre virgolette
                end_index = text.find('"""', start_index)
                if end_index >= 0:
                    end_index += 3
                    self.setFormat(start_index, end_index - start_index, self.commentDocColor)
                    self.comment_state = 0
                    start_index = end_index
                else:
                    self.setFormat(start_index, len(text) - start_index, self.commentDocColor)
                    start_index = -1
        self.setCurrentBlockState(0)

    def searchError2(self, text: str):
        """
        Cerca errori nella riga
        :param errorList:
        :return:
        """
        words = re.findall(r'\b\w+\b', text)
        error_list = []  # Inizializza una lista vuota di errori
        for word in words:
            if word not in self.knownWords and not word.startswith('__'):
                error_list.append((text.index(word), len(word)))  # Aggiungi l'errore alla lista
        # Rimuovi i commenti e le stringhe dalla lista degli errori
        rulez = [(QRegExp(pat), index, fmt)
                 for (pat, index, fmt) in self.rules]

        commentz = [(QRegExp(pat), index, fmt) for (pat, index, fmt) in self.commentRules]
        for expression, _, _ in rulez + commentz:
            index = expression.indexIn(text)
            while index >= 0:
                length = len(expression.cap(0))
                error_list = [(start, end) for start, end in error_list if end <= index or start >= index + length]
                index = expression.indexIn(text, index + length)
        # Applica la formattazione agli errori rimanenti
        for start, end in error_list:
            self.setFormat(start, end, self.errorUnderline)

    def highlightError(self, errorList: list):
        """
        Evidenzia le parole non riconosciute in rosso
        :param errorList:
        :return:
        """
        for error in errorList:
            if error[0] == self.document:
                self.setFormat(error[1], error[2], self.errorUnderline)

    def setColor(self, color: QColor, colorName: str):
        print(f"change in color {colorName} to {color.name()}")
        if colorName == "keywordColor":
            self.keywordColor = color
        elif colorName == "functionColor":
            self.functionColor = color
        elif colorName == "builtInColor":
            self.builtInColor = color
        elif colorName == "selfColor":
            self.selfColor = color

        self.pythonPatternRules()

    def setKeywordColor(self, color: QColor):
        self.keywordColor = color
        self.pythonPatternRules()

    def setFunctionColor(self, color: QColor):
        self.functionColor = color
        self.pythonPatternRules()

    def setBuiltInColor(self, color: QColor):
        self.builtInColor = color
        self.pythonPatternRules()
