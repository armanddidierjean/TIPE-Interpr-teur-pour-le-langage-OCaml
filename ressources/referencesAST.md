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
                        REC? ID EQUALS REF? block                                   => The REC won't be used nor raise an error for nun function assignment

variable_statement:     EXCLAMATION ID
                        ID REASSIGN block
                        ID (code != nothing)*     => Utilisé pour les appels de fonctions : 
                                                      Pas de code (Nothing node) = variable
                                                      Au moins un code = appel d'une fonction avec argument
                                                      On utilise un code et non un bloc suite à un problème pour 1 + 1 interprété comme BinOp(Nothing, +, 1)
```