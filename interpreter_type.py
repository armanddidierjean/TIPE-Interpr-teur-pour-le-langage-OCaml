from tools import *
from keywords import *
from baseclass import *

#####################
#    Interpreter    #
#####################
class InterpreterType(NodeVisitor):
    """
    OCaml InterpreterType

    Determine the type of the AST node
    WARNING: this class is functional but still a WIP

    Methods
    -------
    interpret()
        Interpret the AST

    Parameters
    ----------
    AST_node:
        an AST node that will be interpreted
    """
    def __init__(self, AST_node):
        self.AST_node = AST_node

        # Base memory table, countain builtin types
        self.memory_table = MemoryTable("Main", 0, None)
        self._init_base_types()
    
    def _init_base_types(self):
        print("TODO: Initing base type")
    
    def interpret(self):
        return self.visit(self.AST_node)
    
    #   Nodes visitors   #
    def visit_Program(self, node):
        log("Visiting Program")

        # Create a MemoryTable for the program, this allow to define local variables.
        mt = MemoryTable("Program", 1, self.memory_table)
        self.memory_table = mt

        # The type of the program is the type of the block node
        type = self.visit(node.block_node)

        # Remove the Program memory table
        self.memory_table = self.memory_table.following_table

        # Return the type
        return type
    
    def visit_Block(self, node):
        log("Visiting Block")
        # The type of a block is the type of the node it countain
        return self.visit(node.node)
    
    def visit_Sequence(self, node):
        log("Visiting Sequence")
        for command_node in node.commands_list[:-1]:
            type = self.visit(command_node)
            # The type of the sequence elements, except the last should be unit
            if type != UNIT:
                warning(f"{command_node} is of type {type} instead of unit in sequence")
        # The type of a sequence is the type of its last element
        return self.visit(node.commands_list[-1])

    def visit_Num(self, node):
        log("Visiting Num")
        # Can be INT, FLOAT, STRING
        return node.type
    
    def visit_BinOp(self, node):
        log("Visiting BinOp")
        # Integer operations
        # The left and right nodes should be of type int
        if node.op_token.type in (PLUS_INT, MINUS_INT, MUL_INT, DIV_INT):
            left_type = self.visit(node.left_node)
            if left_type != INT:
                error(f"Left node {node.left_node} is of type {left_type} instead of INTEGER in Binary Operation {node.op_token.type}")
            right_type = self.visit(node.right_node)
            if right_type != INT:
                error(f"Right node {node.right_node} is of type {right_type} instead of INTEGER in Binary Operation {node.op_token.type}")
            return INT
        # Boolean operation
        # The left and right nodes should have the same type
        if node.op_token.type in (EQUALS, DIFFERENT):
            left_type = self.visit(node.left_node)
            right_type = self.visit(node.right_node)
            if left_type != right_type:
                error(f"Left node {node.left_node} is of type {left_type} and right node {node.right_node} of type {right_type} which are not the same in Boolean Binary Operation {node.op_token.type}")
            return BOOL
        
        warning("Undefined operation BinOp", node.op_token.type)
        return UNIT

    def visit_UnaryOp(self, node):
        log("Visiting Unary Op")
        if node.op_token.type in (PLUS_INT, MINUS_INT):
            type = self.visit(node.right_node)
            if type != INT:
                error(f"Unary node {node.right_node} is of type {type} instead of INTEGER in Unary Operation {node.op_token.type}")
            return INT
        warning("Undefined operation UnaryOp")
        return UNIT
    
    def visit_AssignmentStatement(self, node):
        log("Visiting AssignmentStatement")

        # An assignement statement can create a new memory table with local variables 
        # or define variables in the current memory table

        # The syntax (LET assignments IN block) create a new memory table of level: current level + 1
        # The syntax (LET assignments) define variables in the current memory level

        # We need to create a new memory table if node.block_node is not an instance of UnitNode
        #create_a_new_memory_table = not isinstance(node.block_node, UnitNode)
        create_a_new_memory_table = type(node).__name__ != "UnitNode"
        
        if create_a_new_memory_table:
            print("Not an unit node : new memory table ")
            mt = MemoryTable("Assignement scope", self.memory_table.scope_level + 1, self.memory_table)
            self.memory_table = mt
        else:
            print("Unit node : Define var in the current level")
        
        for assignment_node in node.assignments_list:
            assignement_type = self.visit(assignment_node)
            # The type of the assignments should be unit
            #TODO: is this really useful?
            if assignement_type != UNIT:
                warning(f"{assignment_node} is of type {type} instead of unit in assignment statement")
        
        result_type = self.visit(node.block_node)

        if create_a_new_memory_table:
            # After evaluating the block, we need to remove the corresponding memory table
            self.memory_table = self.memory_table.following_table
        
        return result_type
    
    def visit_Assignment(self, node):
        log("Visiting Assignment")
        # We need to check the variable is not already defined as a local variable in the current memory table.
        if not self.memory_table.isdefined(node.var_name, look_following_table=False):
            # We create a new symbol corresponding to the variable, the value is None as we are only searching the type
            symbol = Symbol(node.var_name, node.is_ref, value=None, type=self.visit(node.value_node))
            self.memory_table.define(node.var_name, symbol)
            show(colors.CYELLOW, f"Assigning: {node.var_name} with type {symbol.type}", colors.ENDC)
            # An assignement is of type UNIT
            return UNIT
        else:
            error("Memory error:", node.var_name, "is already defined in the current memory table")
            raise SyntaxError("Variable already defined")

    def visit_Reassignment(self, node):
        log("Visiting Reassignment")
        if self.memory_table.isdefined(node.var_name):
            symbol = self.memory_table.get(node.var_name)
            if symbol.isref:
                # The variable can be reassigned
                value_type = self.visit(node.new_value_node)
                if symbol.type != value_type:
                    error(f"New value node {node.new_value_node} is of type {value_type} instead of {symbol.type} in Reassignment of {node.var_name}")
                # A reassignement is of type UNIT
                return UNIT
            else:
                error("Memory error:", node.var_name, "is not mutable")
                raise SyntaxError("Variable not mutable")
        else:
            error("Memory error:", node.var_name, "is not defined")
            raise SyntaxError("Variable not defined")
        
    def visit_Variable(self, node):
        log("Visiting Variable")
        log(f"Searshing the variable {node.var_name} {node.get_content}")
        
        if not self.memory_table.isdefined(node.var_name, look_following_table=True):
            raise MemoryError(f"The variable {node.var_name} is not defined")
        else:
            # The variable is defined, we can access it
            symbol = self.memory_table.get(node.var_name)

            # If the symbol is mutable, we can return the value or ['ref', value]
            if symbol.isref:
                if node.get_content:
                    # The variable is mutable and we are accessing its value (!var)
                    show(colors.CYELLOW, f"Accessing content of mutable variable {node.var_name}", colors.ENDC)
                    return symbol.type
                else:
                    # The variable is mutable
                    show(colors.CYELLOW, f"Accessing mutable variable {node.var_name}", colors.ENDC)
                    return ['ref', symbol.type]
            else:
                if node.get_content:
                    # The variable is not mutable and we are accessing its value (!var)
                    raise SyntaxError("Variable not mutable but its content is accessed")
                else:
                    # The variable is not mutable
                    show(colors.CYELLOW, f"Accessing content of variable {node.var_name}", colors.ENDC)
                    return symbol.type

    def visit_PrintInt(self, node):
        type = self.visit(node.node)
        if type != INT:
            error(f"Got {type} instead of INT in PrintInt")
        return UNIT

    def visit_PrintString(self, node):
        type = self.visit(node.node)
        if type != STRING:
            error(f"Got {type} instead of STRING in PrintString")
        return UNIT
    
    def visit_Loop(self, node):
        bool_type = self.visit(node.boolean_node)
        if bool_type != BOOL:
            error(f"Boolean_node is of type {bool_type} instead of BOOL in Loop")
        block_type = self.visit(node.block_node)
        if block_type != UNIT:
            warning(f"Block node is of type {block_type} instead of UNIT in Loop")
        return UNIT
    
    def visit_UnitNode(self, node):
        return UNIT