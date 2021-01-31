# Project
* Utiliser une enum pour les TokenType
* Mettre en place le parsing de fonctions

# Fonctions

Deux syntaxes
```
let a = fun PARAMS -> BLOCK
let a PARAMS = BLOCK
```

grammar:
```
Fonction:
LET ID (ID)+ EQUALS BLOCK
LET ID EQUALS (FUN|FUNCTION) (ID)* ARROW BLOCK

LET ID EQUALS BLOCK
```
TODO: Creer un type `FUN ID* -> BLOCK` 

Appel de fonctions A TESTER
C'est bien left associatif
```
ID BLOCK==UnitNode -> variable
ID BLOCK (BLOCK)* BLOCK==UnitNode -> nested functionCall
```

# TODO
Permettre d'avoir des elements vide: LPAREN RPAREN ou BEGIN END
* Concatenate
* If statement
* fail_withs

Creer plusieurs classes de symboles:
    var (id, value, type, isref)
    type (id, type)
    function(id, formal_params[Symbole-var], type)


Init base type

Call main toplevel

Rename isdefined -> is_defined
isref -> is_ref 
Ou dans l'autre sens


Supporter les couples

# Nouvelle Grammaire
Problème : l'operation 2 * 2 + 2 était associée comme ceci : 2 * (2 + 2) ou (2 + 2) est un block

# Precedence

# Ressources
## Grammaire
```EBNF
program:    block? SEMI SEMI

block:      LPAREN block? RPAREN
            pres0

pres0:      PLUS block
            MINUS block
            pres1 ((PLUS | MINUS | CONCATENATE) pres1)*
            
pres1:      pres2 (MOD pres2)*

pres2:      pres3 (MUL pres3)*

pres3:      pres4 (EQUAL | DIFFERENT) pres4

pres4:      code ((BOOLEANCONJUNCTION | BOOLEANDISJUNCTION) code)*

code:       sequence    ->(BEGIN)
            command

sequence:   BEGIN END
            BEGIN block (SEMI block)* END

command:    INT
            FLOAT
            STRING
            assignment_statement       ->(LET)
            WHILE block DO block DONE
            PRINT_INT block
            PRINT_STRING block
            variable_statement         ->(ID|EXCLAMATION)
            nothing

assignment_statement:   LET assignment (AND assignment)* IN block

assignment:             ID EQUALS FUNCTION (ID|LPAREN RPAREN)+ ARROW block
                        ID EQUALS REF? block

variable_statement:     EXCLAMATION ID
                        ID REASSIGN block
                        ID (block != nothing)*     => Utilisé pour les appels de fonctions : 
                                                         Pas de block = variable
                                                         Au moins un block = appel d'une fonction (avec un argument)
```

L'utilisation des fonctions `pres0`, `pres1`, `pres2`, `pres3` et `pres4` permet d'associer les éléments selon la précédence des opérateurs. Par exemple `1 + 2 * 2` sera interprété comme `1 + (2 * 2)`.

## Precédence des opérateurs
Par ordre décroissant de précédence :
```
&& ||
= <> 
*
mod
+ - ^
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

# Micelianous
UnitNode()          # Used to represent a portion of code that
                    # should not be executed ("begin end", "()")

Function(parameter_id, content_node)
```
