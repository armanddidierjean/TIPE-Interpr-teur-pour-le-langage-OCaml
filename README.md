# TIPE - Mise au point d’un interpréteur pour le langage OCaml

## Présentation du projet

Projet réalisé au cours de mon année de classe préparatoire MP\*, dans le cadre de l'épreuve de Travail d'Initiative Personnel Encadré (TIPE).

Mon travail porte sur l'exécution de programmes informatique, en particulier de programmes écrits dans le langage OCaml.

> [Un langage est un] ensemble de symboles et de règles permettant de combiner ces symboles afin de donner des instructions à un ordinateur.
>
> - Centre National de Ressources Textuelles et Lexicales

## Principaux objectifs

Ce projet a pour objectif la compréhension du fonctionnement des langages de programmation, en particulier des langages interprétés.

Nous cherchons ensuite à identifier les spécificités du langage OCaml dans l'objectif de construire une grammaire adapté à celui-ci ([grammaire construite](./ressources/references.md)).

Finalement le projet a permis d'implémenter un interpréteur et de le tester.

![](./images/Fonctionnement%20interpr%C3%A9teur.png)
_Schéma présentant le fonctionnement de l'interpréteur_

## Principaux résultats

Nous pouvons déterminer le type et les résultats de programmes écrits dans le langage OCaml.

```ocaml
let rec factorielle = fun n ->
    if n = 1
		then 1
    	else n * factorielle (n-1)
	in factorielle 6;;
```

L'utilisation du langage Python pour l'implémentation impose une rapidité limitée et une utilisation conséquente de mémoire. Elle permet en revanche d'utiliser cet interpréteur OCaml sur des machines ne le supportant pas nativement, telle une calculatrice graphique.

| ![](./images/Omega%20value.png) | ![](./images/Omega%20value.png) |
| ------------------------------- | ------------------------------- |

_Résultats obtenus sur une calculatrice Numworks avec le framework [Omega](https://github.com/Omega-Numworks/Omega)_
