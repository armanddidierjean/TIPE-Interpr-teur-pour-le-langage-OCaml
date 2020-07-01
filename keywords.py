from baseclass import *

#####################
#      Keywords     #
#####################

############### System ###############
EOF = 'EOF'
ID = 'ID'
UNIT = 'UNIT'

############### BINOP ###############
PLUS_INT = 'PLUS_INT'
PLUS_FLOAT = 'PLUS_FLOAT'
MINUS_INT = 'MINUS_INT'
MINUS_FLOAT = 'MINUS_FLOAT'
MUL_INT = 'MUL_INT'
MUL_FLOAT = 'MUL_FLOAT'
DIV_INT = 'DIV_INT'
DIV_FLOAT = 'DIV_FLOAT'

############### Micelianous ###############
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
SEMI = 'SEMI'
EQUALS = 'EQUAlS'
REASSIGN = 'REASSIGN'
DOT = 'DOT'
EXCLAMATION = 'EXCLAMATION'
PRINT_INT = 'PRINT_INT'
DIFFERENT = 'DIFFERENT'

############### OCAML keywords ###############
LET = 'LET'
AND = 'AND'
IN = 'IN'
REF = 'REF'
BEGIN = 'BEGIN'
END = 'END'
WHILE = 'WHILE'
DO = 'DO'
DONE = 'DONE'

############### Types ###############
INT = 'INT'
FLOAT = 'FLOAT'

############### RESERVED KEYWORDS ###############
RESERVED_KEYWORDS = {
    'let': Token(LET, None),
    'and': Token(AND, None),
    'in': Token(IN, None),
    'ref': Token(REF, None),
    'begin': Token(BEGIN, None),
    'end': Token(END, None),
    'while': Token(WHILE, None),
    'do': Token(DO, None),
    'done': Token(DONE, None),
    'print_int': Token(PRINT_INT, None),
    #'print_string': Token(PRINT_STRING, None),
}