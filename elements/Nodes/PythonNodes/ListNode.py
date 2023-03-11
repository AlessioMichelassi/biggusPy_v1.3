import math
import random
from typing import Union

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface

"""TO DO: 

ITA:
In generale, il codice sembra ben scritto e organizzato. Tuttavia, sebbene le operazioni siano corrette, 
è possibile che ci siano alcuni miglioramenti che si possono apportare per migliorare l'efficienza del codice o la 
sua leggibilità.

Ad esempio, invece di utilizzare una serie di istruzioni if-elif-else nel metodo getCode(), è possibile utilizzare un 
dizionario che mappa ogni valore possibile per la variabile menuReturnValue con una funzione corrispondente. In 
questo modo, il codice diventa più facile da leggere e modificare in futuro.

Un altro possibile miglioramento è la rimozione di codice ripetuto all'interno dei metodi che gestiscono le 
operazioni sulle liste. Ad esempio, la parte in cui viene estratto il valore dall'input e viene verificato se è nullo 
potrebbe essere spostata in un metodo a parte che viene richiamato ogni volta che serve. Inoltre, alcune delle 
operazioni che manipolano la lista, come l'inserimento e l'aggiunta di elementi, potrebbero essere scritte in modo 
più semplice utilizzando la sintassi del linguaggio.

Infine, si potrebbe considerare l'aggiunta di alcuni controlli di errore nei metodi che gestiscono le operazioni 
sulle liste, ad esempio per verificare se l'indice fornito per l'operazione di inserimento è valido o se il valore 
che si sta cercando di rimuovere non esiste nella lista.

ENG:
In general, the code seems well written and organized. However, although the operations are correct,
there may be some improvements that can be made to improve the efficiency of the code or its readability.

For example, instead of using a series of if-elif-else statements in the getCode() method, you can use a
dictionary that maps each possible value for the menuReturnValue variable with a corresponding function. In
this way, the code becomes easier to read and modify in the future.

Another possible improvement is the removal of repeated code within the methods that handle
list operations. For example, the part where the value is extracted from the input and checked if it is null
could be moved to a separate method that is called every time it is needed. In addition, some of the
operations that manipulate the list, such as inserting and adding elements, could be written in a simpler way using the
syntax of the language.

Finally, you could consider adding some error checks in the methods that handle list operations, for example to check 
if the index provided for the insertion operation is valid or if the value
that you are trying to remove does not exist in the list.

"""


class ListNode(AbstractNodeInterface):
    _className = "ListNode"
    menuReturnValue = "list"
    startValue = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    width = 120
    height = 80
    colorTrain = [QColor(219, 255, 190), QColor(226, 190, 255), QColor(226, 190, 255), QColor(190, 252, 255),
                  QColor(255, 155, 127), QColor(127, 227, 255), QColor(127, 227, 255), QColor(163, 255, 127), ]

    def __init__(self, value: list[Union[int, float, str]] = None, inNum=1, outNum=1):
        super().__init__(inNum, outNum)
        self.setClassName(self._className)
        self.setName("ListNode")
        if value is not None:
            self.startValue = value
        else:
            value = self.startValue
        self.changeInputValue(0, value)
        self.changeSize(self.width, self.height)

    def calculateOutput(self, plugIndex):
        value = self.inPlugs[0].getValue()
        valueList = self.checkList(value)
        result = valueList
        if len(self.inPlugs) > 1:
            if self.menuReturnValue == "append":
                list2 = self.inPlugs[1].getValue()
                if len(list2) > 0:
                    result += list2
            elif self.menuReturnValue == "insert":
                index = self.inPlugs[1].getValue()
                list1 = self.inPlugs[2].getValue()
                if index < len(valueList):
                    try:
                        result = valueList.insert(index, list1)
                    except IndexError:
                        result = "index out of range"
            elif self.menuReturnValue == "remove":
                value = self.inPlugs[1].getValue()
                try:
                    result = valueList.remove(value)
                except ValueError:
                    result = "node not in list"
            elif self.menuReturnValue == "index":
                value = self.inPlugs[1].getValue()
                try:
                    result = valueList[value]
                except IndexError:
                    result = "Out of range"
            elif self.menuReturnValue == "extend":
                list2 = self.inPlugs[1].getValue()
                try:
                    if len(list2) > 0:
                        result.extend(list2)
                except TypeError:
                    result = "list2 is not a list"
        self.outPlugs[plugIndex].setValue(result)
        return self.outPlugs[plugIndex].getValue()

    def getCode(self):
        if self.menuReturnValue == "list":
            return self.returnListCode()
        elif self.menuReturnValue == "append":
            return self.returnAppendCode()
        elif self.menuReturnValue == "insert":
            return self.returnInsertCode()
        elif self.menuReturnValue == "pop":
            return self.returnPopCode()
        elif self.menuReturnValue == "remove":
            return self.returnRemoveCode()
        elif self.menuReturnValue == "clear":
            return self.returnClearCode()
        elif self.menuReturnValue == "index":
            return self.returnIndexCode()
        elif self.menuReturnValue == "sort":
            return self.returnSortCode()
        elif self.menuReturnValue == "shuffle":
            return self.returnShuffleCode()
        elif self.menuReturnValue == "reverse":
            return self.returnReverseCode()
        elif self.menuReturnValue == "extend":
            return self.returnExtendCode()
        elif self.menuReturnValue == "reset":
            return self.returnResetCode()

    def redesign(self):
        self.nodeGraphic.redesign(120, 80)

    @staticmethod
    def checkList(value):
        if isinstance(value, list):
            return value
        input_string = value.strip()
        # controlla se inizia con "[" e finisce con "]"
        if input_string.startswith("[") and input_string.endswith("]"):
            # se sì, rimuovi "[" e "]" e splitta la stringa restante sulla base della virgola
            input_list = input_string[1:-1].split(",")
        else:
            # altrimenti, splitta la stringa sulla base della virgola
            input_list = input_string.split(",")
        # prova a convertire ciascun elemento della lista in un numero (intero o decimale)
        try:
            return [int(x) if x.isdigit() else float(x) for x in input_list]
        except ValueError:
            # se non è possibile convertire un elemento in un numero, restituisci la lista come lista di stringhe
            return [x.strip() for x in input_list]

    def showContextMenu(self, position):
        """
        Il nodo deve avere un menu contestuale che permetta come nello stringNode di eseguire operazioni su una lista
        come append, insert, pop, remove, clear, index, sort, shuffle, reverse, extend
        :param position:
        :return:
        """
        contextMenu = QMenu()
        contextMenu.addSection("list")
        actions = {
            "list": self.doList,
            "append": self.doAppend,
            "insert": self.doInsert,
            "pop": self.doPop,
            "remove": self.doRemove,
            "clear": self.doClear,
            "index": self.doIndex,
            "sort": self.doSort,
            "shuffle": self.doShuffle,
            "reverse": self.doReverse,
            "extend": self.doExtend,
            "reset": self.doReset
        }
        for action_name in actions:
            contextMenu.addAction(action_name)

        if selected_action := contextMenu.exec(position):
            action_func = actions[selected_action.text()]
            action_func()
            self.menuReturnValue = selected_action.text()

        if self.nodeData.outConnections:
            for connection in self.nodeData.outConnections:
                connection.updateValue()
        else:
            self.nodeData.calculate()

    def doAppend(self):
        self.removeAllUnnecessaryPlugs()
        self.addInPlug("append")
        self.changeInputValue(1, [])
        self.menuReturnValue = "append"
        self.updateAll()

    def returnAppendCode(self):
        in0Title, in0Code = self.getCodeFromInput(0)
        in1Title, in1Code = self.getCodeFromInput(1)
        return f"{in0Code}\n{in1Title} = {in1Code}\n{in0Title}.append({in1Title})"

    def doInsert(self):
        self.removeAllUnnecessaryPlugs()
        self.addInPlug("index")
        self.addInPlug("insert")
        self.changeInputValue(1, 0)
        self.changeInputValue(2, [])
        self.menuReturnValue = "insert"
        self.updateAll()

    def returnInsertCode(self):
        in0Title, in0Code = self.getCodeFromInput(0)
        in1Title, in1Code = self.getCodeFromInput(1)
        in2Title, in2Code = self.getCodeFromInput(2)
        return f"{in0Code}\n{in1Title} = {in1Code}\n{in2Title} = {in2Code}\n{in0Title}.insert({in1Title}, {in2Title})"

    def doPop(self):
        self.removeAllUnnecessaryPlugs()
        self.menuReturnValue = "pop"
        value = self.inPlugs[0].getValue()
        if value is None:
            value = []
        valueList = self.checkList(value)
        valueList.pop()
        self.changeInputValue(0, valueList)
        self.updateAll()

    def returnPopCode(self):
        in0Title, in0Code = self.getCodeFromInput(0)
        return f"{in0Code}\n{in0Title}.pop()"

    def doRemove(self):
        self.removeAllUnnecessaryPlugs()
        self.addInPlug("remove")
        self.changeInputValue(1, [])
        self.menuReturnValue = "remove"
        self.updateAll()

    def returnRemoveCode(self):
        in0Title, in0Code = self.getCodeFromInput(0)
        in1Title, in1Code = self.getCodeFromInput(1)
        return f"{in0Code}\n{in1Title} = {in1Code}\n{in0Title}.remove({in1Title})"

    def doClear(self):
        self.removeAllUnnecessaryPlugs()
        self.menuReturnValue = "clear"
        value = self.inPlugs[0].getValue()
        if value is None:
            value = []
        valueList = self.checkList(value)
        valueList.clear()
        self.changeInputValue(0, valueList)
        self.updateAll()

    def returnClearCode(self):
        in0Title, in0Code = self.getCodeFromInput(0)
        return f"{in0Code}\n{in0Title}.clear()"

    def doIndex(self):
        self.removeAllUnnecessaryPlugs()
        self.addInPlug("index")
        self.changeInputValue(1, 0)
        self.menuReturnValue = "index"
        self.updateAll()

    def returnIndexCode(self):
        in0Title, in0Code = self.getCodeFromInput(0)
        in1Title, in1Code = self.getCodeFromInput(1)
        return f"{in0Code}\n{in1Title} = {in1Code}\n{in0Title}.index({in1Title})"

    def doSort(self):
        self.removeAllUnnecessaryPlugs()
        self.menuReturnValue = "sort"
        value = self.inPlugs[0].getValue()
        if value is None:
            value = []
        valueList = self.checkList(value)
        valueList.sort()
        self.changeInputValue(0, valueList)
        self.updateAll()

    def returnSortCode(self):
        in0Title, in0Code = self.getCodeFromInput(0)
        return f"{in0Code}\n{in0Title}.sort()"

    def doShuffle(self):
        self.removeAllUnnecessaryPlugs()
        self.menuReturnValue = "shuffle"
        value = self.inPlugs[0].getValue()
        if value is None:
            value = []
        valueList = self.checkList(value)
        random.shuffle(valueList)
        self.changeInputValue(0, valueList)
        self.updateAll()

    def returnShuffleCode(self):
        in0Title, in0Code = self.getCodeFromInput(0)
        return f"{in0Code}\n{in0Title} = random.shuffle({in0Title})"

    def doReverse(self):
        self.removeAllUnnecessaryPlugs()
        self.menuReturnValue = "reverse"
        value = self.inPlugs[0].getValue()
        if value is None:
            value = []
        valueList = self.checkList(value)
        valueList.reverse()
        self.changeInputValue(0, valueList)
        self.updateAll()

    def returnReverseCode(self):
        in0Title, in0Code = self.getCodeFromInput(0)
        return f"{in0Code}\n{in0Title} = {in0Title}.reverse()"

    def doExtend(self):
        self.removeAllUnnecessaryPlugs()
        self.addInPlug("extend")
        self.changeInputValue(1, [])
        self.menuReturnValue = "extend"
        self.updateAll()

    def returnExtendCode(self):
        in0Title, in0Code = self.getCodeFromInput(0)
        in1Title, in1Code = self.getCodeFromInput(1)
        return f"{in0Code}\n{in1Title} = {in1Code}\n{in0Title}.extend({in1Title})"

    def doReset(self):
        self.removeAllUnnecessaryPlugs()
        self.menuReturnValue = "reset"
        self.changeInputValue(0, self.startValue)
        self.updateAll()

    def returnResetCode(self):
        return self.returnListCode()

    def doList(self):
        self.removeAllUnnecessaryPlugs()
        self.menuReturnValue = "list"
        value = self.inPlugs[0].getValue()
        if value is None:
            value = self.startValue
        self.changeInputValue(0, value)
        self.updateAll()

    def returnListCode(self):
        if not self.inPlugs[0].inConnection:
            return f'{self.getTitle()} = {self.inPlugs[0].getValue()}'
        inPlugNodeName, code = self.getCodeFromInput(0)
        return f'{code}\n{self.getTitle()} = str({inPlugNodeName})'
