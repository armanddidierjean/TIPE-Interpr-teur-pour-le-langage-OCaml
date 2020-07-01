#####################
#     Data  Type    #
#####################

class Token:
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
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

#####################
#      Memory       #
#####################
class Symbol(object):
    def __init__(self, id, isref, value, type):
        self.id = id
        self.isref = isref
        self.value = value
        self.type = type

class MemoryTable(object):
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
    def reassigne(self, id, type=None, value=None):
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



    

