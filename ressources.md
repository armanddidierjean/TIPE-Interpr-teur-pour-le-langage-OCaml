https://en.wikipedia.org/wiki/The_C_Programming_Language

# Ressources et documents


The OCaml language
https://caml.inria.fr/pub/docs/manual-ocaml/language.html

Polymorphisme

Patern matching

Microsoft
https://www.microsoft.com/en-us/research/publication/the-implementation-of-functional-programming-languages/ -> Téléchargé

Predictive parser


# Rendez-vous novembre -> voir avancée.md
Plan prévisionnel
 * Généralité sur l'execution des langages de programmation
    Compilateur, interpréteur. Exemples de langages courants.
 * Choix techniques choisit
    Maintenant qu'on a une idée de ce qui existe, que va-t-on concrètement faire.
    Executer un langage proches de OCaml. 
        Pourquoi ?
            Langage intéressant, à la syntaxe, subtile mais facilement parsable
            Profondément typé
            En cours d'apprentissage pour la prépa, donc cela permet de se perfectionner, et de comprendre son fonctionnement
 * Mise en place des outils utilisé
    EBNF et grammaire
    Étapes de l'interpréteur
    Détail d'une execution
 * Approfondissement de champs sélectionné
    A détailler après les expérimentations en question


État actuel
 * Production d'arbres, non optimisés
 * Execution de ceux-ci
 * Gestion de scopes
 * Appels de fonctions


Projet
 * Gérer les erreurs
 * Optimiser l'arbre obtenu
    Il y a plein de noeuds inutiles
    Se renseigner sur certaines méthodes d'optimisation
 * Utiliser des structures de données plus basiques
    Pour le moment j'utilise des instances de classes python et des dictionnaires
 * Implementer des objets plus complexes
    ex listes, tableaux, tuples, custom type
    OBJECTIF: implementer en Python ces objets
    Permettra d'executer des programmes plus complexes (ex programmation dynamique)
 * Se renseigner sur d'autres méthodes de parsing et sur les implementations de langages de références
    Il n'est pas prévu de les utiliser
 * Comparer cet interpréteur avec celui officiel pour OCaml
    Quels sont les choix différents ? grammaire, étapes ?
 * Outils de détection d'erreur et de corrections de codes

------------------------------------------------------------------------------------------------------

Jaune : se renseigner
Violet : connaissances générales
Vert : propre à ce projet

# Idées
 * Ajouter des structures de donnée : commencer par des tuples
 * Memory management
 * Se renseigner sur les https://en.wikibooks.org/wiki/Introduction_to_Programming_Languages/Polymorphis
 * Sélectionner des structures de données performantes
 * Optimiser un arbre
    - https://en.wikipedia.org/wiki/Static_single_assignment_form
    - Éliminer les parenthèses en trop
    - Arrêter de placer des blocs partout
    - Supprimer les calcules mathématiques qui peuvent se faire lors de la compilation
 * Traiter un arbre de données
    - Obtenir des infos sur celui ci

 * Lire l'interpréteur de python: Cython

 * Utiliser l'interpréteur de manière intéressante
    - Fibonacci
    - FAIRE DE LA PROGRAMMATION DYNAMIQUE

 * Lire la liste des chapitres utiles https://compilers.iecc.com/crenshaw/tutor1.txt

 * Générer du langage machine

 * Expliquer la stratégie de programmation
    - Choix de Python comme langage de base
    - Choix de OCaml comme langage à interpréter
    - Utilisation de POO pour avoir des modules indépendant
    - Utilisation de GIT pour le visionnement du projet
    - Création de tests dès le debut du projet : "integration test"


-----

Add a isref = False in function symbol and remove variable check in reassignement
remove id from Function AST node

Check Variable call of a function don't raise an error because of the get content check


self.block do not return a block but self.code does!

Test non fonctionnel pour parser les declarations de fonctions
```
assignment:             ID EQUALS FUNCTION function_body
                        ID EQUALS REF? block

function_body:          (LPAREN RPAREN)|ID) (ARROW block|function_body)
```

# Project
* Utiliser une enum pour les TokenType
* Mettre en place le parsing de fonctions

Supporter les fonctions récurrentes
TODO: rename content_node -> function_node

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


ID = None <=> UNIT for the strings

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
            IF block THEN block (ELSE block)?
            PRINT_INT block
            PRINT_STRING block
            LPAREN RPAREN              => Permet des arguments UNIT (UnitNode) lors des appels de fonction
                                          Car id cherche des codes et non des block (problème avec 1 + 1)
                                          LPAREN block RPAREN *should* not happen
            variable_statement         ->(ID|EXCLAMATION)
            nothing

assignment_statement:   LET assignment (AND assignment)* IN block

assignment:             ID EQUALS FUNCTION (ID|LPAREN RPAREN)+ ARROW block
                        ID EQUALS REF? block

variable_statement:     EXCLAMATION ID
                        ID REASSIGN block
                        ID (code != nothing)*     => Utilisé pour les appels de fonctions : 
                                                      Pas de code (Nothing node) = variable
                                                      Au moins un code = appel d'une fonction avec argument
                                                      On utilise un code et non un bloc suite à un problème pour 1 + 1 interprété comme BinOp(Nothing, +, 1)
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
