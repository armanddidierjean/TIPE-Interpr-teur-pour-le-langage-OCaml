# Ressources, cours and articles

> **Surlignage**
> Jaune : se renseigner
> Violet : connaissances générales
> Vert : propre à ce projet

**Ressources list**
https://github.com/sdmg15/Best-websites-a-programmer-should-visit#building-a-simple-compilerinterpreter

**Books**
[The C Programming Language](https://en.wikipedia.org/wiki/The_C_Programming_Language)

[Microsoft - The Implementation of Functional Programming Languages](https://www.microsoft.com/en-us/research/publication/the-implementation-of-functional-programming-languages/) <téléchargé/>

[Crafting Interpreters](http://craftinginterpreters.com/contents.html) <Excellent>
   - Page http://craftinginterpreters.com/a-map-of-the-territory.html

**OCaml language** : références officielles
https://caml.inria.fr/pub/docs/manual-ocaml/language.html

# Thématiques à explorer

Polymorphisme : [Polymorphism](https://en.wikibooks.org/wiki/Introduction_to_Programming_Languages/Polymorphis)
Pattern matching
Predictive parser

# Idées développement
 * Voir [Avancée novembre](Avancée-novembre.md)

 * Ajouter des structures de donnée : commencer par des tuples
 * Memory management
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

# Idées exposé
 * Voir [Avancée novembre](Avancée-novembre.md)
 
 * Expliquer la stratégie de programmation
    - Choix de Python comme langage de base
    - Choix de OCaml comme langage à interpréter
    - Utilisation de POO pour avoir des modules indépendant
    - Utilisation de GIT pour le visionnement du projet
    - Création de tests dès le debut du projet : "integration test"

 * Informations sur la précédence
    - Tableau / arbre de précédence des opérateurs
    - Petit exemple du problème : une situation d'ambiguïté
    > L'utilisation des fonctions `pres0`, `pres1`, `pres2`, `pres3` et `pres4` permet d'associer les éléments selon la précédence des opérateurs. Par exemple `1 + 2 * 2` sera interprété comme `1 + (2 * 2)`.