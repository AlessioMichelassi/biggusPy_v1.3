import ast


class CodeToNode:
    lastNode = None
    lastIfNode = None
    lastForNode = None
    lastFunctionNode = None
    lastWhileNode = None
    code = None
    functionNodeList = []
    def __init__(self, canvas):
        self.canvas = canvas

    def createNodeFromCode(self, _code: str):
        """
        ITA:
            Questo metodo crea un nodo a partire dal codice passato come parametro grazie alla libreria Ast.
            Ast è una libreria che permette di analizzare il codice python e di creare un AST (Abstract Syntax Tree)
            ovvero un albero sintattico astratto. Questo albero viene poi analizzato per creare i nodi.
            Con parseCode() viene creato l'AST e con nodeSearch() viene analizzato l'AST per creare i nodi.
            una volta che tutti i nodi sono stati creati, vengono posizionati nella scena e quindi vengono creati i collegamenti.
        ENG:
            This method creates a node from the code passed as a parameter thanks to the Ast library.
            Ast is a library that allows you to analyze the python code and create an AST (Abstract Syntax Tree)
            that is, an abstract syntax tree. This tree is then analyzed to create the nodes.
            With parseCode () the AST is created and with nodeSearch () the AST is analyzed to create the nodes.
            once all the nodes have been created, they are positioned in the scene and then the connections are created.
        :param _code:
        :return:
        """
        self.code = _code
        parsedCode = self.parseCode(_code)
        self.nodeSearch(parsedCode)
        self.setNodePosition()
        self.createConnections()

    @staticmethod
    def parseCode(_code: str):
        # parse the code into an AST
        return ast.parse(_code)

    def nodeSearch(self, parsedCode: ast.AST):
        for node in ast.walk(parsedCode):
            if isinstance(node, ast.FunctionDef):
                self.createFunctionNode(node)
                break
            elif isinstance(node, ast.For):
                print("For")
            elif isinstance(node, ast.If):
                self.createIfNode(node)
            elif isinstance(node, ast.Call):
                try:
                    if isinstance(node.func, ast.Name):
                        self.createCallNode(node)
                    elif isinstance(node.func, ast.Attribute):
                        self.createCallNode(node)
                except Exception as e:
                    print("*" * 20)
                    print(e)
                    print("*" * 20)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        self.createVariableNode(target.id, node.value)

    def setNodePosition(self):
        pass

    def createConnections(self):
        pass

    def createVariableNode(self, name: str, value):
        """
        ITA:
            Crea un nodo per la variabile in base al tipo di valore assegnato
        ENG:
            Create a node for the variable based on the type of value assigned
        :param name:
        :param value:
        :return:
        """
        node = []
        # ast.Num sono i numeri
        if isinstance(value, ast.Num):
            node.append(self.returnBiggusPyNode("NumberNode", value.n, name))
        # ast.Str sono le stringhe
        elif isinstance(value, ast.Str):
            node.append(self.returnBiggusPyNode("StringNode", value.s, name))
        # ast.List sono le liste
        elif isinstance(value, ast.List):
            node.append(self.returnBiggusPyNodeWithElements("ListNode", value, name))
        # ast.Tuple sono le tuple
        elif isinstance(value, ast.Tuple):
            node.append(self.returnBiggusPyNodeWithElements("TupleNode", value, name))
        # ast.Dict sono i dizionari
        elif isinstance(value, ast.Dict):
            node.append(self.returnBiggusPyNodeDictionary("DictNode", value, name))
        # ast.Name sono le variabili
        elif isinstance(value, ast.Name):
            node.append(self.returnBiggusPyNode("VariableNode", value.id, name))
        # ast.Attribute sono gli attributi tipo self.var o
        elif isinstance(value, ast.Attribute):
            pass
        # ast.Call sono le chiamate a funzioni tipo print()
        elif isinstance(value, ast.Call):
            pass
        # ast.BinOp sono le operazioni binarie tipo 1 + 1
        elif isinstance(value, ast.BinOp):
            self.createBinOpNode(value, name)

        else:
            self.searchForOtherTypes(value, name)

    def searchForOtherTypes(self, value, name):
        # sourcery skip: guard, merge-duplicate-blocks, remove-empty-nested-block, remove-pass-elif, remove-redundant-if
        # ast.UnaryOp sono le operazioni unarie tipo -1
        if isinstance(value, ast.UnaryOp):
            pass
        # ast.BoolOp sono le operazioni booleane tipo 1 == 1 and 2 == 2
        elif isinstance(value, ast.BoolOp):
            pass
        # ast.Compare sono le operazioni di confronto tipo 1 == 1
        elif isinstance(value, ast.Compare):
            pass
        # ast.Subscript sono gli indici tipo lista[0] o dizionario["chiave"]
        elif isinstance(value, ast.Subscript):
            pass
        # ast.Index sono gli indici tipo lista[0] o dizionario["chiave"] e sono usati per creare i nodi
        elif isinstance(value, ast.Index):
            pass
        # ast.Slice sono gli slice tipo lista[0:1] o lista[0:1:2]
        elif isinstance(value, ast.Slice):
            pass

    def returnBiggusPyNode(self, className: str, value, name):
        if value is None:
            node = self.canvas.createNode(className, "")
        else:
            node = self.canvas.createNode(className, value)
            node.changeInputValue(0, value, True)
        if node is not None:
            node.setName(name)
            self.canvas.addNode(node)
            if self.lastNode is not None:
                self.updateNodePositionByLastNode(node)
            self.lastNode = node
            return node
        else:
            print("WARNING: Node not created")
            return None

    def returnBiggusPyNodeWithElements(self, className: str, value, name):
        """
        ITA:
            nel caso in cui il nodo debba avere degli elementi, come una lista o un dizionario,
            questo metodo viene usato.
        :param className:
        :param value:
        :param name:
        :return:
        """
        elements = [el.value for el in value.elts]
        # elements = [el.n if isinstance(el, ast.Num) else el.value for el in value.elts]
        node = self.canvas.createNode(className, elements)
        if node is not None:
            node.setName(name)
            self.canvas.addNode(node)
            if self.lastNode is not None:
                self.updateNodePositionByLastNode(node)
            self.lastNode = node
            return node
        else:
            print("WARNING: Node not created")
            return None

    def returnBiggusPyNodeDictionary(self, className: str, value, name):
        """
        ITA:
            nel caso di un dizionario una volta trovati key e value, poiche sono due liste,
            vengono convertiti in un dizionario.
        ENG:
            in the case of a dictionary once keys and values are found, because they are two lists,
            they are converted into a dictionary.
        :param className:
        :param value:
        :param name:
        :return:
        """
        keys = [el.s for el in value.keys]
        values = [el.n if isinstance(el, ast.Num) else (el.s if isinstance(el, ast.Str) else el.id) for el in
                  value.values]
        dictionary = dict(zip(keys, values))
        node = self.canvas.createNode(className, dictionary)
        if node is not None:
            node.setName(name)
            self.canvas.addNode(node)
            if self.lastNode is not None:
                self.updateNodePositionByLastNode(node)
            self.lastNode = node
            return node
        else:
            print("WARNING: Node not created")
            return None

    # ---------------    BINOP NODE    ----------------
    """
    ITA: 
        Per BinOp si intende un nodo che ha un operatore binario, come ad esempio
        l'addizione, la sottrazione, la moltiplicazione, la divisione, ecc...
        In questo caso se la variabile assegnata è fra due Numeri, allora viene
        creato un nodo di tipo MathNode, se fra due stringhe viene creato un
        nodo di tipo StringNode, se fra due liste viene creato un nodo di tipo
        ListNode, se fra due tuple viene creato un nodo di tipo TupleNode, se
        fra due set viene creato un nodo di tipo SetNode, se fra due dizionari
        viene creato un nodo di tipo DictNode, se fra due variabili viene creato
        un nodo di tipo VariableNode.
    ENG:
        For BinOp it means a node that has a binary operator, such as
        addition, subtraction, multiplication, division, etc ...
        In this case if the assigned variable is between two Numbers, then it is
        created a MathNode type node, if between two strings a StringNode type node is created,
        if between two lists a ListNode type node is created, if between two tuples a TupleNode
        type node is created, if between two sets a SetNode type node is created, if between two
        dictionaries a DictNode type node is created, if between two variables a VariableNode
        type node is created.
    """

    @staticmethod
    def returnOperator(value):
        """
        ITA:
            Questo metodo ritorna l'operatore binario.
        ENG:
            This method returns the binary operator.
        :param value:
        :return:
        """
        if isinstance(value, ast.Add):
            return "+"
        elif isinstance(value, (ast.Sub, ast.Subtract)):
            return "-"
        elif isinstance(value, ast.Mult):
            return "*"
        elif isinstance(value, ast.Div):
            return "/"
        elif isinstance(value, ast.FloorDiv):
            return "//"
        elif isinstance(value, ast.Mod):
            return "%"
        elif isinstance(value, ast.Pow):
            return "**"
        elif isinstance(value, ast.LShift):
            return "<<"
        elif isinstance(value, ast.RShift):
            return ">>"
        elif isinstance(value, ast.BitOr):
            return "|"
        elif isinstance(value, ast.BitXor):
            return "^"
        elif isinstance(value, ast.BitAnd):
            return "&"
        elif isinstance(value, ast.MatMult):
            return "@"
        else:
            return None

    def createBinOpNode(self, value, name):
        """
        ITA:
            Questo metodo viene chiamato quando viene trovato un nodo di tipo BinOp,
            ovvero una somma o una sottrazione o una moltiplicazione o una divisione.
            Generalmente quando si passa un codice è nella forma a = 10 b = 20 c = a + b
            quindi nel caso in cui a e b sono già state create, viene controllato il tipo
            di variabile. se a = "Hello" e b = "World" in python il risultato è "HelloWorld"
            ma in biggus py per farlo serve un nodo di tipo StringNode, quindi viene creato
            un nodo di tipo StringNode.
        ENG:
            This method is called when a BinOp type node is found.
            Depending on the type of variable that is assigned, a different type node is created.
            For example if a = "Hello" and b = "World" in python the result is "HelloWorld"
            but in biggus py to do it a StringNode type node is needed, so a StringNode type node is created.
        :param value:
        :param name:
        :return:
        """
        assignmentVariable = self.returnBiggusPyNode("VariableNode", value, name)
        operator = self.returnOperator(value.op)
        if assignmentVariable is None:
            print("WARNING: assignmentVariable is None")
            return None
        if operator is None:
            print("WARNING: operator is None")
            return None
        opNode = None
        left = value.left
        right = value.right
        opNode = self.searchWhichNodeToCreate(left, right, operator, value, name)
        print(f"opNode: {str(opNode)}")
        self.checkIfLeftAndRightVariablesExist(left, right, opNode, assignmentVariable, name)

    def returnType(self, value):
        """
        ITA:
            Questo metodo ritorna il tipo di variabile.
        ENG:
            This method returns the type of variable.
        :param value:
        :return:
        """
        if isinstance(value, ast.Num):
            return "Number"
        elif isinstance(value, ast.Str):
            return "String"
        elif isinstance(value, ast.List):
            return "List"
        elif isinstance(value, ast.Tuple):
            return "Tuple"
        elif isinstance(value, ast.Set):
            return "Set"
        elif isinstance(value, ast.Dict):
            return "Dict"
        elif isinstance(value, ast.Name):
            return "Variable"
        else:
            return None

    def searchWhichNodeToCreate(self, left, right, operator, value, name):
        leftType = self.returnType(left)
        rightType = self.returnType(right)
        print(f"leftType: {leftType}")
        # Crea l'op node dopo aver controllato se left e right esistono
        # se esistono e il className di left è NumberNode crea il mathNode
        # altrimenti crea una string etc etc... altrimenti crea un variableNode
        # e ritorna un opNode che adesso andrà creato nella lista dei nodi!
        arg1 = self.canvas.getNodeByName(left.id)
        opNode = None
        if arg1 is not None:
            if arg1.className == "NumberNode":
                opNode = self.returnBiggusPyNode("MathNode", value, name)
                opNode.operator = operator
            elif arg1.className == "StringNode":
                opNode = self.returnBiggusPyNode("StringNode", value, name)
                opNode.operator = operator
            elif arg1.className == "ListNode":
                opNode = self.returnBiggusPyNode("ListNode", value, name)
                opNode.operator = operator
            elif arg1.className == "TupleNode":
                opNode = self.returnBiggusPyNode("TupleNode", value, name)
                opNode.operator = operator
            elif arg1.className == "SetNode":
                opNode = self.returnBiggusPyNode("SetNode", value, name)
                opNode.operator = operator
            elif arg1.className == "DictNode":
                opNode = self.returnBiggusPyNode("DictNode", value, name)
                opNode.operator = operator
            elif arg1.className == "VariableNode":
                opNode = self.returnBiggusPyNode("VariableNode", value, name)
                opNode.operator = operator
            else:
                print("WARNING: leftType not found")
                opNode = None
            return opNode
        return opNode

    def checkIfLeftAndRightVariablesExist(self, left, right, opNode, assignmentVariable, name):
        arg1 = self.canvas.getNodeByName(left.id)
        arg2 = self.canvas.getNodeByName(right.id)
        if arg1 is None or arg2 is None:
            print("WARNING: One of the variables does not exist")
            return
        if opNode is None:
            print("OpNode not created")
        elif assignmentVariable is not None:
            self.setOpNodePosition(arg1, arg2, opNode, assignmentVariable)
            self.createConnection(arg1, opNode)
            self.createConnection(arg2, opNode)
            self.createConnection(opNode, assignmentVariable)
        else:
            print("Assignment variable not created")

    def setOpNodePosition(self, arg1, arg2, opNode, assignmentVariable):
        """
        ITA:
            opNode dovrà essere posizionato in base alle variabili che ha,
            se a = 10 e b = 10 a e b vengono posizionati al momento della creazione
            opNode sarà posizionato come:
                x = max(a.getPos().x(), b.getPos().x())* 1.2
                y = (a.getPos().y(), b.getPos().y()) // 2
        ENG:
            opNode must be positioned based on the variables it has,
            if a = 10 and b = 10 a and b are positioned at the time of creation
            opNode will be positioned as:
                x = max(a.getPos().x(), b.getPos().x())* 1.2
                y = (a.getPos().y(), b.getPos().y()) // 2
        :param assignmentVariable: Ex: a = 10 b = 10 c = a + b assignmentVariable = c
        :param opNode: Ex a = 10 b = 10 c = a + b opNode = mathNode
        :param arg2: variableNode 2 Ex: a = 10 b = 10 c = a + b arg2 = b
        :param arg1: variableNode 1 Ex: a = 10 b = 10 c = a + b arg1 = a
        :return:
        """
        x0 = arg1.getPos().x()
        x1 = max(arg1.getWidth(), arg2.getWidth()) * 1.2
        x = (x0 + x1) * 2
        y0 = arg1.getPos().y()
        y1 = arg2.getPos().y()
        y = (y0 + y1) // 2
        self.updateNodePosition(opNode, x, y)
        # position the assignment variable on the side of opNode
        x = opNode.getPos().x() + opNode.getWidth() * 2
        y = opNode.getPos().y()
        self.updateNodePosition(assignmentVariable, x, y)

    # ------------------ IF NODE ------------------

    @staticmethod
    def returnIfOperator(left=None, right=None, operator=None, value=None):
        if isinstance(value, ast.Compare):
            if left is None:
                left = value.left
            if right is None:
                right = value.comparators[0]
            if operator is None:
                operator = value.ops[0]

            if isinstance(operator, ast.Eq):
                return "=="
            elif isinstance(operator, ast.NotEq):
                return "!="
            elif isinstance(operator, ast.Gt):
                return ">"
            elif isinstance(operator, ast.Lt):
                return "<"
            elif isinstance(operator, ast.GtE):
                return ">="
            elif isinstance(operator, ast.LtE):
                return "<="
            elif isinstance(operator, ast.In):
                return "inRange"
        return None

    def createIfNode(self, node):
        operator = self.returnIfOperator(left=node.test.left, right=node.test.comparators[0], value=node.test)
        ifNode = self.returnBiggusPyNode("IfNode", True, "IfNode")
        ifNode.setOperator(operator)
        # scrivendo print(ast.dump(node)) ottengo: If(test=Compare(left=Name(id='b', ctx=Load()), ops=[Gt()],
        # comparators=[Name(id='a', ctx=Load())]), body=[Expr( value=Call(func=Name(id='print', ctx=Load()),
        # args=[Constant(value='b is greater than a')], keywords=[]))], orelse=[])
        leftNode = node.test.left
        arg1 = self.canvas.getNodeByName(leftNode.id)
        arg2 = self.canvas.getNodeByName(node.test.comparators[0].id)

        if arg1 is not None and arg2 is not None:
            self.setIfNodePosition(arg1, arg2, ifNode)
            self.createConnection(arg1, ifNode)
            self.createConnection(arg2, ifNode)

        body = node.body
        # ora devo creare i nodi per il corpo dell'if, per farlo devo creare un nodo per ogni istruzione

        for statement in body:
            if isinstance(statement, ast.Expr):
                if isinstance(statement.value, ast.Call):
                    if statement.value.func.id == "print":
                        # if find a print statement, create a printNode
                        args = statement.value.args
                        if len(args) > 0 and isinstance(args[0], ast.Constant):
                            printNode = self.returnBiggusPyNode("PrintNode", True, "PrintNode")
                            text = args[0].value
                            if text is not None:
                                stringNode = self.returnBiggusPyNode("StringNode", text, "StringNode")
                                self.setIfBodyNodePosition(stringNode)
                                self.setIfOutNodePosition(printNode)
                                self.createConnection(stringNode, ifNode)
                            else:
                                self.setIfBodyNodePosition(printNode)
                            self.createConnection(ifNode, printNode)

    def setIfNodePosition(self, arg1, arg2, ifNode):
        """
        ITA:
            Funziona in modo simile all'opNodePosition, ma setta la posizione di ifNode
            in self.lastIfNode in modo da posizionare i nodi del body dell'if
        ENG:
            Works in a similar way to opNodePosition, but sets the position of ifNode
            in self.lastIfNode in order to position the nodes of the if body
        :param arg1:
        :param arg2:
        :param ifNode:
        :return:
        """
        x0 = arg1.getPos().x()
        x1 = max(arg1.getWidth(), arg2.getWidth()) * 1.2
        x = (x0 + x1) * 2
        y0 = arg1.getPos().y()
        y1 = arg2.getPos().y()
        y = (y0 + y1) // 2
        self.updateNodePosition(ifNode, x, y)
        self.lastIfNode = ifNode

    def setIfBodyNodePosition(self, *args):
        lastNode = self.lastIfNode
        x = lastNode.getPos().x() + lastNode.getWidth() * 2
        y = lastNode.getPos().y() - lastNode.getHeight() * 1.2
        for node in args:
            self.updateNodePosition(node, x, y)
            x += node.getWidth() * 2
            y += lastNode.getPos().y() - node.getHeight()
            lastNode = node

    def setIfOutNodePosition(self, node):
        lastNode = self.lastIfNode
        x = lastNode.getPos().x() + lastNode.getWidth() * 2
        y = lastNode.getPos().y() + lastNode.getHeight() * 1.2
        self.updateNodePosition(node, x, y)

    # ------------------ FUNCTION NODE ------------------

    def createFunctionNode(self, node):
        code = ast.get_source_segment(self.code, node).strip()
        self.code = self.code.replace(code, "")
        # deve saltare l'intestazione def...
        functionNode = self.returnBiggusPyNode("FunctionNode", code, "FunctionNode")
        self.functionNodeList.append(functionNode)
        functionNode.setName(node.name)
        self.lastFunctionNode = functionNode
        self.createNodeFromCode(self.code)

    # ------------------ CALL NODE ------------------

    def createCallNode(self, node):
        # cerca se il nodo è già stato creato
        callNode = self.canvas.getNodeByName(node.func.id)
        if callNode is None:
            print("callNode is None")
        else:
            # trovato il nodo, ora devo creare i nodi per gli argomenti
            args = node.args
            for arg in args:
                if isinstance(arg, ast.Name):
                    argNode = self.canvas.getNodeByName(arg.id)
                    if argNode is not None:
                        self.callNodePosition(argNode, callNode)
                        self.createConnection(argNode, callNode)

    def callNodePosition(self, argNode, callNode):
        x = argNode.getPos().x() + argNode.getWidth() * 2
        y = argNode.getPos().y()
        self.updateNodePosition(callNode, x, y)


    # ------------------ NODE POSITIONING ------------------

    def updateNodePosition(self, node, x, y):
        """
        ITA:
            Aggiorna la posizione del nodo nella scena. Quindi va a cercare il nodo
            nel canvas e aggiorna la sua posizione.
        ENG:
            Update the position of the node in the scene. Then it looks for the node
            in the canvas and updates its position.
        :param x:
        :param y:
        :param node:
        :return:
        """
        if node is not None:
            self.canvas.updateNodePosition(node, x, y)

    def updateNodePositionByLastNode(self, node):
        """
        ITA:
            Aggiorna la posizione del nodo nella scena rispetto a lastNode. Quando viene
            chiamata questa funzione di solito i nodi vengono posizionati sotto a lastNode.
        ENG:
            Update the position of the node in the scene with respect to lastNode. When this
            function is called, the nodes are usually positioned under lastNode.
        :param node:
        :return:
        """
        x = self.lastNode.getPos().x()
        y = self.lastNode.getPos().y() + self.lastNode.getHeight() * 2
        self.updateNodePosition(node, x, y)

    # ------------------ NODE CONNECTION ------------------

    def createConnection(self, node1, node2):
        plugIndex = 0
        for plug in node2.inPlugs:
            if plug.inConnection is None:
                break
            plugIndex += 1
        self.canvas.addConnection(node2, plugIndex, node1, 0)

