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
    Memory system, allow to store symbol, support nested scopes

    Attributes
    ----------
    scope_name : string
    scope_level : int
    following_table : MemoryTable object
        A memory table where symbole are already defined and where the table should look for unavailable requested symbols
    
    Methods
    -------
    define(id, symbol)
        Define a symbol in the memory
    get(id)
        Return the symbol id defined in the table or in the following
        Return None if id is not defined
    isdefined(id, look_following_table=True)
        Return if id is defined
    """
    def __init__(self, scope_name, scope_level, following_table):
        self.scope_name = scope_name
        self.scope_level = scope_level
        self.following_table = following_table

        self._memory = {}
    
    def define(self, id, symbol):
        """
        Define a new symbol
        """
        self._memory[id] = symbol
    
    def get(self, id):
        """
        Return the symbol id
        """
        symbol = self._memory.get(id)  # symbol is None if it is not in self._memory

        if symbol is not None:
            # If the symbol is define in this table, return it
            return symbol
        else:
            if self.following_table is not None:
                # If the symbol is not defined in this table, it should be in the following_table
                return self.following_table.get(id)
            # There is no following table
            return None
        
    def isdefined(self, id, look_following_table=True):
        """
        Return is the symbol id is already defined

        Attributes
        ----------
        id : string
            Id of the searched symbol
        look_following_table : bool
            If the function should search id in the following tables
        """
        symbol = self._memory.get(id)  # symbol is None if it is not in self._memory

        if symbol is not None:
            # If the symbol is define in this table, return True
            return True
        else:
            # If the symbol is not defined in this table, it should be in the following_table
            if look_following_table and self.following_table is not None:
                return self.following_table.isdefined(id, look_following_table=True)
            else:
                return False
