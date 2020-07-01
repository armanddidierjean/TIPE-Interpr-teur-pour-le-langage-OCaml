from tools import *
from keywords import *
from astclass import *

#####################
#      Parser       #
#####################
class Parser:
    """
    OCaml Parser

    Methods
    -------
    parse()
        Parse the lexer's tokens flow and 
        return and AST node corresponding to the recognised patern 

    Parameters
    ----------
    lexer:
        a lexer that will be called to get the tokens flow
    """
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
    
    def eat(self, type):
        """
        Check if the current token is of type type and get the next token from the lexer

        Parameters
        ----------
        type : Keyword
            expected type of self.current_token
        """
        log(f"-> Eating {self.current_token} expecting type {type}")
        if self.current_token.type == type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise TypeError(f"Expected {type} token, got {self.current_token.type}")

    def parse(self):
        return self.program()
    
    def program(self):
        """ 
        block? SEMI SEMI
        
        Return Program node
        """
        log("Programm")
        if self.current_token.type != SEMI:
            node = self.block()
        self.eat(SEMI)
        self.eat(SEMI)

        #if self.lexer.current_token.type == LET:
        #    node = self.let_statement()
        #else:
        #    node = self.sequence()
        
        return Program(node)
    
    def block(self):
        """
          sequence -> BEGIN
        | command
        """
        log("Block")
        if self.current_token.type == BEGIN:
            node = self.sequence()
        else:
            node = self.command()
        
        return Block(node)

    def sequence(self):
        """
        BEGIN block (SEMI block)* END
        """
        log("Sequence")
        self.eat(BEGIN)
        
        blocks_list = [self.block()]

        while self.current_token.type == SEMI:
            self.eat(SEMI)
            blocks_list.append(self.block())
        
        self.eat(END)

        return Sequence(blocks_list)

    def command(self):
        """
        expr (PLUS block)?

        NE RENVOIT PAS DE NODE PROPRE
        -> return expr()
        -> return BinOp(expr, op, block)
        """
        log("Command")
        expr_node = self.expr()

        if self.current_token.type == PLUS_INT:
            op_token = self.current_token
            self.eat(PLUS_INT)
            block_node = self.block()
            return BinOp(expr_node, op_token, block_node)
        else:
            return expr_node
    
    def expr(self):
        """
        factor (MUL block)?

        NE RENVOIT PAS DE NODE PROPRE
        -> return expr()
        -> return BinOp(expr, op, block)
        """
        log("Expr")
        factor_node = self.factor()

        if self.current_token.type == MUL_INT:
            op_token = self.current_token
            self.eat(MUL_INT)
            block_node = self.block()
            return BinOp(factor_node, op_token, block_node)
        else:
            return factor_node

    def factor(self):
        """
        PLUS block
        MINUS block
        INT
        WHILE block (EQUAL | DIFFERENT) block DO block DONE
        assignement_statement -> LET
        variable_statement

        NE RENVOIT PAS DE NODE PROPRE
        """
        log("Factor")
        if self.current_token.type in (PLUS_INT, MINUS_INT):
            op_token = self.current_token
            self.eat(self.current_token.type)
            return UnaryOp(op_token, self.block())
        elif self.current_token.type in (INT, FLOAT):
            node = Num(self.current_token.value, self.current_token.type)
            self.eat(self.current_token.type)
            return node
        elif self.current_token.type == LET:
            return self.assignement_statement()
        elif self.current_token.type == WHILE:
            self.eat(WHILE)
            left_block = self.block()
            op_token = self.current_token
            if self.current_token.type == EQUALS:
                self.eat(EQUALS)
            else:
                self.eat(DIFFERENT)
            right_block = self.block()
            boolean_node = BinOp(left_block, op_token, right_block)
            self.eat(DO)
            block_node = self.block()
            self.eat(DONE)
            log(f"Returning a Boucle node boolean_node={boolean_node}, block_node={block_node}")
            return Boucle(boolean_node, block_node)
        elif self.current_token.type == PRINT_INT:
            self.eat(PRINT_INT)
            return PrintInt(self.block()) 
        else:
            return self.variable_statement()

        #TODO: romve:
        print(colors.WARNING, "ERROR parser:factor did not got an expencted token : ", self.current_token, colors.ENDC)

    def assignement_statement(self):
        """
        LET assignement (AND assignement)* IN block
        ~~LET assignement (AND assignement)*~~

        Return let_statement node
        """
        log("Assignement_statement")
        self.eat(LET)

        assignements_list = [self.assignement()]

        while self.current_token.type == AND:
            self.eat(AND)
            assignements_list.append(self.assignement())
        
        if self.current_token.type == IN:
            self.eat(IN)
            block = self.block()
        else:
            print(colors.WARNING, "WARNING: parser:assignement_statement global variable are not implemented", colors.ENDC)
            block = None
        
        return AssignementStatement(assignements_list, block)
    
    def assignement(self):
        """
        ID EQUALS block

        Return assignement node
        """
        log("Assignement")
        var_name = self.current_token.value
        self.eat(ID)

        self.eat(EQUALS)

        if self.current_token.type == REF:
            self.eat(REF)
            is_ref = True
        else:
            is_ref = False
        
        block_node = self.block()

        return Assignement(var_name, is_ref, block_node)

    def variable_statement(self):
        """
        EXCLAMATION ID

        ID REASSIGN block
        ID
        """
        log("Variable Statement")
        if self.current_token.type == EXCLAMATION:
            self.eat(EXCLAMATION)
            var_id = self.current_token.value
            self.eat(ID)
            return Variable(var_id, get_content=True)
            
        var_id = self.current_token.value
        self.eat(ID)

        if self.current_token.type == REASSIGN:
            self.eat(REASSIGN)
            return Reassignement(var_id, self.block())
        else:
            return Variable(var_id, get_content=False)