# -*- coding: utf-8 -*-
import math
import random

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMenu

from elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface

"""
ToDO:

ITA:
In alcune funzioni come returnToSnakeCaseCode e returnToCamelCaseCode hai scritto solo una stampa a video invece 
di ritornare il codice vero e proprio. Probabilmente si tratta di un errore e dovresti implementare il codice 
mancante. Alcune delle funzioni che modificano la stringa, come capitalize, casefold, title, upper e lower, 
usano sempre il primo valore in input, ignorando eventuali altri input. Potresti controllare se ci sono altri input 
e, se presenti, usarli per modificare la stringa corretta. La funzione calculateOutput è piuttosto lunga e complessa. 
Potresti renderla più leggibile separando le varie casistiche in funzioni diverse e/o aggiungendo commenti che 
spiegano cosa fa il codice in ogni parte. La funzione showContextMenu è abbastanza lunga e ripetitiva. Potresti 
creare una funzione separata per ogni tipo di azione del menu a tendina (come replace, split, capitalize, 
ecc.) e chiamarle in base all'azione selezionata. La funzione camelCaseToSnakeCase è attualmente implementata in modo 
tale da accettare solo due formati di input (camelCase e snake_case). Potresti rendere la funzione più generale in 
modo da accettare un argomento in più che indica il formato di output desiderato. In generale, il codice potrebbe 
beneficiare di più commenti che spiegano cosa fa ogni funzione e ogni parte di codice. Anche il nome delle variabili 
potrebbe essere più esplicativo per rendere il codice più facile da leggere e capire.

ENG:
In some functions such as returnToSnakeCaseCode and returnToCamelCaseCode you have written only a screen print instead
of returning the actual code. Probably it is a mistake and you should implement the missing code. Some of the functions 
that modify the string, such as capitalize, casefold, title, upper and lower,
use always the first input value, ignoring any other input. You could check if there are other inputs
and, if present, use them to modify the correct string. The calculateOutput function is quite long and complex.
You could make it more readable by separating the various cases into different functions and/or adding comments that
explain what the code does in each part. The showContextMenu function is quite long and repetitive. You could
create a separate function for each type of action of the drop-down menu (such as replace, split, capitalize,
etc.) and call them based on the selected action. The camelCaseToSnakeCase function is currently implemented in such a way
to accept only two input formats (camelCase and snake_case). You could make the function more general by
to accept one more argument that indicates the desired output format. In general, the code could
benefit from more comments that explain what each function and each part of the code does. Even the name of the variables
could be more explanatory to make the code easier to read and understand.

"""


class StringNode(AbstractNodeInterface):
    resetValue = "HelloWorld!"
    width = 120
    height = 80
    colorTrain = [QColor(132, 255, 121), QColor(255, 121, 166), QColor(233, 255, 121), QColor(121, 255, 210),
                  QColor(244, 121, 255), QColor(43, 30, 20), QColor(143, 121, 255), QColor(121, 199, 255), ]
    isReplaceNode = False
    menuReturnValue = "string"

    def __init__(self, value: str = "HelloWorld", inNum=1, outNum=1, parent=None):
        super().__init__(value, inNum, outNum, parent)
        self.setClassName("StringNode")
        self.setName("StringNode")
        self.changeSize(self.width, self.height)
        self.changeInputValue(0, value, True)
        self.menuReturnValue = "string"

    def calculateOutput(self, plugIndex):
        if not self.isReplaceNode:
            value = self.inPlugs[0].getValue()
            self.outPlugs[plugIndex].setValue(value)
        if len(self.inPlugs) > 2:
            string1 = self.inPlugs[1].getValue()
            string2 = self.inPlugs[2].getValue()
            string0 = self.inPlugs[0].getValue()
            string0 = string0.replace(str(string1), str(string2))
            self.outPlugs[plugIndex].setValue(str(string0))
        else:
            string = self.inPlugs[0].getValue()
            self.outPlugs[plugIndex].setValue(str(string))
        return self.outPlugs[plugIndex].getValue()

    def getCode(self):
        if self.menuReturnValue == "replace":
            return self.returnReplaceCode()
        elif self.menuReturnValue == "split":
            return self.returnSplitCode()
        elif self.menuReturnValue == "strip":
            return self.returnStripCode()
        elif self.menuReturnValue == "capitalize":
            return self.returnCapitalizeCode()
        elif self.menuReturnValue == "casefold":
            return self.returnCasefoldCode()
        elif self.menuReturnValue == "title":
            return self.returnTitleCode()
        elif self.menuReturnValue == "upper":
            return self.returnUpperCode()
        elif self.menuReturnValue == "lower":
            return self.returnLowerCode()
        elif self.menuReturnValue == "to snake_case":
            return self.returnToSnakeCaseCode()
        elif self.menuReturnValue == "to camelCase":
            return self.returnToCamelCaseCode()
        else:
            return self.returnStringCode()

    def redesign(self):
        self.changeSize(self.width, self.height)
        self.updateAll()

    def showContextMenu(self, position):
        contextMenu = QMenu()
        contextMenu.addSection("string")
        actionString = contextMenu.addAction("string")
        actionReplace = contextMenu.addAction("replace")
        actionSplit = contextMenu.addAction("split")
        actionStrip = contextMenu.addAction("strip")
        actionCapitalize = contextMenu.addAction("capitalize")
        actionCasefold = contextMenu.addAction("casefold")
        actionTitle = contextMenu.addAction("title")
        actionUpper = contextMenu.addAction("upper")
        actionLower = contextMenu.addAction("lower")
        actionToSnakeCase = contextMenu.addAction("to snake_case")
        actionToCamelCase = contextMenu.addAction("to camelCase")
        action = contextMenu.exec(position)
        self.menuReturnValue = action.text()
        if action == actionReplace:
            self.replace()
        elif action == actionSplit:
            self.split()
        elif action == actionStrip:
            self.strip()
        elif action == actionCapitalize:
            self.capitalize()
        elif action == actionCasefold:
            self.casefold()
        elif action == actionTitle:
            self.title()
        elif action == actionUpper:
            self.upper()
        elif action == actionLower:
            self.lower()
        elif action == actionString:
            self.string()
        elif action == actionToSnakeCase:
            self.ToSnakeCase()
        elif action == actionToCamelCase:
            self.ToCamelCase()

        if self.nodeData.outConnections:
            for connection in self.nodeData.outConnections:
                connection.updateValue()
        else:
            self.nodeData.calculate()

    def string(self):
        self.valueType = str
        self.setGraphicTitleText("StringNode")
        self.removeAllUnnecessaryPlugs()
        if self.inPlugs[0].getValue() is not None:
            return self.inPlugs[0].getValue()

    def returnStringCode(self):
        if not self.inPlugs[0].inConnection:
            return f'{self.getTitle()} = "{self.inPlugs[0].getValue()}"'
        inPlugNodeName, code = self.getCodeFromInput(0)
        return f'{code}\n{self.getTitle()} = str({inPlugNodeName})'

    def split(self):
        self.valueType = list
        self.setGraphicTitleText("SplitNode")
        self.removeAllUnnecessaryPlugs()
        self.addInPlug("splitChar")
        self.changeInputValue(1, " ", True)
        self.redesign()

    def returnSplitCode(self):
        in0Title, in0Code = self.getCodeFromInput(0)
        in1Title, in1Code = self.getCodeFromInput(1)
        return f'{in0Code}\n{in1Code}\n{self.getTitle()} = {in0Title}.split({in1Title})'

    def capitalize(self):
        self.valueType = str
        self.setGraphicTitleText("CapitalizeNode")
        self.removeAllUnnecessaryPlugs()
        string = self.inPlugs[0].getValue().capitalize()
        self.changeInputValue(0, string, True)
        self.redesign()

    def returnCapitalizeCode(self):
        in0Title, in0Code = self.getCodeFromInput(0)
        return f'{in0Code}\n{self.getTitle()} = {in0Title}.capitalize()'

    def casefold(self):
        self.valueType = str
        self.setGraphicTitleText("CasefoldNode")
        self.removeAllUnnecessaryPlugs()
        string = self.inPlugs[0].getValue().casefold()
        self.changeInputValue(0, string, True)
        self.redesign()

    def returnCasefoldCode(self):
        in0Title, in0Code = self.getCodeFromInput(0)
        return f'{in0Code}\n{self.getTitle()} = {in0Title}.casefold()'

    def title(self):
        self.valueType = str
        self.setGraphicTitleText("TitleNode")
        self.removeAllUnnecessaryPlugs()
        string = self.inPlugs[0].getValue().title()
        self.changeInputValue(0, string, True)
        self.redesign()

    def returnTitleCode(self):
        in0Title, in0Code = self.getCodeFromInput(0)
        return f'{in0Code}\n{self.getTitle()} = {in0Title}.title()'

    def upper(self):
        self.valueType = str
        self.setGraphicTitleText("UpperNode")
        self.removeAllUnnecessaryPlugs()
        string = self.inPlugs[0].getValue().upper()
        self.changeInputValue(0, string, True)
        self.redesign()

    def returnUpperCode(self):
        in0Title, in0Code = self.getCodeFromInput(0)
        return f'{in0Code}\n{self.getTitle()} = {in0Title}.upper()'

    def lower(self):
        self.valueType = str
        self.setGraphicTitleText("LowerNode")
        self.removeAllUnnecessaryPlugs()
        string = self.inPlugs[0].getValue().lower()
        self.changeInputValue(0, string, True)
        self.redesign()

    def returnLowerCode(self):
        in0Title, in0Code = self.getCodeFromInput(0)
        return f'{in0Code}\n{self.getTitle()} = {in0Title}.lower()'

    def strip(self):
        self.valueType = str
        self.setGraphicTitleText("StripNode")
        self.removeAllUnnecessaryPlugs()
        string = self.inPlugs[0].getValue().strip()
        self.changeInputValue(0, string, True)
        self.redesign()

    def returnStripCode(self):
        in0Title, in0Code = self.getCodeFromInput(0)
        return f'{in0Code}\n{self.getTitle()} = {in0Title}.strip()'

    def replace(self):
        self.valueType = str
        self.setGraphicTitleText("ReplaceNode")
        self.removeAllUnnecessaryPlugs()
        self.addInPlug("replace")
        self.addInPlug("with")
        self.redesign()

    def returnReplaceCode(self):
        in0Title, in0Code = self.getCodeFromInput(0)
        in1Title, in1Code = self.getCodeFromInput(1)
        in2Title, in2Code = self.getCodeFromInput(2)
        code = f'{in0Code}\n{in1Code}\n{in2Code}\n{self.getTitle()} = {in0Title}.replace({in1Title}, {in2Title})'
        print(f"Debug from {self.getTitle()}:\n{code}")
        return code

    def ToSnakeCase(self):
        self.valueType = str
        self.setGraphicTitleText("ToSnakeCaseNode")
        self.removeAllUnnecessaryPlugs()
        string = self.inPlugs[0].getValue()
        snakeCase = self.camelCaseToSnakeCase(string, "snake_case")
        self.changeInputValue(0, snakeCase, True)
        self.redesign()

    def returnToSnakeCaseCode(self):
        in0Title, in0Code = self.getCodeFromInput(0)
        print("snakeCase to be implemented")

    def ToCamelCase(self):
        self.valueType = str
        self.setGraphicTitleText("ToCamelCaseNode")
        self.removeAllUnnecessaryPlugs()
        string = self.inPlugs[0].getValue()
        camelCase = self.camelCaseToSnakeCase(string, "camelCase")
        self.changeInputValue(0, camelCase, True)
        self.redesign()

    def returnToCamelCaseCode(self):
        in0Title, in0Code = self.getCodeFromInput(0)
        print("camelCase to be implemented")

    def camelCaseToSnakeCase(self, string, to_format):
        import re
        if string == "":
            return ""
        if to_format == "camelCase":
            # verifica se la stringa è già in formato camelCase
            if string == string.title():
                return string
            # verifica se la stringa è già in formato snake_case
            elif "_" in string:
                # sostituisce ogni "_" con uno spazio
                string = string.replace("_", " ")
                # trasforma ogni parola in formato camelCase
                string = re.sub(r"(\w)([A-Z])", r"\1 \2", string).title().replace(" ", "")
                return string
            else:
                # trasforma la stringa in formato camelCase
                return string
        elif to_format == "snake_case":
            # verifica se la stringa è già in formato snake_case
            if "_" in string:
                return string
            # verifica se la stringa è già in formato camelCase
            elif string == string.title():
                # sostituisce ogni spazio con un "_"
                string = re.sub(r"([A-Z])", r" \1", string).lower().replace(" ", "_")
                return string
            else:
                # trasforma la stringa in formato snake_case
                return string.lower().replace(" ", "_")
        else:
            return "Formato non valido"
