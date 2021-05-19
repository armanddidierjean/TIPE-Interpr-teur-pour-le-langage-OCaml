# TODO

Est-ce que nous utiliserions cette stratégie pour s'assurer d'un string est fermé ? [string / crafting interpreters](http://craftinginterpreters.com/scanning.html#string-literals)
Ajouter un `.isNotEnded` in the Lexer

Modifier les noms des keywords
      case '*': addToken(STAR); break; 
      case '(': addToken(LEFT_PAREN); break;
      case ')': addToken(RIGHT_PAREN); break;
      case '{': addToken(LEFT_BRACE); break;
      case '}': addToken(RIGHT_BRACE); break;

Mémoriser dans le Token la position du token

Devrions nous utiliser des fonctions personnalisées pour la gestion des erreurs ? Cela permettrait d'afficher la ligne ainsi que sa position dans le code. Le mieux serait de passer au différents objets (Lexer, Parser, Interpreter) une classe qui implémente des fonctions d'affichage d'erreur (cela permettrait de les logger dans un fichier, les printer dans la console). Voir [Errors handling / crafting interpreters](http://craftinginterpreters.com/scanning.html#error-handling)

Indicate were errors happened during the lexing process by returning `self.current_pos` in the error

Ajouter un mot clef `not` qui attend un block booléen
Ajouter un `for i = 1 to 4 do block done`

We should create a function_type Symbole. Les types des paramètres seraient ainsi stockés dans le type de la fonction. La définition de la fonction met en oeuvres tous les types nécessaires. Son appel utiliserait les premiers types pour verifier que l'appel est bien typé. Le dernier élément serait utilisé comme élément de retour. Ce serait plus cohérent avec le stockage des valeurs de la fonction, dans une memory table.

Use a function `self.get_SymboleType()` pour les Symbole qui appellerait l'élément parent et le compléterai si besoin

Les symboles ont des classes spécifiques. On pourrait éventuellement utiliser des wrappers. Ex: `Variable(id, ref)` -> `Ref(Variable(Identifier(Id)))` ou `Function(name, [param], rec)` -> `Rec(Function(Identifier(name), [Identifier(name)]))`

Fixer le loggin et les erreurs raising
Documenter le parsing de fonctions. Quels sont les grammaires? Quels sont les nodes AST utilisées? (un peu bizarre)

Difference entre UnitNode and NothingNode. None is also used in function parameters' lists
 - `code` LPAREN RPAREN         -> UnitNode()
 - `block` LPAREN RPAREN        -> NothingNode
 - `sequence` BEGIN END         -> UnitNode()

L'AST node Block est inutile et peut dans la majorité des cas être éliminée

Rename l'AST node Num() car elle supporte des STRING and FLOAT, INT

Use only one AST for PrintInt and PrintString with a type?

Les Unary Operator créent un phénomène d'associativités à droite `-1+1` est interprété comme `-(1+1)`

# Étapes suivantes
 * Ajouter des structures de donnée : commencer par des tuples
 * Nettoyer la gestion de la mémoire
 * Nettoyer les nodes AST

# TODO

Add a isref = False in function symbol and remove variable check in reassignment
remove id from Function AST node

Check Variable call of a function don't raise an error because of the get content check


self.block do not return a block but self.code does!

Test non fonctionnel pour parser les declarations de fonctions
```
assignment:             ID EQUALS FUNCTION function_body
                        ID EQUALS REF? block

function_body:          (LPAREN RPAREN)|ID) (ARROW block|function_body)
```

Supporter les fonctions récurrentes
TODO: rename content_node -> function_node

* Mettre en place le parsing de fonctions

# TODO
Permettre d'avoir des elements vide: LPAREN RPAREN ou BEGIN END
* Concatenate
* If statement
* fail_withs

Créer plusieurs classes de symboles:
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

# Amelioration finales / Production
* Utiliser une enum pour les TokenType
