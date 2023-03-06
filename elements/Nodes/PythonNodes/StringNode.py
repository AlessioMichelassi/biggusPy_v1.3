# -*- coding: utf-8 -*-
import math
import random

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMenu

from elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface


class StringNode(AbstractNodeInterface):
    resetValue = "HelloWorld!"
    width = 120
    height = 80
    colorTrain = [QColor(132, 255, 121), QColor(255, 121, 166), QColor(233, 255, 121), QColor(121, 255, 210),
                  QColor(244, 121, 255), QColor(43, 30, 20), QColor(143, 121, 255), QColor(121, 199, 255), ]
    isReplaceNode = False

    def __init__(self, value: str = "HelloWorld", inNum=1, outNum=1, parent=None):
        super().__init__(value, inNum, outNum, parent)
        self.setClassName("StringNode")
        self.setName("StringNode")
        self.changeSize(self.width, self.height)
        self.changeInputValue(0, value, True)

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

    def redesign(self):
        self.changeSize(self.width, self.height)

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

    def split(self):
        self.valueType = list
        self.setGraphicTitleText("SplitNode")
        self.removeAllUnnecessaryPlugs()
        self.addInPlug("splitChar")
        self.changeInputValue(1, " ", True)
        self.redesign()

    def capitalize(self):
        self.valueType = str
        self.setGraphicTitleText("CapitalizeNode")
        self.removeAllUnnecessaryPlugs()
        string = self.inPlugs[0].getValue().capitalize()
        self.changeInputValue(0, string, True)
        self.redesign()

    def casefold(self):
        self.valueType = str
        self.setGraphicTitleText("CasefoldNode")
        self.removeAllUnnecessaryPlugs()
        string = self.inPlugs[0].getValue().casefold()
        self.changeInputValue(0, string, True)
        self.redesign()

    def title(self):
        self.valueType = str
        self.setGraphicTitleText("TitleNode")
        self.removeAllUnnecessaryPlugs()
        string = self.inPlugs[0].getValue().title()
        self.changeInputValue(0, string, True)
        self.redesign()

    def upper(self):
        self.valueType = str
        self.setGraphicTitleText("UpperNode")
        self.removeAllUnnecessaryPlugs()
        string = self.inPlugs[0].getValue().upper()
        self.changeInputValue(0, string, True)
        self.redesign()

    def lower(self):
        self.valueType = str
        self.setGraphicTitleText("LowerNode")
        self.removeAllUnnecessaryPlugs()
        string = self.inPlugs[0].getValue().lower()
        self.changeInputValue(0, string, True)
        self.redesign()

    def strip(self):
        self.valueType = str
        self.setGraphicTitleText("StripNode")
        self.removeAllUnnecessaryPlugs()
        string = self.inPlugs[0].getValue().strip()
        self.changeInputValue(0, string, True)
        self.redesign()

    def replace(self):
        self.valueType = str
        self.setGraphicTitleText("ReplaceNode")
        self.removeAllUnnecessaryPlugs()
        self.addInPlug("replace")
        self.addInPlug("with")
        self.redesign()

    def ToSnakeCase(self):
        self.valueType = str
        self.setGraphicTitleText("ToSnakeCaseNode")
        self.removeAllUnnecessaryPlugs()
        string = self.inPlugs[0].getValue()
        snakeCase = self.camelCaseToSnakeCase(string, "snake_case")
        self.changeInputValue(0, snakeCase, True)
        self.redesign()

    def ToCamelCase(self):
        self.valueType = str
        self.setGraphicTitleText("ToCamelCaseNode")
        self.removeAllUnnecessaryPlugs()
        string = self.inPlugs[0].getValue()
        camelCase = self.camelCaseToSnakeCase(string, "camelCase")
        self.changeInputValue(0, camelCase, True)
        self.redesign()

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
