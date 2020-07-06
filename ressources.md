
# TODO
Permettre d'avoir des elements vide: LPAREN RPAREN ou BEGIN END
Concatenate

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
            assignment_statement ->(LET)
            WHILE block DO block DONE
            PRINT_INT block
            PRINT_STRING block
            variable_statement

assignment_statement:  LET assignment (AND assignment)* IN block

assignment:            ID EQUALS REF? block

variable_statement:     EXCLAMATION ID
                        ID REASSIGN block
                        ID
```

L'utilisation des fonctions `pres0`, `pres1`, `pres2`, `pres3` et `pres4` permet d'associer les éléments selon la précédence des opérateurs. Par exemple `1 + 2 * 2` sera interpreté comme `1 + (2 * 2)`.

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
```
