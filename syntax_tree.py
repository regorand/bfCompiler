from enum import Enum

class AST_Node:
    child_nodes = []
    type = None
    value = None

    def __init__(self, type):
        self.type = type
        self.child_nodes = []

    def addChild(self, child):
        self.child_nodes = self.child_nodes + [child]

    def setValue(self, value):
        self.value = value

    def printTree(self, level):
        s = level * '\t' + self.type.name
        if self.value is not None:
            s += '({})'.format(self.value)
        print(s)

        for child in self.child_nodes:
            child.printTree(level + 1)


NodeType = Enum('NodeType', [
'STATEMENT_LIST',
'SET', 
'CALL', 
'IF', 
'WHILE', 
'IDENT', 
'CONST',
'EQ',
'LT',
'LTE',
'GT',
'GTE',
'NEW_VAR',
'ADD',
'SUB',
'MUL',
'DIV',
'MOD'
])