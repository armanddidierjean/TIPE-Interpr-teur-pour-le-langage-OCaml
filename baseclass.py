#####################
#     Data  Type    #
#####################

class Token:
    """
    Token

    Represent a base element of a program ('1', '+', 'print_int'...)

    Attributes
    ----------
    type : keyword
        Type of the token
    value : VALUE (string, int...)
        Value of the token (value, None or keyword)
    """
    def __init__(self, type, value):
        self.type = type
        self.value = value
    
    def __str__(self):
        """
        Token(INTEGER, 3)
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

#####################
#   Nodes visitor   #
#####################
class NodeVisitor(object):
    """
    Base class used to construct an interpreter

    Methods
    -------
    visit(node)
        Call the visitType(node) methode corresponding to the node type
    """
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')

#####################
#      Memory       #
#####################
class Symbol(object):
    """
    Represent a symbol, for the moment only a variable 

    Attributes
    ----------
    id : string
        Non duplicated id used to find the symbol
    isref : bool
        Is the symbol mutable
    value : VALUE (string, int...)
        Value of the symbol
    type : PREDEFINED TYPE
        Type of symbol
    """
    def __init__(self, id, isref, value, type):
        self.id = id
        self.isref = isref
        self.value = value
        self.type = type

class MemoryTable(object):
    """
    Class that manage a basic memory system. Is based on a Python dictionnary

    WARNING: This class is a usable WIP
    TODO: Improve the class

    Methods
    -------
    define(id, isref, type=None, value=None)
        define a new symbol in the memory
        check if the id is already used
    isdefined(id)
        return True if id is in the memory
    isref(id)
        return True if the symbol id is mutable
        WARNING: do not check if id is defined
    change_value(id, value)
        Change the value of the id symbol
        WARNING: do not check if id is defined or mutable
    get_value(id)
        return the value of the symbol id
        WARNING: do not check if id is defined
    get_type(id)
        return the type of the symbol id
        WARNING: do not check if id is defined

    TODO: remove or modify:
    get_symbol(id, getref=False)
    """
    def __init__(self):
        self.memoryTable = {}
    
    def define(self, id, isref, type=None, value=None):
        """
        Define a new symbol
        """
        if self.isdefined(id):
            raise NameError(f"{id} is already defined")
        
        self.memoryTable[id] = Symbol(id, isref, value, type)
    
    def isdefined(self, id):
        return id in self.memoryTable
    
    def isref(self, id):
        return self.memoryTable[id].isref
    
    def change_value(self, id, value):
        self.memoryTable[id].value = value
    
    def get_value(self, id):
        return self.memoryTable[id].value

    def get_type(self, id):
        return self.memoryTable[id].type
    """
    def reassign(self, id, type=None, value=None):
        if not id in self.memoryTable:
            raise NameError(f"{id} is not defined")
        if not self.memoryTable[id].isref:
            raise TypeError("{id} is not mutable")
        MemoryTable[id].type = type
        MemoryTable[id].value = value
    """
    def get_symbol(self, id, getref=False):
        if not self.isdefined(id):
            raise NameError(f"{id} is not defined")

        return self.memoryTable[id]



    

