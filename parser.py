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
        return an AST node

    Parameters
    ----------
    lexer:
        a lexer that will be used to get the tokens flow
    """
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
    
    def match(self, type):
        """
        Check if the current token is of type `type` and get the next token from the lexer

        Parameters
        ----------
        type : Keyword
            expected type of self.current_token
        """
        log(f"-> Matching {self.current_token} expecting type {type}")
        if self.current_token.type == type:
            self.current_token = self.lexer.get_next_token()
        else:
            errorsManager.TypeError(f"Expected {type} token, got {self.current_token.type}")

    def parse(self):
        return self.program()
    
    def program(self):
        """ 
        block? SEMI SEMI

        Return a Program node
        """
        log("Program")
        if self.current_token.type != SEMI:
            node = self.block()
        else:
            node = UnitNode()
        self.match(SEMI)
        self.match(SEMI)
        return Program(node)
    
    def block(self):
        """
        pres0

        Does not return its own node
        """
        log("Block")
        return self.pres0()

    def pres0(self):
        """
          PLUS block
        | MINUS block
        | pres1 ((PLUS | MINUS) pres1)*

        Return a BinaryOperation or a UnaryOperation
        """
        log("Pres0")

        """PLUS block | MINUS block"""
        if self.current_token.type in (PLUS_INT, MINUS_INT):
            op_token = self.current_token
            self.match(self.current_token.type)
            block_node = self.block()
            return UnaryOp(op_token, block_node)
        else:
            """pres1 ((PLUS | MINUS) pres1)*"""
            node = self.pres1()
            while self.current_token.type in (PLUS_INT, MINUS_INT):
                op_token = self.current_token
                self.match(self.current_token.type)
                node = BinOp(node, op_token, self.pres1())
            return node

    def pres1(self):
        """
        pres2 (MOD pres2)*

        Return a BinaryOperation
        """
        log("Pres1")
        node = self.pres2()

        while self.current_token.type == MOD:
            op_token = self.current_token
            self.match(self.current_token.type)
            node = BinOp(node, op_token, self.pres2())
        
        return node

    def pres2(self):
        """
        pres3 (MUL pres3)*

        Return a BinaryOperation
        """
        log("Pres2")
        node = self.pres3()

        while self.current_token.type == MUL_INT:
            op_token = self.current_token
            self.match(self.current_token.type)
            node = BinOp(node, op_token, self.pres3())
        
        return node

    def pres3(self):
        """
        pres4 ((EQUAL | DIFFERENT) pres4)*

        Return a BinaryOperation
        """
        log("Pres3")
        node = self.pres4()

        while self.current_token.type in (EQUALS, DIFFERENT):
            op_token = self.current_token
            self.match(self.current_token.type)
            node = BinOp(node, op_token, self.pres4())
        
        return node

    def pres4(self):
        """
        code ((BOOLEANCONJUNCTION | BOOLEANDISJUNCTION) code)*

        Return a BinaryOperation
        """
        log("pres4")
        node = self.code()

        while self.current_token.type in (BOOLEANCONJUNCTION, BOOLEANDISJUNCTION):
            op_token = self.current_token
            self.match(self.current_token.type)
            node = BinOp(node, op_token, self.code())
        return node
    
    def code(self):
        """
          LPAREN block? RPAREN                            =>   LPAREN RPAREN should return UnitNode
                                                               LPAREN block RPAREN return self.block()
                                                               Calling self.block when the code is 
                                                               LPAREN RPAREN would return NothingNode
        | sequence      -> (BEGIN)
        | command

        Return a Block node
        """
        log("Code")
        if self.current_token.type == LPAREN:
            self.match(LPAREN)
            if self.current_token.type == RPAREN:
                node = UnitNode()
            else:
                node = self.block()
            self.match(RPAREN)
        elif self.current_token.type == BEGIN:
            node = self.sequence()
        else:
            node = self.command()
        
        # NOTE: we could replace `Block(node)` by `node`
        return Block(node)

    def sequence(self):
        """
        BEGIN END                       => Return UnitNode
        BEGIN block (SEMI block)* END

        Return UnitNode or a Sequence node
        """
        log("Sequence")
        self.match(BEGIN)
        
        """BEGIN END"""
        if self.current_token.type == END:
            self.match(END)
            return UnitNode()
        
        """BEGIN block (SEMI block)* END"""
        blocks_list = [self.block()]

        while self.current_token.type == SEMI:
            self.match(SEMI)
            blocks_list.append(self.block())
        
        self.match(END)

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
        | variable_statement ->(ID|EXCLAMATION)
        | nothing

        Does not return its own node
        """
        log("Command")
        if self.current_token.type in (INT, FLOAT, STRING):
            """INT | FLOAT | STRING"""
            node = Literal(self.current_token.value, self.current_token.type)
            self.match(self.current_token.type)
            return node
        elif self.current_token.type == LET:
            """assignment_statement"""
            return self.assignment_statement()
        elif self.current_token.type == WHILE:
            """WHILE block DO block DONE"""
            self.match(WHILE)
            boolean_node = self.block()
            self.match(DO)
            block_node = self.block()
            self.match(DONE)
            return Loop(boolean_node, block_node)
        elif self.current_token.type == IF:
            """IF block THEN block (ELSE block)?"""
            self.match(IF)
            condition_node = self.block()

            self.match(THEN)
            then_node = self.block()

            if self.current_token.type == ELSE:
                self.match(ELSE)
                else_node = self.block()
            else:
                else_node = UnitNode()
            
            return ConditionalStatement(condition_node, then_node, else_node)
        elif self.current_token.type == PRINT_INT:
            """PRINT_INT block"""
            self.match(PRINT_INT)
            return PrintInt(self.block())
        elif self.current_token.type == PRINT_STRING:
            """PRINT_STRING block"""
            self.match(PRINT_STRING)
            return PrintString(self.block())
        elif self.current_token.type == ID or self.current_token.type == EXCLAMATION:
            """variable_statement ->(ID|EXCLAMATION)"""
            return self.variable_statement()
        else:
            """nothing"""
            # The nothing command is used to determine the end of a function call
            return NothingClass()

    def assignment_statement(self):
        """
        LET assignment (AND assignment)* IN block
        LET assignment (AND assignment)*                => NOTE: currently UnitNode is used as the IN block

        Return a AssignmentStatement node
        """
        log("Assignment_statement")
        self.match(LET)

        assignments_list = [self.assignment()]

        while self.current_token.type == AND:
            self.match(AND)
            assignments_list.append(self.assignment())
        
        if self.current_token.type == IN:
            """LET assignment (AND assignment)* IN block"""
            self.match(IN)
            block = self.block()
        else:
            """LET assignment (AND assignment)*"""
            # We use a UnitNode node to create an assignment_statement without "IN block" part
            block = UnitNode()
        
        return AssignmentStatement(assignments_list, block)
    
    def assignment(self):
        """
        REC? ID (ID|LPAREN RPAREN)+ EQUAL block                  => Currified function assignment
        REC? ID EQUALS FUNCTION (ID|LPAREN RPAREN)+ ARROW block
        REC? ID EQUALS REF? block                                => The REC won't be used nor raise an error

        Return an AssignmentFunction or an AssignmentVariable node
        """
        log("Assignment")

        # The REC keyword will only be used if this is a function declaration. It won't raise an error.
        if self.current_token.type == REC:
            is_rec = True
            self.match(REC)
        else:
            is_rec = False
        
        var_name = self.current_token.value
        self.match(ID)


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
                        self.match(LPAREN)
                        # NOTE: couples and tuples are currently not supported
                        self.match(RPAREN)
                        # It's an unit parameter
                        # We use the None parameter to represent an UNIT id
                        parameter_id = None
                else:
                    """ID"""
                    parameter_id = self.current_token.value
                    self.match(ID)
                    
                parameters_list.append(parameter_id)
            
            self.match(EQUALS)

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

            self.match(EQUALS)

            if self.current_token.type == FUNCTION:
                # It's a function declaration
                self.match(FUNCTION)
                parameters_list = []

                # We need at least one (ID|LPAREN RPAREN) in the parameters_list.
                # If we pass the following test, we should have parameters declared
                if self.current_token.type == ARROW:
                    errorsManager.SyntaxError("Expected at least one parameter in the function declaration, got none")

                while self.current_token.type != ARROW:
                    
                    if self.current_token.type == LPAREN:
                        """LPAREN RPAREN"""
                        self.match(LPAREN)
                        # NOTE: couples and tuples are currently not supported
                        self.match(RPAREN)
                        # It's an unit parameter
                        # We use the None parameter to represent an UNIT id
                        parameter_id = None
                    else:
                        """ID"""
                        parameter_id = self.current_token.value
                        self.match(ID)
                    
                    parameters_list.append(parameter_id)

                self.match(ARROW)

                # The types are not yet determined
                parameters_types_list = [None] * len(parameters_list)

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
                    self.match(REF)
                    is_ref = True
                else:
                    is_ref = False
            
                block_node = self.block()
                return AssignmentVariable(var_name, is_ref, block_node)

    def variable_statement(self):
        """
          EXCLAMATION ID
        | ID REASSIGN block
        | ID (block != nothing)*        => If there is no block, it's a variable
                                           else, it's a function call
        """
        log("Variable Statement")

        """EXCLAMATION ID"""
        if self.current_token.type == EXCLAMATION:
            self.match(EXCLAMATION)
            var_id = self.current_token.value
            self.match(ID)
            return Variable(var_id, get_content=True)
        
        """ID REASSIGN block
         | ID (code != nothing)*"""
        var_id = self.current_token.value
        self.match(ID)

        if self.current_token.type == REASSIGN:
            """ID REASSIGN block"""
            self.match(REASSIGN)
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
                # We open the block
                following_block_node_content = following_block.node
            else:
                following_block_node_content = following_block
            
            while not type(following_block_node_content).__name__ == "NothingClass":
                # Found a new id
                arguments_nodes_list.append(following_block)
                following_block = self.code()

                if type(following_block).__name__ == "Block":
                    # We open the block
                    following_block_node_content = following_block.node
                else:
                    following_block_node_content = following_block
            
            # We can now determine if the syntax was a function call or a variable access
            if len(arguments_nodes_list) == 0:
                # It's a variable call. (The variable can be a function but it will not be executed)
                return Variable(var_id, get_content=False)
            else:
                # It's a function call
                return FunctionCall(var_id, arguments_nodes_list)
