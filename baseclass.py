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
        return f'Token({self.type}, {self.value})'

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
        errorsManager.Exception(f'No visit_{type(node).__name__} method')

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
    """
    symbol_type = "Symbol"
    def __init__(self, id):
        self.symbol_type = "Symbol"
        self.id = id

class SymbolType(Symbol):
    """
    Represent a type
    """
    def __init__(self, id):
        self.symbol_type = "Type"
        self.id = id
    
    def get_symbol_type(self):
        """
        Return the quote object corresponding to the type
        Used for function call
        """
        return self
    
    def __str__(self):
        return f"<{self.id}>"
    
    def __repr__(self):
        return self.__str__()


class SymbolQuoteType(Symbol):
    """
    Represent a quote type ('a, 'b)
    This type is used as a placeholder type which can be resolved.

    Comparison between type can be managed by this class
     - If the type is already resolved, it calls a comparison with the resolved type
     - If it is not resolved, the type becomes resolved and the comparison return True
    We assume the comparison between two types is sufficient to determine types

    The resolution usually happen in function definitions and calls

    # NOTE: Using the same id twice *should* be a problem as we use id check to differentiate symboles

    Attributes
    ----------
    numeric_id : string
        Identifier for the quote symbole
    resolved_type : SymbolType object, optional
        The type that should be used to resolve this symbol
    
    Methods
    -------
    lock
        Lock the quote type to prevent it from being resolved.
        A quote type should always be locked after it's use (ex: after a function definition)
    """
    def __init__(self, numeric_id, resolved_type=None):
        self.symbol_type = "QuoteType"
        self.numeric_id = numeric_id
        self.resolved_type = resolved_type

        # If the symbole can be resolved
        # Can be changed with the self.lock() command
        self._locked = False
    
    def lock(self):
        """
        Prevent the unresolved quote type from being locked.
        Should for example be used after the defintion of the function, before its call

        # WARNING: A quote type should always be locked after the end of its definition
        """
        self._locked = True
    
    def get_symbol_type(self):
        """
        If the symbol is resolved, call and return get_symbol_type() on the resolved type
        Else return itself

        This method is used for function call

        Always return a TypeSymbol or an unresolved SymbolQuoteType
        """
        if self.resolved_type is None:
            return self
        else:
            return self.resolved_type.get_symbol_type()
    
    def _generate_string_identifier(self):
        """
        Construct and return a string identifying the symbole (format: a b ... z aa bb ... zz aaa bbb ... zzz)
        
        This method is used to get a human readable representation of the type
        """
        return chr(ord('a') + self.numeric_id % 26) * (self.numeric_id // 26 + 1)

    def __eq__(self, other):
        """
        Charge the equality operation to allow the class to resolve unresolved quote type
         - If the type is already resolved, it calls a comparison with the resolved type
         - If it is not resolved, the type becomes resolved and the comparison return True
        """
        if self.resolved_type is None:
            if self._locked:
                # The quote type is locked
                # An unresolved and locked type accept anything
                warning("Comparing unresolved and locked type")
                return True
            else:
                # The type is unresolved but not locked
                # We can resolve the two elements
                self.resolved_type = other
                return True
        else:
            # The type is already resolved. We then need to compare the real type and the other type
            return self.resolved_type == other
    
    def __str__(self):
        if self.resolved_type is not None:
            return f"<SymbolQuoteType:{self._generate_string_identifier()} is {self.resolved_type}>"
        else:
            return f"<SymbolQuoteType:{self._generate_string_identifier()}>"
    
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
        self.value = value
        self.type = type
    
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
        for parameter, parameter_type in zip(self.parameters_list, self.parameters_types_list):
            text += f"{parameter}:{parameter_type} -> "
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
        A memory table which the class should use to get symbols unavailable in the current scope
    
    Methods
    -------
    define(id, symbol)
        Define a symbol in the memory
    get(id)
        Return the symbol named id
        Return None if it is not defined
    isdefined(id, look_following_table=True)
        If a symbol id is defined
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
        If the symbol id is defined

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
        text = f"""
Following table:
----------------

{self.following_table.__str__()}

Memory Table
============
scope_name: {str(self.scope_name)}
scope_level: {str(self.scope_level)}

Content:
--------
"""
        for obj_id in self._memory.keys():
            text += str(obj_id) + ": " + str(self._memory[obj_id]) + "\n"
        
        text += "============"

        return text

    def __repr__(self):
        return self.__str__()
