from tools import *
from keywords import *
from baseclass import *

"""
File containing an interpreter that print the content of the AST node.
"""

#####################
#    Interpreter    #
#####################
class InterpreterShow(NodeVisitor):
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
        self.indentation = 0
        self.indentation_string = '    '
    
    def print_ind(self, *arg):
        print(self.indentation_string * self.indentation, *arg)
    def ind(self):
        self.indentation += 1
    def deind(self):
        self.indentation -= 1

    def interpret(self):
        return self.visit(self.AST_node)
    
    #   Nodes visitor   #
    def visit_Program(self, node):
        self.print_ind('Program')
        self.print_ind('{')
        self.ind()
        self.visit(node.block_node)
        self.deind()
        self.print_ind('}')
        
    
    def visit_Block(self, node):
        self.print_ind('Block')
        self.print_ind('{')
        self.ind()
        self.visit(node.node)
        self.deind()
        self.print_ind('}')
    
    def visit_Sequence(self, node):
        self.print_ind('Sequence')
        self.print_ind('{')
        self.ind()
        self.visit(node.node)
        
        for command_node in node.commands_list[:-1]:
            self.visit(command_node)
            self.print_ind('-------')
        self.visit(node.commands_list[-1])
        self.deind()
        self.print_ind('}')

    def visit_Num(self, node):
        self.print_ind('Num')
        self.print_ind('{')
        self.ind()
        self.print_ind(node.value)
        self.deind()
        self.print_ind('}')
    
    def visit_BinOp(self, node):
        self.print_ind('BinOp', node.op_token.type)
        self.print_ind('{')
        self.ind()
        self.visit(node.left_node)
        self.print_ind(node.op_token.value)
        self.visit(node.right_node)
        self.deind()
        self.print_ind('}')

    def visit_UnaryOp(self, node):
        self.print_ind('UnaryOp', node.op_token.type)
        self.print_ind('{')
        self.ind()
        self.visit(node.right_node)
        self.deind()
        self.print_ind('}')
    
    def visit_AssignmentStatement(self, node):
        self.print_ind('AssignmentStatement')
        self.print_ind('{')
        self.ind()
        self.print_ind('Assignments:')
        self.ind()
        for assignment_node in node.assignments_list:
            self.visit(assignment_node)
        self.deind()
        self.print_ind('Block:')
        self.visit(node.block_node)
        self.deind()
        self.print_ind('}')

    def visit_Assignment(self, node):
        self.print_ind('Assignment', node.var_name)
        self.print_ind('{')
        self.ind()
        self.visit(node.value_node)
        self.deind()
        self.print_ind('}')

    def visit_Reassignment(self, node):
        self.print_ind('Reassignment', node.var_name)
        self.print_ind('{')
        self.ind()
        self.visit(node.value_node)
        self.deind()
        self.print_ind('}')
        
    def visit_Variable(self, node):
        self.print_ind('Reassignment', node.var_name)
        self.print_ind('{')
        self.ind()
        self.print_ind(node.var_name, "getcontent", node.get_content)

        self.deind()
        self.print_ind('}')
        
    def visit_PrintInt(self, node):
        self.print_ind('PrintInt')
    
    def visit_PrintString(self, node):
        self.print_ind('PreintString')
    
    def visit_Loop(self, node):
        self.print_ind('Loop')
        self.print_ind('{')
        self.ind()
        self.print_ind('Boolean operation')
        self.visit(node.boolean_node)
        self.print_ind('Block')
        self.visit(node.block_node)
        self.deind()
        self.print_ind('}')
        
    def visit_UnitNode(self, node):
        self.print_ind('UnitNode')