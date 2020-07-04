from tools import *
from keywords import *
from baseclass import *

#####################
#    Interpreter    #
#####################
class InterpreterValue(NodeVisitor):
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
            # The result of these nodes is not used
            # # InterpreterType will return a warning if their type is not unit
            self.visit(command_node)
        return self.visit(node.commands_list[-1])

    def visit_Num(self, node):
        log("Visiting Num")
        return node.value
    
    def visit_BinOp(self, node):
        log("Visiting BinOp")
        # Integer operations
        if node.op_token.type == PLUS_INT:
            return self.visit(node.left_node) + self.visit(node.right_node)
        if node.op_token.type == MINUS_INT:
            return self.visit(node.left_node) - self.visit(node.right_node)
        if node.op_token.type == MUL_INT:
            return self.visit(node.left_node) * self.visit(node.right_node)
        if node.op_token.type == DIV_INT:
            return self.visit(node.left_node) / self.visit(node.right_node)

        # Boolean operation
        #TODO: check the type of elements: an equality between list should be an equality between it's content
        if node.op_token.type == EQUALS:
            return self.visit(node.left_node) == self.visit(node.right_node)
        if node.op_token.type == DIFFERENT:
            return self.visit(node.left_node) != self.visit(node.right_node)

    def visit_UnaryOp(self, node):
        log("Visiting UnaryOp")
        if node.op_token.type == PLUS_INT:
            return self.visit(node.right_node)
        if node.op_token.type == MINUS_INT:
            return -self.visit(node.right_node)
    
    def visit_AssignementStatement(self, node):
        log("Visiting AssignementStatement")
        for assignement_node in node.assignements_list:
            self.visit(assignement_node)
        
        return self.visit(node.block_node)
    
    # WARNING: the following methods need some improvements

    def visit_Assignement(self, node):
        log("Visiting Assignement")
        if not self.memory_table.isdefined(node.var_name):
            self.memory_table.define(node.var_name, node.is_ref, value=self.visit(node.value_node))
            show(colors.CYELLOW, f"Assigning: {node.var_name} = {self.memory_table.get_value(node.var_name)}", colors.ENDC)
        else:
            print(colors.FAIL, "Memory error:", node.var_name, "is already defined", colors.ENDC)
            raise SyntaxError("Variable already defined")

    def visit_Reassignement(self, node):
        log("Visiting Reassignement")
        if self.memory_table.isdefined(node.var_name):
            if self.memory_table.isref(node.var_name):
                # ref
                self.memory_table.change_value(node.var_name, self.visit(node.new_value_node))
                log(colors.CYELLOW, f"ReAssigning {node.var_name} := {self.memory_table.get_value(node.var_name)}", colors.ENDC)
            else:
                print(colors.FAIL, "Memory error:", node.var_name, "is not mutable", colors.ENDC)
                raise SyntaxError("Variable not mutable")
        else:
            print(colors.FAIL, "Memory error:", node.var_name, "is not defined", colors.ENDC)
            raise SyntaxError("Variable not defined")
        
    
    def visit_Variable(self, node):
        log("Visiting Variable")
        log(f"Searshing the variable {node.var_name} {node.get_content}")
        
        symbol = self.memory_table.get_symbol(node.var_name)

        # If the symbol is mutable, we can return the value or ['ref', value]
        if symbol.isref:
            if node.get_content:
                show(colors.CYELLOW, f"Accessing content of mutable variable {node.var_name}", colors.ENDC)
                return symbol.value
            else:
                show(colors.CYELLOW, f"Accessing mutable variable {node.var_name}", colors.ENDC)
                return ['ref', symbol]
        else:
            # The variable is not mutable
            show(colors.CYELLOW, f"Accessing content of variable {node.var_name}", colors.ENDC)
            return symbol.value

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
        print(colors.BOLD, self.visit(node.node), colors.ENDC)
    
    def visit_PrintString(self, node):
        print(colors.BOLD, self.visit(node.node), colors.ENDC)
    
    def visit_Loop(self, node):
        while self.visit(node.boolean_node):
            # TODO: warning if the type is not None
            self.visit(node.block_node)
    
    def visit_UnitNode(self, node):
        return None