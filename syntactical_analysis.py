from syntax_tree import *
from Tokens import Token
from parser import parse

def main():
    raw = "var x = (5 * 7);\n"#var y = x * 5;\nx = 17;\nif (x == 5) {\nprint(y);\n}\nprint(x);"
    res = parse(raw)
    tokens = res[0]
    print(tokens)
    #tokens = [(Token.VAR, 0), (Token.IDENT, 2), (Token.SETEQ, 0), (Token.NUM, 5), (Token.SEMICOLON, 0)]
    tree = doAnalysis(tokens)
    tree.printTree(0)

def doAnalysis(tokens):
    stream = tokenStream(tokens)
    #print(stream.current)

    tree = parseStart(stream)

    return tree


def parseStart(stream):
    return parse_S_list(stream)
    
    

def parse_S_list(stream):
    root = AST_Node(NodeType.STATEMENT_LIST)
    t = stream.current
    while (True):
        match stream.current[0]:
            case Token.LB | Token.VAR | Token.IDENT | Token.IF | Token.WHILE | Token.PRINT:
                root.addChild(parseS(stream))
            case Token.END | Token.RB:
                break
            case x:
                error("Unexpected Token parsing S_List: {}", x.name)
        stream.next()
    return root


def parseS(stream):
    match stream.current[0]:
        case Token.LB:
            return parseB(stream)
        case Token.VAR:
            node = AST_Node(NodeType.NEW_VAR)
            ident_node = AST_Node(NodeType.IDENT)
            ident_node.setValue(stream.current[1])
            node.addChild(ident_node)
            stream.next()
            stream.next()

            expr_node = parseE(stream)
            
            # TODO need stream.next() here ?
            expect(stream.current, Token.SEMICOLON)

            node.addChild(expr_node)

            return node
        case Token.IDENT:
            return AST_Node(NodeType.IDENT)
        case Token.IF:
            return AST_Node(NodeType.IF)
        case Token.WHILE:
            return AST_Node(NodeType.WHILE)
        case Token.PRINT:
            return AST_Node(NodeType.CALL)
        case Token.END:
            return
        case x:
            error("Unexpected Token parsing S: {}", x.name)


def parseB(stream):
    node = AST_Node(NodeType.STATEMENT_LIST)
    stream.next()
    content = parse_S_list(stream)
    stream.next()
    expect(stream.current, Token.RB)
    node.addChild(content)

def parseE(stream):

    left_term = parseT(stream)

    stream.next()

    others = parseEList(stream)

    if others is None:
        return left_term
    parent = others[0]
    right = others[1]
    parent.addChild(left_term)
    parent.addChild(right)
    return parent

def parseEList(stream):
    match stream.current[0]:
        case Token.ADD | TOKEN.SUB:
            parent = parseArithLine(stream)
            stream.next()
            left_node = parseT()
            stream.next()

            others = parseEList(stream)
            if others is None:
                error("Expression ended unexpectedly")
            if others[1] is None:
                return (parent, rest_expr_node[0])
            
            sub_parent = others[0]
            right = others[1]
            sub_parent.addChild(left_node)
            sub_parent.addChild(right)
            return (parent, sub_parent)
            

        case Token.RP | Token.SEMICOLON:
            return None



def parseT(stream):
    parseF(stream)
    parseTList(stream)

def parseTList(stream):


def parseF(stream):
    match stream.current[0]:
        case Token.IDENT:
            node = AST_Node(NodeType.IDENT)
            node.setValue(stream.current[1])
        case Token.NUM:
            node = AST_Node(NodeType.CONST)
            node.setValue(stream.current[1])
        case Token.READ:
            node = AST_Node(NodeType.CALL)
            node.setValue('READ')
        case Token.LP:
            stream.next()
            node = parseE(stream)
            stream.next()
            expect(stream.current, Token.RP)
        case x:
            error("Unexpected Token parsing F: {}", x.name)

    stream.next()
    return node


def parseArithLine(stream):
    match stream.current[0]:
        case Token.ADD:
            return AST_Node(NodeType.ADD)
        case Token.SUB:
            return AST_Node(NodeType.SUB)
        case x:
            error("Unexpected Token parsing ArithLine: {}", x.name)
        

class tokenStream():
    current = (Token.END, 0)
    _ite = None

    def __init__(self, tokens):
        self._ite = iter(tokens)
        self.current = next(self._ite, (Token.END, 0))

    def next(self):
        self.current = next(self._ite, (Token.END, 0))
        return self.current






def expect(actual, expected):
    if actual[0] != expected:
        error("Expected Token {}, instead found Token {}".format(expected, actual))

        
def error(msg, *chars):
    print("Syntactical Analysis Error: {}".format(msg.format(chars)))
    quit()

if __name__ == '__main__':
    main()