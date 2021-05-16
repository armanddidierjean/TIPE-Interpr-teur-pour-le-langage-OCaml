# Grammaire

program:    block? SEMI SEMI                                    -> Program(`block`|UnitNode())

block:      # TODO: Remove @LPARENRPAREN
            #LPAREN block? RPAREN
            pres0                                               -> `pres0`

pres0:      PLUS block                                          -> UnaryOp(PLUS token, `block`)
            MINUS block                                         -> UnaryOp(MINUS token, `block`)
            pres1 ((PLUS | MINUS | CONCATENATE) pres1)*         -> BinOp(..., op_token, `pres1`) imbriqués
            
pres1:      pres2 (MOD pres2)*                                  -> BinOp(..., op_token, `pres2`) imbriqués

pres2:      pres3 (MUL pres3)*                                  -> BinOp(..., op_token, `pres3`) imbriqués

pres3:      pres4 ((EQUAL | DIFFERENT) pres4)*                  -> BinOp(..., op_token, `pres4`) imbriqués

pres4:      code ((BOOLEANCONJUNCTION | BOOLEANDISJUNCTION) code)*  -> BinOp(..., op_token, `code`) imbriqués

code:       LPAREN RPAREN                                       -> Block(UnitNode())
            LPAREN block? RPAREN                                -> Block(`block`)
            sequence    ->(BEGIN)                               -> Block(`sequence`)
            command                                             -> Block(`command`)             `BIZARRE`, retirer Block

sequence:   BEGIN END                                           -> UnitNode()
            BEGIN block (SEMI block)* END                       -> Sequence([`block`])

command:    INT                                                 -> Num(value, type)
            FLOAT                                               -> Num(value, type)
            STRING                                              -> Num(value, type)             `BIZARRE` rename Num
            assignment_statement       ->(LET)                  -> `assignment_statement`
            WHILE block DO block DONE                           -> Loop(boolean_node=`block`, block_node=`block`)
            IF block THEN block                                 -> ConditionalStatement(condition_node=`block`,
                                                                                        then_node=`block`,
                                                                                        else_node=UnitNode())
            IF block THEN block (ELSE block)?                   -> ConditionalStatement(condition_node=`block`,
                                                                                        then_node=`block`,
                                                                                        else_node=`block`)
            PRINT_INT block                                     -> PrintInt(`block`)
            PRINT_STRING block                                  -> PrintString(`block`)     `BIZARRE` use only one
            # TODO: REMOVE @LPARENRPAREN
            #LPAREN RPAREN              => Permet des arguments UNIT (UnitNode) lors des appels de fonction
            #                              Car id cherche des codes et non des block (problème avec 1 + 1)
            #                              LPAREN block RPAREN *should* not happen
            variable_statement         ->(ID|EXCLAMATION)       -> `variable_statement`
            nothing                                             -> NothingClass()

assignment_statement:   LET assignment (AND assignment)* IN block -> AssignmentStatement(assignments_list=[`assignment`],
                                                                                         block=`block`)
                        LET assignment (AND assignment)*          -> AssignmentStatement(assignments_list=[`assignment`],
                                                                                         block=UnitNode())

assignment:             REC? ID (ID|LPAREN RPAREN)+ EQUAL block
                                -> AssignmentFunction(name, Function(parameters_list=[identifier|None], 
                                                                     parameters_types_list=[None],
                                                                     function_body_node=`block`),
                                                      is_rec)
                        REC? ID EQUALS FUNCTION (ID|LPAREN RPAREN)+ ARROW block
                                -> AssignmentFunction(var_name, Function(parameters_list=[identifier|None], 
                                                                     parameters_types_list=[None],
                                                                     function_body_node=`block`),
                                                      is_rec)
                        REC? ID EQUALS REF? block       
                                -> AssignmentVariable(var_name, is_ref, `block`)

variable_statement:     EXCLAMATION ID          -> Variable(var_id, get_content=True)
                        ID REASSIGN block       -> Reassignment(var_id, `block`)
                        ID (code != nothing)+   -> FunctionCall(var_id, [`code`])
                        ID                      -> Variable(var_id, get_content=False)
```