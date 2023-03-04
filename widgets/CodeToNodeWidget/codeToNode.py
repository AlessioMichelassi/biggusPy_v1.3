import ast

code = '''def SieveOfEratosthenes(n):
    prime_list = []
    for i in range(2, n+1):
        if i not in prime_list:
            print (i)
            for j in range(i*i, n+1, i):
                prime_list.append(j)'''


class CodeToNode:
    nodes = []

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
        for node in ast.walk(parsedCode):
            if isinstance(node, ast.FunctionDef):
                print(node.name)
            elif isinstance(node, ast.For):
                print("For")
            elif isinstance(node, ast.If):
                print("If")
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
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        self.createVariableNode(target.id, node.value)

    def createVariableNode(self, name: str, value):
        node = None
        if isinstance(value, ast.Num):
            node = self.canvas.createNode("NumberNode", value.n)
            node.setName(name)
        elif isinstance(value, ast.Name):
            node = self.canvas.createNode("VariableNode", value.id)
            node.setName(name)
        elif isinstance(value, ast.List):
            elements = [el.n if isinstance(el, ast.Num) else el.id for el in value.elts]
            node = self.canvas.createNode("ListNode", elements)
            node.setName(name)
        elif isinstance(value, ast.Tuple):
            node = self.canvas.createNode("Tuple", value.elts)
            node.setName(name)
        elif isinstance(value, ast.Dict):
            node = self.canvas.createNode("DictionaryNode", value.keys, value.values)
            node.setName(name)
        elif isinstance(value, ast.Set):
            node = self.canvas.createNode("Set", value.elts)
            node.setName(name)
        elif isinstance(value, ast.Str):
            node = self.canvas.createNode("StringNode", value.s)
            node.setName(name)
        elif isinstance(value, ast.Bytes):
            node = self.canvas.createNode("VariableNode", value.s)
            node.setName(name)

        if node:
            print(f"Created {node} with value {value}")
            self.nodes.append(node)