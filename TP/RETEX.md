RETEX — Retour d’expérience sur le projet Triangulator

Introduction

Ce document présente mon retour d’expérience sur la réalisation du projet Triangulator dans le cadre du module Techniques de Test (M1 ILSEN). Je décris ici :

ce que j’ai bien réussi

les difficultés rencontrées

les décisions prises en cours de route

ce que je ferais autrement avec le recul

Ce que j’ai bien réussi ✔️ Mise en place d’une architecture claire
Le projet respecte la séparation en deux microservices :

PointSetManager

Triangulator

La communication entre eux est propre, cohérente et robuste.

✔️ Implémentation correcte de la représentation binaire

J’ai réussi à respecter à 100% le format binaire demandé dans le sujet, et à le tester de manière approfondie.

✔️ Tests complets et bien structurés

Unitaires : conversion binaire, validation, triangulation

Intégration : démarrage de microservices, flux complet binaire

Performance : mesures de triangulation et d’encodage/décodage

Le tout orchestré proprement via make.

✔️ API fonctionnelle et testable via un frontend interactif

Un petit frontend HTML permet de tester facilement la triangulation. Même si ce n’était pas demandé dans le sujet, cela a aidé à valider le comportement de l’API.

Difficultés rencontrées ❗ Représentation binaire
Le format binaire m’a demandé un temps d’adaptation, notamment pour :

gérer les floats 32 bits

éviter les erreurs de décodage

comparer avec pytest.approx

❗ Suppression de SciPy/NumPy

J’ai dû réécrire la triangulation “from scratch” car SciPy était interdit. Cela m’a obligé à comprendre un algorithme simple basé sur l’éventail (fan triangulation).

❗ Tests d’intégration avec plusieurs processus

Démarrer deux serveurs Flask dans des processus séparés pour les tests était un défi technique.

Ce que je ferais différemment 🔄 Préparer le plan de test plus tôt
Avec le recul, j’aurais dû rédiger le plan avant de coder la logique, comme le demande réellement la démarche "test first".

🔄 Séparer plus clairement les responsabilités

J’aurais pu mieux isoler :

la logique métier

la logique réseau

la logique binaire

🔄 Ajouter plus de tests adversariaux

Critères supplémentaires possibles :

flot de données corrompu

valeurs extrêmes

formats non conformes

Points d'amélioration possibles
Améliorer l’algorithme de triangulation pour un rendu plus "géométrique".

Ajouter une interface CLI pour trianguler des fichiers .bin.

Générer automatiquement la documentation dans une pipeline CI.

Conclusion
Ce projet m’a permis :

d’apprendre à tester un système distribué

d’utiliser un format binaire complexe

de comprendre l’importance des tests d’intégration réels

de structurer correctement un projet Python avec Makefile

Je suis satisfait du résultat final, parfaitement fonctionnel et conforme aux attentes.
