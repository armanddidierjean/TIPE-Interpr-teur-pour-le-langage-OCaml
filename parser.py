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
        return Program(node)
    
    def block(self):
        """
          LPAREN block? RPAREN
        | pres0

        USED FOR A BINOP
        """
        log("Block")
        if self.current_token.type == LPAREN:
            self.eat(LPAREN)
            """LPAREN RPAREN"""
            if self.current_token.type == RPAREN:
                return UnitNode()
            """LPAREN block RPAREN"""
            node = self.block()
            self.eat(RPAREN)
            return node
        else:
            return self.pres0()

    def pres0(self):
        """
          PLUS block
        | MINUS block
        | pres1 ((PLUS | MINUS) pres1)*

        USED FOR A BINOP OR A UNARYOP
        """
        log("Pres0")

        """PLUS block | MINUS block"""
        if self.current_token in (PLUS_INT, MINUS_INT):
            op_token = self.current_token
            self.eat(self.current_token.type)
            return UnaryOp(op_token, self.pres1())
        else:
            """code ((PLUS | MINUS) code)*"""
            node = self.pres1()
            while self.current_token.type in (PLUS_INT, MINUS_INT):
                op_token = self.current_token
                self.eat(self.current_token.type)
                node = BinOp(node, op_token, self.pres1())
            return node

    def pres1(self):
        """
        pres2 (MOD pres2)*

        USED FOR A BINOP
        """
        log("Pres1")
        node = self.pres2()

        while self.current_token.type in (MOD):
            op_token = self.current_token
            self.eat(self.current_token.type)
            node = BinOp(node, op_token, self.pres2())
        
        return node

    def pres2(self):
        """
        pres3 (MUL pres3)*

        USED FOR A BINOP
        """
        log("Pres2")
        node = self.pres3()

        while self.current_token.type in (MUL_INT):
            op_token = self.current_token
            self.eat(self.current_token.type)
            node = BinOp(node, op_token, self.pres3())
        
        return node

    def pres3(self):
        """
        pres4 (EQUAL | DIFFERENT) pres4

        USED FOR A BINOP
        """
        log("Pres3")
        node = self.pres4()

        while self.current_token.type in (EQUALS, DIFFERENT):
            op_token = self.current_token
            self.eat(self.current_token.type)
            node = BinOp(node, op_token, self.pres4())
        
        return node

    def pres4(self):
        """
        code ((BOOLEANCONJUNCTION | BOOLEANDISJUNCTION) code)*

        USED FOR A BINOP
        """
        log("pres4")
        node = self.code()

        while self.current_token.type in (BOOLEANCONJUNCTION, BOOLEANDISJUNCTION):
            op_token = self.current_token
            self.eat(self.current_token.type)
            node = BinOp(node, op_token, self.code())
        
        return node
    
    def code(self):
        """
          sequence      -> (BEGIN)
        | command
        """
        log("Code")
        if self.current_token.type == BEGIN:
            node = self.sequence()
        else:
            node = self.command()
        
        return Block(node)

    def sequence(self):
        """
        BEGIN END
        BEGIN block (SEMI block)* END
        """
        log("Sequence")
        self.eat(BEGIN)
        
        """BEGIN END"""
        if self.current_token.type == END:
            self.eat(END)
            return UnitNode()
        
        """BEGIN block (SEMI block)* END"""
        blocks_list = [self.block()]

        while self.current_token.type == SEMI:
            self.eat(SEMI)
            blocks_list.append(self.block())
        
        self.eat(END)

        return Sequence(blocks_list)

    def command(self):
        """
          INT 
        | FLOAT
        | PRINT_INT block
        | WHILE block DO block DONE
        | assignement_statement ->(LET)
        | variable_statement

        DO NOT RETURN HIS OWN NODE
        """
        log("Command")
        if self.current_token.type in (INT, FLOAT):
            node = Num(self.current_token.value, self.current_token.type)
            self.eat(self.current_token.type)
            return node
        elif self.current_token.type == LET:
            return self.assignement_statement()
        elif self.current_token.type == WHILE:
            self.eat(WHILE)
            boolean_node = self.block()
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

    def assignement_statement(self):
        """
        LET assignement (AND assignement)* IN block
        LET assignement (AND assignement)*

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
            print(colors.WARNING, "WARNING: parser:assignement_statement global variable are not implemented, using a UnitNode", colors.ENDC)
            block = UnitNode()
        
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