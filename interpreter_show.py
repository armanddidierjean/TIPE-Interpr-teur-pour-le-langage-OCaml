from tools import *
from keywords import *
from baseclass import *

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
    
    def visit_AssignementStatement(self, node):
        self.print_ind('AssignementStatement')
        self.print_ind('{')
        self.ind()
        self.print_ind('Assignements:')
        self.ind()
        for assignement_node in node.assignements_list:
            self.visit(assignement_node)
        self.deind()
        self.print_ind('Block:')
        self.visit(node.block_node)
        self.deind()
        self.print_ind('}')

    def visit_Assignement(self, node):
        self.print_ind('Assignement', node.var_name)
        self.print_ind('{')
        self.ind()
        self.visit(node.value_node)
        self.deind()
        self.print_ind('}')

    def visit_Reassignement(self, node):
        self.print_ind('Reassignement', node.var_name)
        self.print_ind('{')
        self.ind()
        self.visit(node.value_node)
        self.deind()
        self.print_ind('}')
        
    def visit_Variable(self, node):
        self.print_ind('Reassignement', node.var_name)
        self.print_ind('{')
        self.ind()
        self.print_ind(node.var_name, "getcontent", node.get_content)

        self.deind()
        self.print_ind('}')
        
    def visit_PrintInt(self, node):
        self.print_ind('PrintInt')
    
    def visit_Boucle(self, node):
        self.print_ind('Boucle')
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