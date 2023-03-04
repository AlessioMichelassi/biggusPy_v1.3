import ast

from elements.Nodes.PythonNodes.NumberNode import NumberNode

code = '''def SieveOfEratosthenes(n):
    prime_list = []
    for i in range(2, n+1):
        if i not in prime_list:
            print (i)
            for j in range(i*i, n+1, i):
                prime_list.append(j)'''


class CodeToNode:
    nodes = []
    positions = []

    def __init__(self, canvas):
        self.canvas = canvas

    def createNodeFromCode(self, _code: str):
        self.nodes = []
        parsedCode = self.parseCode(_code)
        self.nodeSearch(parsedCode)

    @staticmethod
    def parseCode(_code: str):
        # parse the code into an AST
        return ast.parse(_code)

    def searchFunction(self, parsed_code: ast.AST):
        pass

    def nodeSearch(self, parsedCode: ast.AST):
        prev_node = None
        for node in ast.walk(parsedCode):
            if isinstance(node, ast.FunctionDef):
                print(node.name)
            elif isinstance(node, ast.For):
                print("For")
            elif isinstance(node, ast.If):
                self.createIfNode(node)
            elif isinstance(node, ast.Call):
                try:
                    if isinstance(node.func, ast.Name):
                        print(node.func.id)
                    elif isinstance(node.func, ast.Attribute):
                        print(node.func.attr)
                except Exception as e:
                    print("*" * 20)
                    print(e)
                    print("*" * 20)
            elif isinstance(node, ast.Assign):
                # create a node for each variable
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        prev_node = self.createVariableNode(target.id, node.value, prev_node)

    def createVariableNode(self, name: str, value, prev_node=None, y_offset=0):
        """
        ITA:
            Crea un nodo per la variabile in base al tipo di valore assegnato
            target.id è il nome della variabile, mentre node.value è il valore assegnato
            in target si trova questi dati:
            ast.Assign(targets=[ast.Name(id='a', ctx=ast.Store())],
        ENG:
            Create a node for the variable based on the type of value assigned
        :param name: is the name of the variable and is from the ast.Name
        :param value: came from the ast.Assign
        :param prev_node:
        :param y_offset:
        :return:
        """
        # Se la variabile esiste già, cerca il nodo associato alla variabile
        node = self.canvas.getNodeByName(name)
        if isinstance(value, ast.Num):
            node = self.canvas.createNodeFromCodeToNode("NumberNode", value.n)
            self.setName(node, name)
        elif isinstance(value, ast.Name):
            node = self.canvas.createNodeFromCodeToNode("VariableNode", value.id)
            self.setName(node, name)
        elif isinstance(value, ast.List):
            node = self.getElements(value, "ListNode", name)
        elif isinstance(value, ast.Tuple):
            node = self.getElements(value, "TupleNode", name)
        elif isinstance(value, ast.Dict):
            self.createDictNode(name, value)
        elif isinstance(value, ast.Set):
            elements = [el.n if isinstance(el, ast.Num) else el.value for el in value.elts]
            node = self.canvas.createNodeFromCodeToNode("SetNode", elements)
            self.setName(node, name)
        elif isinstance(value, ast.Str):
            node = self.canvas.createNodeFromCodeToNode("StringNode", value.s)
            self.setName(node, name)
        elif isinstance(value, ast.Bytes):
            node = self.canvas.createNodeFromCodeToNode("VariableNode", value.s)
            self.setName(node, name)
        elif isinstance(value, ast.BinOp):
            self.checkBinOpNode(name, value)
        if node:
            x = 0
        if prev_node:
            prev_node_pos = prev_node.getPos()
            y = prev_node_pos.y() + prev_node.getHeight() * 1.2 + y_offset
            self.updateNodePosition(node, prev_node_pos.x(), y)
        else:
            y = 0
        return node


    @staticmethod
    def setName(node, name):
        if node:
            node.setName(name)
        else:
            print("Node was not created")

    def getElements(self, value, arg1, name):
        elements = [el.value for el in value.elts]
        result = self.canvas.createNodeFromCodeToNode(arg1, elements)
        self.setName(result, name)
        return result


    def createNodeOnCanvas(self, node):
        self.canvas.addNode(node)

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

    def createConnection(self, node1, node2):
        plugIndex = 0
        for plug in node2.inPlugs:
            if plug.inConnection is None:
                break
            plugIndex += 1
        self.canvas.addConnection(node2, plugIndex, node1, 0)

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
    def checkBinOpNode(self, name, value):
        # controllo se il nodo è già stato creato
        # check if the node has already been created
        node = self.canvas.getNodeByName(name)
        if node is None:
            node = self.createVariableNode(name, value.right)
            self.createNodeOnCanvas(node)
        # controlla che l'argomento della sinistra già esista
        # check that the left argument already exists
        arg1 = self.canvas.getNodeByName(value.left.id)
        if arg1 is None:
            arg1 = self.createVariableNode(value.left.id, value.left)
            self.createNodeOnCanvas(arg1)
        arg2 = self.canvas.getNodeByName(value.right.id)
        if arg2 is None:
            arg2 = self.createVariableNode(value.right.id, value.right)
            self.createNodeOnCanvas(arg2)

        mathNode = self.createMathNode(name, value)
        self.createNodeOnCanvas(mathNode)
        self.setMathNodePosition(mathNode, arg1, arg2)
        self.setVarNodePositionAfterMathNode(node, mathNode)
        self.createConnection(arg1, mathNode)
        self.createConnection(arg2, mathNode)
        self.createConnection(mathNode, node)

    def createMathNode(self, name, value):
        """
        ITA:
            Crea un MathNode e setta l'operatore come +, -, *, / etc ...
        ENG:
            Create a MathNode and set the operator as +, -, *, / etc ...
        :param name:
        :param value:
        :return:
        """
        node = None
        if isinstance(value, ast.BinOp) and isinstance(value.op, ast.Add):
            if isinstance(value.op, ast.Add):
                if name in self.canvas.nodesTitleList:
                    node = self.canvas.getNodeByTitle(name)
                else:
                    node = self.returnMathNode(name, "+")
            elif isinstance(value.op, ast.Sub):
                if name in self.canvas.nodesTitleList:
                    node = self.canvas.getNodeByTitle(name)
                else:
                    node = self.returnMathNode(name, "-")
            elif isinstance(value.op, ast.Mult):
                if name in self.canvas.nodesTitleList:
                    node = self.canvas.getNodeByTitle(name)
                else:
                    node = self.returnMathNode(name, "*")
            elif isinstance(value.op, ast.Div):
                if name in self.canvas.nodesTitleList:
                    node = self.canvas.getNodeByTitle(name)
                else:
                    node = self.returnMathNode(name, "/")
            elif isinstance(value.op, ast.FloorDiv):
                if name in self.canvas.nodesTitleList:
                    node = self.canvas.getNodeByTitle(name)
                else:
                    node = self.returnMathNode(name, "//")
            elif isinstance(value.op, ast.Mod):
                if name in self.canvas.nodesTitleList:
                    node = self.canvas.getNodeByTitle(name)
                else:
                    node = self.returnMathNode(name, "%")
            elif isinstance(value.op, ast.Pow):
                if name in self.canvas.nodesTitleList:
                    node = self.canvas.getNodeByTitle(name)
                else:
                    node = self.returnMathNode(name, "**")
        return node

    def returnMathNode(self, name, operatorType):
        """
        ITA:
            crea un mathNode e lo setta con l'operatore passato come argomento
        ENG:
            create a mathNode and set it with the operator passed as an argument
        :param name:
        :param operatorType:
        :return:
        """
        node = self.canvas.createNode("MathNode")
        node.setName(name)
        node.setOperator(operatorType)
        return node

    def setMathNodePosition(self, node, arg1, arg2):
        """
        MathNode dovrà essere posizionato in base agli argomenti che ha
        ad esempio:
            x = max(a.getPos().x(), b.getPos().x())* 1.2
            y = (a.getPos().y(), b.getPos().y()) // 2

        :param arg2: variableNode 2
        :param arg1: variableNode 1
        :param node: mathNode
        :return:
        """
        x0 = arg1.getPos().x()
        x1 = max(arg1.getWidth(), arg2.getWidth()) * 1.2
        x = (x0 + x1) * 2
        y0 = arg1.getPos().y()
        y1 = arg2.getPos().y()
        y = (y0 + y1) // 2
        self.updateNodePosition(node, x, y)

    def setVarNodePositionAfterMathNode(self, node, mathNode):
        x = mathNode.getPos().x() + mathNode.getWidth() * 2
        y = mathNode.getPos().y()
        self.updateNodePosition(node, x, y)

    # ---------------    DICTIONARY NODE    ----------------
    def createDictNode(self, name: str, value):
        keys = [el.s for el in value.keys]
        values = [el.n if isinstance(el, ast.Num) else (el.s if isinstance(el, ast.Str) else el.id) for el in
                  value.values]
        dictionary = dict(zip(keys, values))
        node = self.canvas.createNodeFromCodeToNode("DictionaryNode", dictionary)
        self.setName(node, name)

    # ---------------    IF NODE    ----------------

    def createIfNode(self, node: ast.If):
        if_node = self.canvas.createNodeFromCodeToNode("IfNode", node.test)
        self.setName(if_node, "if")

    def createIfNode(self, node: ast.If):
        if_node = self.canvas.createNodeFromCodeToNode("IfNode", node.test)
        self.setName(if_node, "if")
        self.setIfNodePosition(if_node, node)
        self.createIfNodeBody(if_node, node)
        self.createIfNodeOrelse(if_node, node)
        return if_node

    def setIfNodePosition(self, if_node, node):
        x = node.getPos().x() + node.getWidth() * 2
        y = node.getPos().y()
        self.updateNodePosition(if_node, x, y)

    # ---------------    FOR NODE    ----------------

    # ################################################################
    #
    #                OPERATORS
    #

    """
    ITA:
        La maggior parte dei nodi hanno un menu interno che li rende dinamici,
        questa cosa è stata pensata per ridurre il numero di nodi da creare.
        ad esempio MathNode può essere una qualunque operazione matematica
        quindi quanto si crea il nodo si deve scegliere l'operatore.
        Allo stesso modo le liste, le stringhe, le tuple, i dizionario, i set
        hanno un menu interno che le può trasformare in una qualsiasi delle operazioni che
        possono essere fatte su di esse.
        StringNode... può essere un concat, split, replace, etc...
    ENG:
        Most of the nodes have an internal menu that makes them dynamic,
        this was thought to reduce the number of nodes to create.
        for example MathNode can be any mathematical operation
        so when you create the node you must choose the operator.
        In the same way lists, strings, tuples, dictionaries, sets
        have an internal menu that can transform them into any of the operations that
        can be done on them.
        StringNode ... can be a concat, split, replace, etc ...
    """

    @staticmethod
    def getMathOperator(op: ast.AST):
        if isinstance(op, ast.Add):
            return "+"
        elif isinstance(op, ast.Sub):
            return "-"
        elif isinstance(op, ast.Mult):
            return "*"
        elif isinstance(op, ast.Div):
            return "/"
        elif isinstance(op, ast.Mod):
            return "%"
        elif isinstance(op, ast.Pow):
            return "**"
        elif isinstance(op, ast.LShift):
            return "<<"
        elif isinstance(op, ast.RShift):
            return ">>"
        elif isinstance(op, ast.BitOr):
            return "|"
        elif isinstance(op, ast.BitXor):
            return "^"
        elif isinstance(op, ast.BitAnd):
            return "&"
        elif isinstance(op, ast.FloorDiv):
            return "//"

    @staticmethod
    def getStringOperator(op: ast.AST):
        if isinstance(op, ast.Add):
            return "concat"
        elif isinstance(op, ast.Mult):
            return "repeat"
        elif isinstance(op, ast.Mod):
            return "format"
        elif isinstance(op, ast.BitOr):
            return "replace"
        elif isinstance(op, ast.BitXor):
            return "split"
        elif isinstance(op, ast.BitAnd):
            return "join"
        elif isinstance(op, ast.FloorDiv):
            return "find"

    @staticmethod
    def getCollectionOperator(op: ast.AST):
        if isinstance(op, ast.Add):
            return "add"
        elif isinstance(op, ast.Sub):
            return "remove"
        elif isinstance(op, ast.Mult):
            return "repeat"
        elif isinstance(op, ast.BitOr):
            return "replace"
        elif isinstance(op, ast.BitXor):
            return "split"
        elif isinstance(op, ast.BitAnd):
            return "join"
        elif isinstance(op, ast.FloorDiv):
            return "find"

    @staticmethod
    def getBoolOperator(op: ast.AST):
        if isinstance(op, ast.And):
            return "and"
        elif isinstance(op, ast.Or):
            return "or"
        elif isinstance(op, ast.Not):
            return "not"
        elif isinstance(op, ast.Invert):
            return "invert"
        elif isinstance(op, ast.UAdd):
            return "uadd"
        elif isinstance(op, ast.USub):
            return "usub"
        elif isinstance(op, ast.Eq):
            return "=="
        elif isinstance(op, ast.NotEq):
            return "!="
        elif isinstance(op, ast.Gt):
            return ">"
        elif isinstance(op, ast.GtE):
            return ">="
        elif isinstance(op, ast.Lt):
            return "<"
        elif isinstance(op, ast.LtE):
            return "<="
        elif isinstance(op, ast.Is):
            return "is"
        elif isinstance(op, ast.IsNot):
            return "is not"
        elif isinstance(op, ast.In):
            return "in"
        elif isinstance(op, ast.NotIn):
            return "not in"

    @staticmethod
    def getIfOperator(op: ast.AST):
        if isinstance(op, ast.Eq):
            return "=="
        elif isinstance(op, ast.NotEq):
            return "!="
        elif isinstance(op, ast.Gt):
            return ">"
        elif isinstance(op, ast.GtE):
            return ">="
        elif isinstance(op, ast.Lt):
            return "<"
        elif isinstance(op, ast.LtE):
            return "<="
        elif isinstance(op, ast.Is):
            return "is"
        elif isinstance(op, ast.IsNot):
            return "is not"
        elif isinstance(op, ast.In):
            return "in"
        elif isinstance(op, ast.NotIn):
            return "not in"
