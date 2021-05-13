# Rendez-vous novembre
## Plan prévisionnel
 * Généralité sur l'execution des langages de programmation
    Compilateur, interpréteur. Exemples de langages courants.
 * Choix techniques choisit
    Maintenant qu'on a une idée de ce qui existe, que va-t-on concrètement faire.
    Executer un langage proches de OCaml. 
        Pourquoi ?
            Langage intéressant, à la syntaxe, subtile mais facilement parsable
            Profondément typé
            En cours d'apprentissage : perfectionnement, et comprendre son fonctionnement
 * Mise en place des outils utilisé
    EBNF et grammaire
    Étapes et détail d'une execution
 * Approfondissement de champs sélectionné
    A détailler après les expérimentations en question


## État actuel
 * Production d'arbres, non optimisés
 * Execution de ceux-ci

 * Gestion de scopes
 * Appels de fonctions


## Projet
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