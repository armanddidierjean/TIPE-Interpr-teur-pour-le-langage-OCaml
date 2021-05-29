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
    position : int
        Position of the begining of the associated code, used for error reporting
    length : int
        Length of the associated code, used for error reporting
    """
    def __init__(self, type, value, position, length):
        self.type = type
        self.value = value

        # We use the position and the token length for errors reporting
        self.position = position
        self.length = length
    
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
    symbol_type = "Symbol" #TODO: remove
    def __init__(self, id, isref, value, type):
        self.symbol_type = "Symbol"
        self.id = id
        #self.isref = isref
        #self.value = value
        #self.type = type

class SymbolType(Symbol):
    """
    Represent a type
    - builtin type
    - composites type (int -> string) TODO :Really?
    """
    def __init__(self, id):
        self.symbol_type = "Type"
        self.id = id
        #self.type = type
        #TODO: remove type
    
    def __str__(self):
        return f"<{self.id}>"
    
    def __repr__(self):
        return self.__str__()


class SymbolQuoteType(Symbol):
    """
    Represent a quote type ('a, 'b)
    This class allow to use placeolder type 'a. They can or not be resolved ('a = int or 'a = None)
    
    TODO: Document
    A comparison is managed by this class
     - is equals
     - resolve the unresolved quote type
    TODO: Assumption: when a comparison is done we can fix the type

    Attributes
    ----------
    id : string
    resolved_type : SymbolType object
        When we know what type should be a 'a object, we attribute it to resolved_type
        This allow to do type determination for procedure parameters
    """
    def __init__(self, id, resolved_type=None):
        self.symbol_type = "Type"
        self.id = id
        self.resolved_type = resolved_type

        # If the symbole can be resolved
        # Can be changed with the self.lock() command
        self._locked = False
    
    def lock(self):
        """
        Prevent the unresolved quote type from being locked.
        Should for example be used after the defintion of the function, before its call

        # WARNING
        A quote type should always be locked after the end of its definition, before its usage
        """
        self._locked = True

    def __eq__(self, other):
        """
        Charge the equality operation
        Allow to resolve unresolved quote type
        """
        if self.resolved_type is None:
            if self.lock:
                # The quote type is locked
                # An unresolved and locked type accept anything
                print("Comparing unresolved locked", self, other)
                return True
            else:
                # The type is unresolved but not locked
                print("Comparing unresolved", self, other)
                # We can now resolve the two elements
                self.resolved_type = other
                return True
        else:
            print("Comparing resolved", self, other)
            # The type is already resolved. We then need to compare the real type and the other type
            return self.resolved_type == other
    
    def __str__(self):
        if self.resolved_type is not None:
            return f"<SymbolQuoteType:{self.id} is {self.resolved_type}>"
        else:
            return f"<SymbolQuoteType:{self.id}>"
    
    def __repr__(self):
        return self.__str__()
    
class SymbolVariable(Symbol):
    def __init__(self, id, isref, value, type):
        self.symbol_type = "Variable"
        self.id = id
        self.isref = isref
        self.value = value
        self.type = type
    
    def __str__(self):
        return f"Variable {self.id}: isref={self.isref}; value={self.value}; type={self.type}"

class SymbolArrayVariable(Symbol):
    def __init__(self, id, size, value, type):
        self.symbol_type = "ArrayVariable"
        self.id = id
        self.size = size
        self.value = value          # An array?
        self.type = type            # Correspond of the type of the content of the variable
                                    # TODO: improve array_type Is it the type of the content or the type of 'a array?
    
    def __str__(self):
        return f"Variable {self.id}: isref={self.isref}; value={self.value}; type={self.type}"

class SymbolFunction(Symbol):
    def __init__(self, id, parameters_list, parameters_types_list, function_body_node, result_type, is_recursive):
        self.symbol_type = "Function"
        self.id = id
        self.parameters_list = parameters_list
        self.parameters_types_list = parameters_types_list
        self.function_body_node = function_body_node
        self.result_type = result_type
        self.is_recursive = is_recursive
    
    def __str__(self):
        text = f"Function {self.id}: "
        for param, ptype in zip(self.parameters_list, self.parameters_types_list):
            text += f"{param}:{ptype} -> "
        text += str(self.result_type)

        return text

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
        
    def __str__(self):
        text = "\n\n"

        text += "Following table:\n"
        text += "----------------\n"

        text += self.following_table.__str__()

        text += "Memory Table\n"
        text += "============\n"
        text += "scope_name: " + str(self.scope_name) + '\n'
        text += "scope_level: " + str(self.scope_level) + '\n'

        text += "\n"
        text += "Content:\n"
        text += "--------\n"

        for obj_id in self._memory.keys():
            text += str(obj_id) + ": " + str(self._memory[obj_id]) + "\n"
        

        text += "\n============\n\n"

        return text

    def __repr__(self):
        return self.__str__()
