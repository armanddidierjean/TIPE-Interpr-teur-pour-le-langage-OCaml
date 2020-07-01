#####################
#     AST  Nodes    #
#####################
class AST:
    pass

class Program(AST):
    """
    Program node

    Attributes
    ----------
    statement : AST node
        Program begining node
    """
    def __init__(self, block_node):
        self.block_node = block_node

class Block(AST):
    """
    Block node

    Attributes
    ----------
    node : AST node
        code component (command or sequence)
    """
    def __init__(self, node):
        self.node = node

class Sequence(AST):
    """
    Sequence node
    Represent a sequence

    Attributes
    ----------
    commands_list : [AST]
        List of the commands contained in the sequence
    """
    def __init__(self, commands_list):
        self.commands_list = commands_list

class Num(AST):
    """
    Num node
    Represent a predefined type number

    TODO: accept strings

    Attributes
    ----------
    value : VALUE (string, int...)
        Value of the represented data
    type : PREDEFINED TYPE
        Type of the represented data
    """
    def __init__(self, value, type):
        self.value = value
        self.type = type

class BinOp(AST):
    """
    BinOp node
    Represent a binary operation: + - * /...

    Attributes
    ----------
    left_node : AST node
        Left node
    op_token : Token
        Operator toke,
    right_node : AST Node
        Right Node
    """
    def __init__(self, left_node, op_token, right_node):
        self.left_node = left_node
        self.op_token = op_token
        self.right_node = right_node

class UnaryOp(AST):
    """
    UnaryOp node
    Represent a unary operation: + -

    Attributes
    ----------
    op_token : Token
        Operator token
    right_node : AST Node
        Right Node
    """
    def __init__(self, op_token, right_node):
        self.op_token = op_token
        self.right_node = right_node

class AssignementStatement(AST):
    """
    AssignementStatement node
    Represent a let statement

    Attributes
    ----------
    assignements_list : [AST node]
        List countaining assignement nodes
    block_node : AST node
        Node countaining the block to execute. Can be None
    """
    def __init__(self, assignements_list, block_node):
        self.assignements_list = assignements_list
        self.block_node = block_node

class Assignement(AST):
    """
    Assignement node
    Represent an assignement

    Attributes
    ----------
    var_name : string
        Name of the defined variable
    is_ref : boolean
        If the assignement is a mutable assignement
    value_node : AST node
        Expression assigned to the variable
    """
    def __init__(self, var_name, is_ref, value_node):
        self.var_name = var_name
        self.is_ref = is_ref
        self.value_node = value_node

class Reassignement(AST):
    """
    Reassignement node

    Attributes
    ----------
    var_name : string
        Name of the modified variable
    new_value_node : AST node
        Expression assigned to the variable
    """
    def __init__(self, var_name, new_value_node):
        self.var_name = var_name
        self.new_value_node = new_value_node

class Variable(AST):
    """
    Variable node

    Attributes
    ----------
    var_name : string
        Name of the accessed variable
    get_content : bool
        Get the content of a ref variable
    """
    def __init__(self, var_name, get_content):
        self.var_name = var_name
        self.get_content = get_content
        #TODO: creer un AST node pour le point d'esclamation

class PrintInt(AST):
    def __init__(self, node):
        self.node = node

class Boucle(AST):
    def __init__(self, boolean_node, block_node):
        self.boolean_node = boolean_node
        self.block_node = block_node

class UnitNode(AST):
    pass