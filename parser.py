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
        return and AST node corresponding to the recognized pattern 

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
        log("Program")
        if self.current_token.type != SEMI:
            node = self.block()
        self.eat(SEMI)
        self.eat(SEMI)
        return Program(node)
    
    def block(self):
        """
          # TODO: Remove @LPARENRPAREN
          #LPAREN block? RPAREN
        | pres0

        USED FOR A BINOP
        """
        log("Block")
        
        # Removed to put LPAREN block? RPAREN in code
        # TODO: should work without. Remove this code Remove @LPARENRPAREN
        #if self.current_token.type == LPAREN:
        #    self.eat(LPAREN)
        #    """LPAREN RPAREN"""
        #    if self.current_token.type == RPAREN:
        #        log("This block is a UnitNode")
        #        self.eat(RPAREN)
        #        return UnitNode()
        #    """LPAREN block RPAREN"""
        #    node = self.block()
        #    self.eat(RPAREN)
        #    return node
        #else:
        #    return self.pres0()
        return self.pres0()

    def pres0(self):
        """
          PLUS block
        | MINUS block
        | pres1 ((PLUS | MINUS) pres1)*

        USED FOR A BINOP OR AN UNARYOP
        """
        log("Pres0")

        """PLUS block | MINUS block"""
        if self.current_token in (PLUS_INT, MINUS_INT):
            op_token = self.current_token
            log("pres0 is eating a self type:", self.current_token)
            self.eat(self.current_token.type)
            return UnaryOp(op_token, self.pres1())
        else:
            """code ((PLUS | MINUS) code)*"""
            node = self.pres1()
            while self.current_token.type in (PLUS_INT, MINUS_INT):
                op_token = self.current_token
                log("pres0 is eating a self type2:", self.current_token)
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

        while self.current_token.type == MOD:
            op_token = self.current_token
            log("pres1 is eating a self type:", self.current_token)
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

        while self.current_token.type == MUL_INT:
            op_token = self.current_token
            log("pres2 is eating a self type:", self.current_token)
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
            log("pres3 is eating a self type:", self.current_token)
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
            log("pres4 is eating a self type:", self.current_token)
            self.eat(self.current_token.type)
            node = BinOp(node, op_token, self.code())
        
        return node
    
    def code(self):
        """
          LPAREN block? RPAREN                            => On vérifie l'absence de RPAREN avant de chercher le block 
                                                               LPAREN RPAREN doit renvoyer UnitNode
                                                               block() renverra NothingNode
        | sequence      -> (BEGIN)
        | command
        """
        log("Code")
        if self.current_token.type == LPAREN:
            self.eat(LPAREN)
            if self.current_token.type == RPAREN:
                node = UnitNode()
            else:
                node = self.block()
            self.eat(RPAREN)
        elif self.current_token.type == BEGIN:
            node = self.sequence()
        else:
            node = self.command()
        
        # TODO: remove Block(node) to use only node
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
        | STRING
        | assignment_statement ->(LET)
        | WHILE block DO block DONE
        | IF block THEN block (ELSE block)?
        | PRINT_INT block
        | PRINT_STRING block
        #TODO: REMOVE @LPARENRPAREN
        #| LPAREN RPAREN                 => Permet des arguments UNIT (UnitNode) lors des appels de fonction
        #                                   Car id cherche des codes et non des block (problème avec 1 + 1)
        #                                   LPAREN block RPAREN *should* not happen
        | variable_statement ->(ID|EXCLAMATION)
        | nothing

        DO NOT RETURN HIS OWN NODE
        """
        log("Command")
        if self.current_token.type in (INT, FLOAT, STRING):
            """INT | FLOAT | STRING"""
            node = Num(self.current_token.value, self.current_token.type)
            print("NUM:", self.current_token.value, self.current_token.type)
            log("Command is eating a self type (should be a num):", self.current_token)
            self.eat(self.current_token.type)
            return node
        elif self.current_token.type == LET:
            """assignment_statement"""
            return self.assignment_statement()
        elif self.current_token.type == WHILE:
            """WHILE block DO block DONE"""
            self.eat(WHILE)
            boolean_node = self.block()
            self.eat(DO)
            block_node = self.block()
            self.eat(DONE)
            log(f"Returning a Loop node boolean_node={boolean_node}, block_node={block_node}")
            return Loop(boolean_node, block_node)
        elif self.current_token.type == IF:
            """IF block THEN block (ELSE block)?"""
            self.eat(IF)
            condition_node = self.block()

            self.eat(THEN)
            then_node = self.block()

            if self.current_token.type == ELSE:
                self.eat(ELSE)
                else_node = self.block()
            else:
                else_node = UnitNode()
            
            return ConditionalStatement(condition_node, then_node, else_node)
        elif self.current_token.type == PRINT_INT:
            """PRINT_INT block"""
            self.eat(PRINT_INT)
            return PrintInt(self.block())
        elif self.current_token.type == PRINT_STRING:
            """PRINT_STRING block"""
            self.eat(PRINT_STRING)
            return PrintString(self.block())
        # TODO: Remove @LPARENRPAREN
        #elif self.current_token.type == LPAREN:
        #    print("Finding an UnitNode in code (LPAREN RPAREN), used to be able to use UNIT argument in function call (see comments). LPAREN block RPAREN *should* not happen")
        #    self.eat(LPAREN)
        #    self.eat(RPAREN)
        #    return UnitNode()
        elif self.current_token.type == ID or self.current_token.type == EXCLAMATION:
            """variable_statement ->(ID|EXCLAMATION)"""
            return self.variable_statement()
        else:
            """nothing"""
            # The nothing command is used to determine the end of a function call
            # TODO: Improve class distinction NothingClass/UnitNode
            return NothingClass()

    def assignment_statement(self):
        """
        LET assignment (AND assignment)* IN block
        LET assignment (AND assignment)*                => TODO: to implement, for the moment we just use an IN UnitNode

        Return let_statement node
        """
        log("Assignment_statement")
        self.eat(LET)

        assignments_list = [self.assignment()]

        while self.current_token.type == AND:
            self.eat(AND)
            assignments_list.append(self.assignment())
        
        if self.current_token.type == IN:
            """LET assignment (AND assignment)* IN block"""
            self.eat(IN)
            block = self.block()
        else:
            """LET assignment (AND assignment)*"""
            # We use a UnitNode node to create an assignment_statement without "IN block" part
            show(colors.WARNING, "WARNING: parser:assignment_statement global variable are not implemented, using a UnitNode", colors.ENDC)
            block = UnitNode()
        
        return AssignmentStatement(assignments_list, block)
    
    def assignment(self):
        """
        REC? ID (ID|LPAREN RPAREN)+ EQUAL block                     => Currified function assignment
        REC? ID EQUALS FUNCTION (ID|LPAREN RPAREN)+ ARROW block
        REC? ID EQUALS REF? block                                   => The REC won't be used nor raise an error

        Return assignment node
        """
        log("Assignment")

        # The REC keyword will only be used if this is a function declaration. It won't raise an error.
        if self.current_token.type == REC:
            is_rec = True
            self.eat(REC)
        else:
            is_rec = False
        
        var_name = self.current_token.value
        self.eat(ID)

        # Currified function assignment
        if self.current_token.type != EQUALS:
            """
            REC? ID (ID|LPAREN RPAREN)+ EQUAL block
            """

            parameters_list = []

            while self.current_token.type != EQUALS:
                # There is a new parameter name

                if self.current_token.type == LPAREN:
                        """LPAREN RPAREN"""
                        self.eat(LPAREN)
                        #TODO: Support couples
                        self.eat(RPAREN)
                        # It's an unit parameter
                        # We use the None parameter to represent an UNIT id
                        parameter_id = None
                else:
                    """ID"""
                    parameter_id = self.current_token.value
                    self.eat(ID)
                    
                parameters_list.append(parameter_id)
            
            self.eat(EQUALS)

            # The types are not yet determined
            parameters_types_list = [None] * len(parameters_list)

            print("searching a function body")
            function_body_node = self.block()

            function_node = Function(parameters_list, parameters_types_list, function_body_node)

            # The function is represented by the Function class.
            # let f a b c = block 
            # will be stored as Function(["a", "b", "c"], [None, None, None], block)
                
            return AssignmentFunction(var_name, function_node, is_recursive=is_rec)
        
        # Non currified function or non function assignment
        else:

            self.eat(EQUALS)

            if self.current_token.type == FUNCTION:
                # It's a function declaration
                self.eat(FUNCTION)
                parameters_list = []

                # We need at least one (ID|LPAREN RPAREN) in the parameters_list.
                # If we pass the following test, we should have parameters declared
                if self.current_token.type == ARROW:
                    raise SyntaxError("Expected at least one parameter in the function declaration, got none")

                while self.current_token.type != ARROW:
                    
                    if self.current_token.type == LPAREN:
                        """LPAREN RPAREN"""
                        self.eat(LPAREN)
                        #TODO: Support couples
                        self.eat(RPAREN)
                        # It's an unit parameter
                        # We use the None parameter to represent an UNIT id
                        parameter_id = None
                    else:
                        """ID"""
                        parameter_id = self.current_token.value
                        self.eat(ID)
                    
                    parameters_list.append(parameter_id)

                self.eat(ARROW)

                # The types are not yet determined
                parameters_types_list = [None] * len(parameters_list)

                print("searching a function body")
                function_body_node = self.block()

                function_node = Function(parameters_list, parameters_types_list, function_body_node)

                # The function is represented by the Function class.
                # let f = fun a b c -> block 
                # will be stored as Function(["a", "b", "c"], [None, None, None], block)
                
                return AssignmentFunction(var_name, function_node, is_recursive=is_rec)

            else:
                # It's not a function declaration
                # It's then a variable declaration
                if self.current_token.type == REF:
                    self.eat(REF)
                    is_ref = True
                else:
                    is_ref = False
            
                block_node = self.block()
                return AssignmentVariable(var_name, is_ref, block_node)        

    """
    # Alternative function déclaration grammar
    def assignment(self):
        ""#"
        ID EQUALS function (-> FUNCTION)
        ID EQUALS REF? block

        Return assignment node
        ""#"
        log("Assignment")
        var_name = self.current_token.value
        self.eat(ID)

        self.eat(EQUALS)

        if self.current_token.type == FUNCTION:
            # It's a function declaration
            self.eat(FUNCTION)
            # The function is represented by the Function class.
            # let f = fun a b c -> block 
            # will be stored as Function(a -> Function(b -> Function(c -> block)))
            print("searching a function body")
            content_node = self.function_body()
            return AssignmentFunction(var_name, content_node)

        else:
            # It's not a function declaration
            # It's then a variable declaration
            if self.current_token.type == REF:
                self.eat(REF)
                is_ref = True
            else:
                is_ref = False
        
            block_node = self.block()
            return AssignmentVariable(var_name, is_ref, block_node)        

    def function_body(self):
        ""#"
        (LPAREN RPAREN)|ID) (ARROW block|function_body)

        Return a function node.
        This function allow to use recursion to create the nested Functions nodes
        ""#"
        
        if self.current_token.type == LPAREN:
            ""#"LPAREN RPAREN""#"
            self.eat(LPAREN)
            #TODO: Support couples
            self.eat(RPAREN)
            # It's an unit parameter
            parameter_id = None
        else:
            ""#"ID""#"
            parameter_id = self.current_token.value
            self.eat(ID)
        
        if self.current_token.type == ARROW:
            ""#"ARROW block""#"
            self.eat(ARROW)
            block_node = self.block()
            return Function(parameter_id, block_node)

        else:
            ""#"function_body""#"
            function_node = self.function_body()

            return Function(parameter_id, function_node)
    """

    def variable_statement(self):
        """
          EXCLAMATION ID
        | ID REASSIGN block
        | ID (block != nothing)*        => Utilisé pour les appels de fonctions : 
                                            Pas de block = variable
                                            Au moins un block = appel d'une fonction (avec un argument)

        # If there is no block then it's a variable
        # Else it's a function call
        """
        log("Variable Statement")

        """EXCLAMATION ID"""
        if self.current_token.type == EXCLAMATION:
            self.eat(EXCLAMATION)
            var_id = self.current_token.value
            self.eat(ID)
            return Variable(var_id, get_content=True)
        
        """ID REASSIGN block
         | ID (code != nothing)*"""
        var_id = self.current_token.value
        self.eat(ID)

        if self.current_token.type == REASSIGN:
            """ID REASSIGN block"""
            self.eat(REASSIGN)
            return Reassignment(var_id, self.block())
        else:
            """ID (code != nothing)*"""
            arguments_nodes_list = []

            print(colors.FAIL, "STARTING BLOCK", colors.ENDC)
            #following_block = self.block()     # Issue a + 2 is interpreted as ID BinOp(Nothing, PLUS, 2)
            following_block = self.code()       

            # WARNING block() is not transparent
            # if following_block is a block node we need to get the node it contains
            # because we need to check whether the content of the block node is or not a NothingClass
            if type(following_block).__name__ == "Block":
                print("Opening block node in id check")
                following_block_node_content = following_block.node
            else:
                print("Not a block node in id check")
                following_block_node_content = following_block
            
            while not type(following_block_node_content).__name__ == "NothingClass":
                arguments_nodes_list.append(following_block)
                print(colors.FAIL, "CONTINUE FINDING BLOCK in id check (function or variable) ", type(following_block_node_content).__name__, colors.ENDC)
                following_block = self.code()

                if type(following_block).__name__ == "Block":
                    print("Opening block node in id check (function or variable) OK")
                    following_block_node_content = following_block.node
                else:
                    print("It was not a block node in id check (function or variable) OK")
                    following_block_node_content = following_block
            
            # We can now determine if the syntax was a function call or a variable access
            if len(arguments_nodes_list) == 0:
                # It's a variable call. (The variable can be a function but it will not be executed)
                return Variable(var_id, get_content=False)
            else:
                # It's a function call
                return FunctionCall(var_id, arguments_nodes_list)