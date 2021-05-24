# Grammaire
```EBNF
program:    block? SEMI SEMI

block:      # TODO: Remove @LPARENRPAREN
            #LPAREN block? RPAREN
            pres0

pres0:      PLUS block
            MINUS block
            pres1 ((PLUS | MINUS | CONCATENATE) pres1)*
            
pres1:      pres2 (MOD pres2)*

pres2:      pres3 (MUL pres3)*

pres3:      pres4 ((EQUAL | DIFFERENT) pres4)*              => Enchaîner des EQUAL lèvera généralement une erreur de type

pres4:      code ((BOOLEANCONJUNCTION | BOOLEANDISJUNCTION) code)*

code:       LPAREN block? RPAREN                            => On vérifie l'absence de RPAREN avant de chercher le block 
                                                               LPAREN RPAREN doit renvoyer UnitNode
                                                               block() renverra NothingNode
            sequence    ->(BEGIN)
            command

sequence:   BEGIN END
            BEGIN block (SEMI block)* END

command:    INT
            FLOAT
            STRING
            assignment_statement       ->(LET)
            WHILE block DO block DONE
            IF block THEN block (ELSE block)?
            PRINT_INT block
            PRINT_STRING block
            # TODO: REMOVE @LPARENRPAREN
            #LPAREN RPAREN              => Permet des arguments UNIT (UnitNode) lors des appels de fonction
            #                              Car id cherche des codes et non des block (problème avec 1 + 1)
            #                              LPAREN block RPAREN *should* not happen
            variable_statement         ->(ID|EXCLAMATION)
            nothing

assignment_statement:   LET assignment (AND assignment)* IN block
                        LET assignment (AND assignment)*                            => TODO: to implement

assignment:             REC? ID (ID|LPAREN RPAREN)+ EQUAL block                     => Currified function assignment
                        REC? ID EQUALS FUNCTION (ID|LPAREN RPAREN)+ ARROW block
                        REC? ID EQUALS REF? block                                   => The REC won't be used nor raise an    
                                                                                        error for non function assignment

variable_statement:     EXCLAMATION ID
                        ID REASSIGN block
                        ID (code != nothing)*     => Utilisé pour les appels de fonctions : 
                                                      Pas de code (Nothing node) = variable
                                                      Au moins un code = appel d'une fonction avec argument
                                                      On utilise un code et non un bloc suite à un problème pour 1 + 1 interprété comme BinOp(Nothing, +, 1)
```

# AST nodes
Classes utilisées pour construire l'arbre.
> Une méthode de visite doit être définie pour un interpréteur pour toutes ces classes.

```
Program(block_node)
Block(node)
Sequence(commands_list)

# Pres
BinOp(left_node, op_token, right_node)
UnaryOp(op_token, right_node)

# Commands
Num(value, type)
AssignmentStatement(assignments_list, block_node)
Loop(boolean_node, block_node)
PrintInt(node)
PrintString(node)

# AssignmentStatement
Assignment(var_name, isref, value_node)

# Variable
Reassignment(id, new_value_node)
Variable(var_name, get_content)

# Miscellaneous
UnitNode()          # Used to represent a portion of code that
                    # should not be executed ("begin end", "()")

Function(parameter_id, content_node)
```

# Precédence des opérateurs
Par ordre décroissant de précédence :
```
&& ||
= <> 
*
mod
+ - ^
```

# Fonctions

Deux syntaxes
```EBNF
let a = fun PARAMS -> BLOCK         <implémenté/>
let a PARAMS = BLOCK
```

grammar:
```
Fonction:
LET ID (ID)+ EQUALS BLOCK
LET ID EQUALS (FUN|FUNCTION) (ID)* ARROW BLOCK          <implémenté/>

LET ID EQUALS BLOCK
```
TODO: Créer un type `FUN ID* -> BLOCK` 

Appel de fonctions A TESTER
C'est bien left associatif
```
ID BLOCK==UnitNode -> variable
ID BLOCK (BLOCK)* BLOCK==UnitNode -> nested functionCall
```