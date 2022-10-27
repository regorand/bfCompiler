from enum import Enum

Token = Enum('Token', [
    'VAR', 
    'ADD',
    'EQ',
    'NUM',
    'SETEQ',
    'READ',
    'PRINT',
    'LP',
    'RP',
    'LB',
    'RB',
    'IF',
    'WHILE',
    'SEMICOLON',
    'IDENT',
    'SUB',
    'MUL',
    'DIV',
    'MOD',
    'LT',
    'LTE',
    'GT',
    'GTE',
    'END'])
#
#class Token(Enum):
#    VAR = 1
#    ADD = 2
#    EQ = 3
#    NUM = 4
#    SETEQ = 5
#    READ = 6
#    PRINT = 7
#    LP = 8
#    RP = 9
#    LB = 10
#    RB = 11
#    IF = 12
#    WHILE = 13
#    SEMICOLON = 14
#    IDENT = 15
#    SUB = 16
#    MUL = 17
#    DIV = 18
#    MOD = 19
#    LT = 20
#    LTE = 21
#    GT = 22
#    GTE = 23