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

        # Used to generate new quote type ('a, 'b...)
        self.quote_index = 0
    
    def _init_base_types(self):
        print("Initiating base type")
        for identifier in BUILTIN_TYPES:
            symbol = BUILTIN_TYPES[identifier]
            self.memory_table.define(symbol.id, symbol)
    
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
            if type != BUILTIN_TYPES["unit"]:
                warning(f"{command_node} is of type {type} instead of unit in sequence")
        # The type of a sequence is the type of its last element
        return self.visit(node.commands_list[-1])

    def visit_Num(self, node):
        log("Visiting Num")
        # Can be INT, FLOAT, STRING
        # node.type is set by the Lexer and countain a string like INT. We need to convert it to a symbol
        return BUILTIN_TYPES[node.type.lower()]
    
    def visit_BinOp(self, node):
        log("Visiting BinOp")
        # Integer operations
        # The left and right nodes should be of type int
        if node.op_token.type in (PLUS_INT, MINUS_INT, MUL_INT, DIV_INT):
            left_type = self.visit(node.left_node)
            if left_type != BUILTIN_TYPES["int"]:
                error(f"Left node {node.left_node} is of type {left_type} instead of INTEGER in Binary Operation {node.op_token.type}")
            right_type = self.visit(node.right_node)
            if right_type != BUILTIN_TYPES["int"]:
                error(f"Right node {node.right_node} is of type {right_type} instead of INTEGER in Binary Operation {node.op_token.type}")
            return BUILTIN_TYPES["int"]
        # Boolean operation
        # The left and right nodes should have the same type
        if node.op_token.type in (EQUALS, DIFFERENT):
            left_type = self.visit(node.left_node)
            right_type = self.visit(node.right_node)
            if left_type != right_type:
                error(f"Left node {node.left_node} is of type {left_type} and right node {node.right_node} of type {right_type} which are not the same in Boolean Binary Operation {node.op_token.type}")
            return BUILTIN_TYPES["bool"]
        
        warning("Undefined operation BinOp", node.op_token.type)
        return BUILTIN_TYPES["unit"]

    def visit_UnaryOp(self, node):
        log("Visiting Unary Op")
        if node.op_token.type in (PLUS_INT, MINUS_INT):
            type = self.visit(node.right_node)
            if type != BUILTIN_TYPES["int"]:
                error(f"Unary node {node.right_node} is of type {type} instead of INTEGER in Unary Operation {node.op_token.type}")
            return BUILTIN_TYPES["int"]
        warning("Undefined operation UnaryOp")
        return BUILTIN_TYPES["unit"]
    
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
            if assignement_type != BUILTIN_TYPES["unit"]:
                warning(f"{assignment_node} is of type {type} instead of unit in assignment statement")
        
        result_type = self.visit(node.block_node)

        if create_a_new_memory_table:
            # After evaluating the block, we need to remove the corresponding memory table
            self.memory_table = self.memory_table.following_table
        
        #TODO: remove memory_table print
        print(self.memory_table)

        return result_type
    
    def visit_AssignmentVariable(self, node):
        log("Visiting AssignmentVariable")
        # We need to check a variable is not already defined as a local variable in the current memory table with the same id.
        if not self.memory_table.isdefined(node.var_name, look_following_table=False):
            # We create a new symbol corresponding to the variable, the value is None as we are only searching the type
            symbol = SymbolVariable(node.var_name, node.is_ref, value=None, type=self.visit(node.value_node))
            self.memory_table.define(node.var_name, symbol)
            show(colors.CYELLOW, f"Assigning: {node.var_name} with type {symbol.type}", colors.ENDC)
            # An assignement is of type UNIT
            return BUILTIN_TYPES["unit"]
        else:
            error("Memory error:", node.var_name, "is already defined in the current memory table")
            raise SyntaxError("Variable already defined")
    
    def visit_AssignmentFunction(self, node):
        log("Visiting AssignmentFunction")
        # We need to check a variable is not already defined as a local symbol in the current memory table with the same id.
        if not self.memory_table.isdefined(node.var_name, look_following_table=False):
            # We create a new symbol corresponding to the function

            # Construire la liste de parametres
            # Executer le corps qui se chargera de l'inference de types
            # Construire le symbole representant la fonction et l'enregistrer
            
            # 1 We get the data of the function, it will be used to create the symbol
            # node is an object of AssignementFunction
            function_id = node.var_name
            function_node = node.content_node

            parameters_list = function_node.parameters_list

            # 2 We create a new memory table for the function body, it will be used to determine parameters type
            mt = MemoryTable(function_id, self.memory_table.scope_level + 1, self.memory_table)
            
            # List of currently quote types passed for the recursive definition of the function
            # TODO: improve this system
            rec_param_type_list = []

            # We need to lock **all** quote object after the function definition, before its call
            # Every time we will create a such symbole we will add it here
            used_quote_symbol_objects = []

            for parameter_id in parameters_list:
                # We add each parameters to the memory table
                # By default each type is defined to a quote type
                if parameter_id is None:
                    # The parameter can be an UNIT parameter. 
                    # We don't need to add it to the memory table
                    # This happen for example when we declare `let f = fun () -> 1`

                    # We add the type of the parameter to the list
                    rec_param_type_list.append(BUILTIN_TYPES["unit"])

                    pass
                else:
                    quote_symbol = SymbolQuoteType(self.quote_index, resolved_type=None)
                    used_quote_symbol_objects.append(quote_symbol)
                    self.quote_index += 1
                    # self.quote_index contain the index of the next to use quote numeric_identifier
                    
                    parameter_symbol = SymbolVariable(parameter_id, isref=False, value=None, type=quote_symbol)

                    # We add the current type of the parameter to the list
                    rec_param_type_list.append(quote_symbol)
                    
                    mt.define(parameter_id, parameter_symbol)
            
            if node.is_recursive:
                # We add the function as an item of it's own memory table

                rec_return_type_quote_symbol = SymbolQuoteType(self.quote_index, resolved_type=None)
                used_quote_symbol_objects.append(rec_return_type_quote_symbol)
                self.quote_index += 1

                rec_function_symbol = SymbolFunction(function_id, parameters_list, rec_param_type_list, function_node.function_body_node, rec_return_type_quote_symbol, is_recursive=True)
                mt.define(function_id, rec_function_symbol)
                # TODO: check if the returned type of the function does correspond to the deducted type in the recursive call
            
            self.memory_table = mt
            
            # 3 We determine the type of the result. Parameters type will be determined too
            result_type = self.visit(function_node.function_body_node)
            
            # 4 The parameters types should now be determined. We can create the list parameters_types_list.
            parameters_types_list = []
            for parameter_id in parameters_list:
                if parameter_id is None:
                    # The parameter is of type UNIT
                    parameter_type = BUILTIN_TYPES["unit"]
                else:
                    parameter_symbol = mt.get(parameter_id)
                    parameter_type = parameter_symbol.type
                parameters_types_list.append(parameter_type)
                # The list parameters_types_list countain the respectives types of parameters_list

            #TODO:REMOVE
            print("Determining function declaration parameters")
            print(self.memory_table)

            # 4 We remove the memory table and define the function symbol
            self.memory_table = self.memory_table.following_table
            
            function_symbol = SymbolFunction(function_id, parameters_list, parameters_types_list, function_node.function_body_node, result_type, is_recursive=node.is_recursive)
            self.memory_table.define(function_id, function_symbol)

            print("Dfining function")
            print(self.memory_table)
            
            show(colors.CYELLOW, f"Assigning function: {function_id} with parameters: {list(zip(parameters_list, parameters_types_list))} result type {result_type} and function_body_node:{function_node.function_body_node}", colors.ENDC)
            # An assignement is of type UNIT
            
            # Type is of the form "int -> string -> string"
            function_object_type = ""
            for parameter_type in parameters_types_list:
                function_object_type += str(parameter_type)
                function_object_type += " -> "
            function_object_type += str(result_type)

            # We can now lock used quote symboles object
            for quote_symbole in used_quote_symbol_objects:
                quote_symbole.lock()
            
            print("function_object_type", function_object_type)


            return BUILTIN_TYPES["unit"]
        else:
            error("Memory error:", node.var_name, "is already defined in the current memory table")
            raise SyntaxError("Variable already defined")

    def visit_Reassignment(self, node):
        log("Visiting Reassignment")
        if self.memory_table.isdefined(node.var_name):
            symbol = self.memory_table.get(node.var_name)
            if symbol.symbol_type != "Variable":
                error("It's not a variable")
                raise SyntaxError("It's not a variable")
            else:
                if symbol.isref:
                    # The variable can be reassigned
                    value_type = self.visit(node.new_value_node)
                    if symbol.type != value_type:
                        error(f"New value node {node.new_value_node} is of type {value_type} instead of {symbol.type} in Reassignment of {node.var_name}")
                    # A reassignement is of type UNIT
                    return BUILTIN_TYPES["unit"]
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
                    return ['ref', symbol.type]                 #TODO: use a symbol
            else:
                if node.get_content:
                    # The variable is not mutable and we are accessing its value (!var)
                    raise SyntaxError("Variable not mutable but its content is accessed")
                else:
                    # The variable is not mutable
                    show(colors.CYELLOW, f"Accessing content of variable {node.var_name}", colors.ENDC)
                    return symbol.type

    def visit_FunctionCall(self, node):
        log("Visiting visit_FunctionCall")
        log(f"Calling the function {node.var_name} with parameters list {node.arguments_nodes_list}")
        
        function_id = node.var_name
        given_arguments_nodes_list = node.arguments_nodes_list

        # We check the symbol is defined before accessing it
        if not self.memory_table.isdefined(function_id):
            raise MemoryError(f"{function_id} is not defined in function call")
        
        function_symbol = self.memory_table.get(function_id)

        # We check it's a function and thus a callable object
        if not function_symbol.symbol_type == "Function":
            raise SyntaxError(f"function_id is not callable in function call")
        
        # We need to check the type of each parameter correspond to the type of arguments given in the call
        parameters_types_list = function_symbol.parameters_types_list

        if not len(parameters_types_list) == len(given_arguments_nodes_list):
            raise SyntaxError(f"Invalid arguments given in function call. Expected {len(given_arguments_nodes_list)} arguments got {len(parameters_types_list)}")
        
        # We need to lock **all** quote object after the function definition, before its call
        # Every time we will create a such symbole we will add it here
        used_quote_symbol_objects = []
        # We create a dictionnary that will store each expected type and the generated associated type
        quote_type_correspondance = {}

        for i in range(len(parameters_types_list)):
            expected_parameter_type = parameters_types_list[i].get_symbol_type() # Return the resolved Type or the unresolved QuoteType

            # If the expected parameter is a quote type, it should have been locked in the function definition.
            # Indeed, we don't want the function call to modify the function definition (ex: `let f a = a in begin f 1; f 'i' end;;` is valid)
            # We still need to be able to resolve the type in the function call
            # (ex: `let f a b = if true then a else b in f 1 'a';;` should raise an error as type a and b should be the same)
            if expected_parameter_type.symbol_type == "QuoteType":
                # It's an unresolved QuoteType
                # It should be locked. To be able to be able to resolve it, we need to create a new one that will be stored in the dict quote_type_correspondance
                if expected_parameter_type.numeric_id in quote_type_correspondance:
                    # A quote type has already been created, we will use this one
                    expected_parameter_type = quote_type_correspondance[expected_parameter_type.numeric_id]
                else:
                    # We create a new quote type
                    quote_symbol = SymbolQuoteType(self.quote_index, resolved_type=None)
                    used_quote_symbol_objects.append(quote_symbol)
                    self.quote_index += 1
                    # self.quote_index contain the index of the next to use quote numeric_identifier

                    #We store this type is the dictionnary and use it
                    quote_type_correspondance[expected_parameter_type.numeric_id] = quote_symbol
                    expected_parameter_type = quote_symbol

            # The actual type is determined by calling visit method on the AST node
            actual_type_given = self.visit(given_arguments_nodes_list[i])

            # The following comparison check the types match but also
            # Resolve quote types. See SymbolQuoteType class in baseclass.py
            if not expected_parameter_type == actual_type_given:
                raise TypeError(f"Invalid argument in function call. Expected argument of type {expected_parameter_type} got {actual_type_given}")
            
        # The result_type should have been resolved by the previous comparaisons
        result_type = function_symbol.result_type.get_symbol_type()

        # If the return type is a quote type, we need to replace it by the local one that has been created previously
        # and should be stored in quote_type_correspondance
        if result_type.symbol_type == "QuoteType":
            if result_type.numeric_id in quote_type_correspondance:
                # It has already be created. We use this one
                result_type = quote_type_correspondance[result_type.numeric_id]
            else:
                # If a local type has not been created, that should mean the type had to be resolved in the function definition
                warning("The return quote type was be resolved in function call, it should have been resolved in the function definition")

        # We lock all quote symbol.
        for quote_symbol in used_quote_symbol_objects:
            quote_symbol.lock()
        
        return result_type

    def visit_PrintInt(self, node):
        type = self.visit(node.node)
        if type != BUILTIN_TYPES["int"]:
            error(f"Got {type} instead of INT in PrintInt")
        return BUILTIN_TYPES["unit"]

    def visit_PrintString(self, node):
        type = self.visit(node.node)
        if type != BUILTIN_TYPES["string"]:
            error(f"Got {type} instead of STRING in PrintString")
        return BUILTIN_TYPES["unit"]
    
    def visit_Loop(self, node):
        bool_type = self.visit(node.boolean_node)
        if bool_type != BUILTIN_TYPES["bool"]:
            error(f"Boolean_node is of type {bool_type} instead of BOOL in Loop")
        block_type = self.visit(node.block_node)
        if block_type != BUILTIN_TYPES["unit"]:
            warning(f"Block node is of type {block_type} instead of UNIT in Loop")
        return BUILTIN_TYPES["unit"]
    
    def visit_ConditionalStatement(self, node):
        condition_type = self.visit(node.condition_node)
        if condition_type != BUILTIN_TYPES["bool"]:
            error(f"Condition_node is of type {condition_type} instead of BOOL in ConditionalStatement")
        then_type = self.visit(node.then_node)
        else_type = self.visit(node.else_node)
        if then_type != else_type:
            error(f"Two then block is of type {then_type} but else block of type {else_type} in ConditionalStatement")
        return then_type
    
    def visit_UnitNode(self, node):
        return BUILTIN_TYPES["unit"]