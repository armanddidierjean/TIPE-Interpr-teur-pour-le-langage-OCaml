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
        
        # Base memory table, countain builtin types
        self.memory_table = MemoryTable("Main", 0, None)
        
        #TODO: Is it useful to init base types?
        #self._init_base_types()
    
    # TODO: Is it useful to init base types?
    #def _init_base_types(self):
    #    print("Initing base type")
    #    for symbol in BUILTIN_TYPES:
    #        self.memory_table.define(symbol.id, symbol)
    
    def interpret(self):
        return self.visit(self.AST_node)
    
    #   Nodes visitors   #
    def visit_Program(self, node):
        log("Visiting Program")
        # Create a MemoryTable for the program, this allow to define local variables.
        mt = MemoryTable("Program", 1, self.memory_table)
        self.memory_table = mt

        # The type of the program is the type of the block node
        result = self.visit(node.block_node)

        # Remove the Program memory table
        self.memory_table = self.memory_table.following_table

        # Return the type
        return result
    
    def visit_Block(self, node):
        log("Visiting Block")
        return self.visit(node.node)
    
    def visit_Sequence(self, node):
        log("Visiting Sequence")
        for command_node in node.commands_list[:-1]:
            # The result of these nodes is not used
            # InterpreterType will return a warning if their type is not unit
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
            self.visit(assignment_node)
        
        result = self.visit(node.block_node)

        if create_a_new_memory_table:
            # After evaluating the block, we need to remove the corresponding memory table
            self.memory_table = self.memory_table.following_table
        
        return result
    
    # WARNING: the following methods need some improvements

    def visit_AssignmentVariable(self, node):
        log("Visiting AssignmentVariable")

        # We don't need to check if the statement is correct as it was done before by the InterpreterType
        symbol = SymbolVariable(node.var_name, node.is_ref, value=self.visit(node.value_node), type=None)
        # the type is None as we don't use types in InterpreterValue
        
        self.memory_table.define(node.var_name, symbol)
        show(colors.YELLOW, f"Assigning Variable: {node.var_name} with type {symbol.type}, isref = {symbol.isref}", colors.ENDC)

    """ TODO: remove
    def visit_AssignmentFunction(self, node):
        log("Visiting AssignmentFunction")

        # We don't need to check if the statement is correct as it was done before by the InterpreterType
        symbol = SymbolFunction(node.var_name, node.is_ref, value=self.visit(node.value_node), type=None)
        # the type is None as we don't use types in InterpreterValue
        
        self.memory_table.define(node.var_name, symbol)
        show(colors.YELLOW, f"Assigning Variable: {node.var_name} with type {symbol.type}, isref = {symbol.isref}", colors.ENDC)
    """

    def visit_AssignmentFunction(self, node):
        log("Visiting AssignmentFunction")
        # We don't need to check if the statement is correct as it was done before by the InterpreterType

        # Id of the function, used to store it in the memory table
        function_id = node.var_name
        # AST node representing the body of the function
        function_node = node.content_node
        # List of the parameters id
        parameters_list = function_node.parameters_list

        # We don't use the types as this was done in interpreter_type
        parameters_types_list = [None]*len(parameters_list)
        # The content of the parameters is, at the opposite of the parameters types, a value that 
        # - do not need to be stored in the symbol as it is not used elsewhere that when the meory table of the function is used
        # - keep changing and is stored in the function memory table

        function_symbol = SymbolFunction(function_id, parameters_list, [], function_body_node=function_node.function_body_node, result_type=None, is_recursive=node.is_recursive)
        
        self.memory_table.define(function_id, function_symbol)
        
        show(colors.YELLOW, f"Assigning function: {function_id} with parameters: {parameters_list} and function_body_node:{function_node.function_body_node}", colors.ENDC)

    def visit_Reassignment(self, node):
        log("Visiting Reassignment")

        # We don't need to check if the statement is correct as it was done before by the InterpreterType
        # We just change the symbol value, we know it's a defined and mutable variable
        self.memory_table.get(node.var_name).value = self.visit(node.new_value_node)
    
    def visit_Variable(self, node):
        log("Visiting Variable")
        log(f"Searshing the variable {node.var_name} {node.get_content}")
        
        symbol = self.memory_table.get(node.var_name)

        if node.get_content:
            # InterpreterType checked the variable is mutable
            show(colors.YELLOW, f"Accessing content of mutable variable {node.var_name}", colors.ENDC)
            return symbol.value
        
        else:
            if symbol.isref:
                # We don't access the content of the mutable variable
                return ['ref', symbol.value]
            else:
                # The variable isn't mutable
                return symbol.value

    def visit_FunctionCall(self, node):
        log("Visiting visit_FunctionCall")
        log(f"Calling the function {node.var_name} with parameters list {node.arguments_nodes_list}")
        
        function_id = node.var_name

        # We don't need to check if the function is already defined or is indeed a function.
        # We don't need to check the amount of arguments/parameters is the same
        # It was done in InterpreterType
        function_symbol = self.memory_table.get(function_id)
        
        # List of the id of the expected arguments
        parameters_list = function_symbol.parameters_list
        # List of the arguments that were passed in the call
        given_arguments_nodes_list = node.arguments_nodes_list

        # 1 We create a new memory table
        mt = MemoryTable(function_id, self.memory_table.scope_level + 1, self.memory_table)
        
        # 2 We define each parameter with its given as argument value
        for i in range(len(parameters_list)): 
            parameter_id = parameters_list[i]
            argument_node = given_arguments_nodes_list[i]

            # We get its value by visiting its node
            argument_value = self.visit(argument_node)

            argument_symbol = SymbolVariable(parameter_id, isref=False, value=argument_value, type=None)

            mt.define(parameter_id, argument_symbol)
        
        # 3 If the function is recursive, we add this function as an object of its own memory table
        if function_symbol.is_recursive:
            mt.define(function_id, function_symbol)

        # 4 We use this memory table
        self.memory_table = mt

        # 5 We can then execute the body of the function
        function_body_node = function_symbol.function_body_node
        print("Visiting function body node")
        function_result = self.visit(function_body_node)

        # 6 We restore the old memory table and return the result
        self.memory_table = self.memory_table.following_table
        return function_result

    def visit_PrintInt(self, node):
        print(colors.BOLD, self.visit(node.node), colors.ENDC)
    
    def visit_PrintString(self, node):
        print(colors.BOLD, self.visit(node.node), colors.ENDC)
    
    def visit_Loop(self, node):
        while self.visit(node.boolean_node):
            self.visit(node.block_node)
    
    def visit_ConditionalStatement(self, node):
        if self.visit(node.condition_node):
            return self.visit(node.then_node)
        else:
            return self.visit(node.else_node)
    
    def visit_UnitNode(self, node):
        return None