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
MOD = 'MOD'

BOOLEANCONJUNCTION = 'BOOLEANCONJUNCTION'
BOOLEANDISJUNCTION = 'BOOLEANDISJUNCTION'

############### Functions ###############
PRINT_INT = 'PRINT_INT'
PRINT_STRING = 'PRINT_STRING'

############### Micelianous ###############
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
SEMI = 'SEMI'
EQUALS = 'EQUAlS'
DIFFERENT = 'DIFFERENT'
REASSIGN = 'REASSIGN'
DOT = 'DOT'
EXCLAMATION = 'EXCLAMATION'
ARROW = 'ARROW'

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
FUNCTION = 'FUNCTION'
IF = 'IF'
THEN = 'THEN'
ELSE = 'ELSE'
REC = 'REC'

############### Types ###############
INT = 'INT'
FLOAT = 'FLOAT'
BOOL = 'BOOL'
STRING = 'STRING'

############### RESERVED KEYWORDS ###############
RESERVED_KEYWORDS = {
    'let': LET,
    'and': AND,
    'in': IN,
    'ref': REF,
    'begin': BEGIN,
    'end': END,
    'while': WHILE,
    'do': DO,
    'done': DONE,
    'mod': MOD,
    'print_int': PRINT_INT,
    'print_string': PRINT_STRING,
    'function': FUNCTION,
    'fun': FUNCTION,
    'if': IF,
    'then': THEN,
    'else': ELSE,
    'rec': REC
}

BUILTIN_TYPES = [
    SymbolType("int"),
    SymbolType("float"),
    SymbolType("string"),
]