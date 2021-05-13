# TODO

Fixer le loggin et les erreurs raising
Documenter le parsing de fonctions. Quels sont les grammaires? Quels sont les nodes AST utilisées? (un peu bizarre)

# Étapes suivantes
 * Ajouter des structures de donnée : commencer par des tuples
 * Nettoyer la gestion de la mémoire
 * Nettoyer les nodes AST

# TODO

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

Supporter les fonctions récurrentes
TODO: rename content_node -> function_node

* Mettre en place le parsing de fonctions

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

# Amelioration finales / Production
* Utiliser une enum pour les TokenType