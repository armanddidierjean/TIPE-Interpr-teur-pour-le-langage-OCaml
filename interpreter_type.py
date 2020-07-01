from tools import *
from keywords import *
from baseclass import *

#####################
#    Interpreter    #
#####################
class InterpreterType(NodeVisitor):
    """
    OCaml Interpreter

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
        self.memory_table = MemoryTable()
    
    def interpret(self):
        return self.visit(self.AST_node)
    
    #   Nodes visitor   #
    def visit_Program(self, node):
        log("Visiting Program")
        return self.visit(node.block_node)
    
    def visit_Block(self, node):
        log("Visiting Block")
        return self.visit(node.node)
    
    def visit_Sequence(self, node):
        log("Visiting Sequence")
        for command_node in node.commands_list[:-1]:
            #TODO: return a warning if the result is not None
            type = self.visit(command_node)
            if type != UNIT:
                warning(f"{command_node} is of type {type} instead of unit in sequence")
        return self.visit(node.commands_list[-1])

    def visit_Num(self, node):
        log("Visiting Num")
        return node.type
    
    def visit_BinOp(self, node):
        log("Visiting BinOp")
        # TODO and MINUS AND SIV
        #print(node.op_token.type)
        # Integer operations
        if node.op_token.type in (PLUS_INT, MINUS_INT, MUL_INT, DIV_INT):
            left_type = self.visit(node.left_node)
            if left_type != INT:
                error(f"Left node {node.left_node} is of type {left_type} instead of INTEGER in Binary Operation {node.op_token.type}")
            right_type = self.visit(node.right_node)
            if right_type != INT:
                error(f"Right node {node.right_node} is of type {right_type} instead of INTEGER in Binary Operation {node.op_token.type}")
            return INT
        # Boolean operation
        if node.op_token.type in (EQUALS, DIFFERENT):
            left_type = self.visit(node.left_node)
            right_type = self.visit(node.right_node)
            if left_type != right_type:
                error(f"Left node {node.left_node} is of type {left_type} and right node {node.right_node} of type {right_type} which are not the same in Boolean Binary Operation {node.op_token.type}")
            return BOOL
        warning("Undefined operation BinOp")
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
    
    def visit_AssignementStatement(self, node):
        log("Visiting AssignementStatement")
        for assignement_node in node.assignements_list:
            type = self.visit(assignement_node)
            if type != UNIT:
                warning(f"{assignement_node} is of type {type} instead of unit in assignement statement")
        
        return self.visit(node.block_node)
    
    def visit_Assignement(self, node):
        log("Visiting Assignement")
        # TODO: implement variable storage
        if not self.memory_table.isdefined(node.var_name):
            self.memory_table.define(node.var_name, node.is_ref, type=self.visit(node.value_node))
            print(colors.CYELLOW, f"Assigning: {node.var_name} = {self.memory_table.get_value(node.var_name)}", colors.ENDC)
            return UNIT
        else:
            error("Memory error:", node.var_name, "is already defined")
            raise SyntaxError("Variable already defined")

    def visit_Reassignement(self, node):
        log("Visiting Reassignement")
        # TODO: implement variable storage
        if self.memory_table.isdefined(node.var_name):
            if self.memory_table.isref(node.var_name):
                # ref
                value_type = self.visit(node.new_value_node)
                if self.memory_table.get_type(node.var_name) != value_type:
                    error(f"New value node {node.new_value_node} is of type {value_type} instead of {self.memory_table.get_type(node.var_name)} in Reassignent of {node.var_name}")
                return UNIT
                #print(colors.CYELLOW, f"ReAssigning {node.var_name} := {self.memory_table.get_value(node.var_name)}", colors.ENDC)
            else:
                error("Memory error:", node.var_name, "is not mutable")
                raise SyntaxError("Variable not mutable")
        else:
            error("Memory error:", node.var_name, "is not defined")
            raise SyntaxError("Variable not defined")
        
    
    def visit_Variable(self, node):
        log("Visiting Variable")
        log(f"Searshing the variable {node.var_name} {node.get_content}")
        
        symbol = self.memory_table.get_symbol(node.var_name)

        # If the symbol is mutable, we can retrun the value or ['ref', value]
        if symbol.isref:
            if node.get_content:
                show(colors.CYELLOW, f"Accessing content of mutable variable {node.var_name}", colors.ENDC)
                return symbol.type
            else:
                show(colors.CYELLOW, f"Accessing mutable variable {node.var_name}", colors.ENDC)
                return ['ref', symbol.type]
        else:
            # The variable is not mutable
            show(colors.CYELLOW, f"Accessing content of variable {node.var_name}", colors.ENDC)
            return symbol.type

        """
        # Methode sans table memoire
        if node.var_name in MEMORY:
            if MEMORY[node.var_name][0]:
                if node.get_content:
                    show(colors.CYELLOW, f"Accessing content of mutable variable {node.var_name}", colors.ENDC)
                    return MEMORY[node.var_name][1]
                else:
                    show(colors.CYELLOW, f"Accessing mutable variable {node.var_name}", colors.ENDC)
                    return MEMORY[node.var_name]
            else:
                show(colors.CYELLOW, f"Accessing content of variable {node.var_name}", colors.ENDC)
                return MEMORY[node.var_name][1]
        else:
            print(colors.FAIL, "Memory error:", node.var_name, "is not defined", colors.ENDC)
            raise SyntaxError("Variable not defined")
        """

    def visit_PrintInt(self, node):
        type = self.visit(node.node)
        if type != INT:
            error(f"Got {type} instead of INT in PrintInt")
        return UNIT
    
    def visit_Boucle(self, node):
        bool_type = self.visit(node.boolean_node)
        if bool_type != BOOL:
            error(f"Boolean_node is of type {bool_type} instead of BOOL in Boucle")
        block_type = self.visit(node.block_node)
        if block_type != UNIT:
            warning(f"Block node is of type {block_type} instead of UNIT in Boucle")
        return UNIT