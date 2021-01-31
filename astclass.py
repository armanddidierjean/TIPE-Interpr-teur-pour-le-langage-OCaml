#####################
#     AST  Nodes    #
#####################
"""
File containing all class used to create the tree representing the program
"""

class AST:
    pass

class Program(AST):
    """
    Program node

    Attributes
    ----------
    block_node : AST node
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
    commands_list : [AST node]
        List of the commands contained in the sequence
    """
    def __init__(self, commands_list):
        self.commands_list = commands_list

class Num(AST):
    """
    Num node
    Represent a predefined type value

    TODO:accept strings and bool
    
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
    Represent a binary operation: + - * mod = &&

    Attributes
    ----------
    left_node : AST node
        Left node
    op_token : Token
        Operator token
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

class AssignmentStatement(AST):
    """
    AssignmentStatement node
    Represent a let statement

    Attributes
    ----------
    assignments_list : [AST node]
        List countaining assignment nodes
    block_node : AST node
        Node countaining the block to execute. Can be a UnitNode.
    """
    def __init__(self, assignments_list, block_node):
        self.assignments_list = assignments_list
        self.block_node = block_node

class AssignmentVariable(AST):
    """
    Represent a variable assignment

    Attributes
    ----------
    var_name : string
        Name of the defined variable
    is_ref : boolean
        If the assignment is a mutable assignment
    value_node : AST node
        Expression assigned to the variable
    """
    def __init__(self, var_name, is_ref, value_node):
        self.var_name = var_name
        self.is_ref = is_ref
        self.value_node = value_node

class AssignmentFunction(AST):
    """
    Represent a function assignment

    Attributes
    ----------
    var_name : string
        Name of the defined variable
    content_node : AST node
        Content of a function, can be an other function or a block

        TODO: rename the attributes
    """
    def __init__(self, var_name, content_node):
        self.var_name = var_name
        self.content_node = content_node

class Reassignment(AST):
    """
    Reassignment node

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
        #TODO: créer un AST node pour le point d'exclamation

class FunctionCall(AST):
    """
    FunctionCall node
    It does not represent the function but its result. To access a function symbol, use a variable class.
    
    Attributes
    ----------
    var_name : string
        Name of the called function
    parameters_nodes_list : [AST]
        List countaining AST nodes of actual parameters or arguments
    """
    def __init__(self, var_name, arguments_nodes_list):
        self.var_name = var_name
        self.arguments_nodes_list = arguments_nodes_list

class PrintInt(AST):
    """
    PrintInt node

    TODO: create a global Print node with a type arg

    Attributes
    ----------
    node : AST node
        Value to be printed
    """
    def __init__(self, node):
        self.node = node

class PrintString(AST):
    """
    PrintInt node

    TODO: create a global Print node with a type arg

    Attributes
    ----------
    node : AST node
        Value to be printed
    """
    def __init__(self, node):
        self.node = node

class Loop(AST):
    """
    Loop node

    Attributes
    ----------
    boolean_node : AST node of type BOOL
        Node of the condition of the loop
    block_node : AST node
        Executed code
    """
    def __init__(self, boolean_node, block_node):
        self.boolean_node = boolean_node
        self.block_node = block_node

class UnitNode(AST):
    """
    UnitNode node
    Allow to have non executed node (usually return None of type UNIT)
    """
    pass

class NothingClass(AST):
    """
    Used to detect empty blocks
    Tool class: It does not represent OCaml code but is used by the interpreter to detect empty block
    """
    pass

class Function(AST):
    """
    Node used to store a function declaration

    Attributes
    ----------
    parameter_id : string or None
        Name of the parameter
        Can be none if the parameter is unit
    content_node : AST node
        Body of the function, can be an other function or a block node
    TODO: change

    WARNING THERE IS NO VISIT FUNCTION METHOD ???
    """
    def __init__(self, parameters_list, parameters_types_list, function_body_node):
        self.parameters_list = parameters_list
        self.parameters_types_list = parameters_types_list
        self.function_body_node = function_body_node
    """
    def __init__(self, parameter_id, content_node):
        self.parameter_id = parameter_id
        self.content_node = content_node
    """