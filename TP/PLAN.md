PLAN DE TESTS – Projet Triangulator

Objectif général
Ce plan de tests détaille comment valider un microservice appelé Triangulator, responsable du calcul de la triangulation d’un ensemble de points 2D à partir d’un identifiant fourni par le PointSetManager.
Les tests sont réalisés afin de garantir la précision des calculs, la robustesse du service face aux erreurs et autres défaillances externes, ses performances, ainsi que sa conformité à l’API définie.
 
1. Organisation générale des tests
Les tests sont répartis en trois grandes catégories :
•	Tests unitaires : Ils ont pour but de vérifier que les fonctions internes du microservice fonctionnent correctement, notamment celles qui effectuent les calculs, les conversions binaires et la validation. Ces tests seront menés avec le framework pytest.
•	Tests d’intégration : Ils permettront de tester la cohérence globale du service et la communication de l’API Flask avec les autres composants. Pour cela, pytest, le client de test Flask et unittest.mock pour simuler les dépendances externes seront utilisés.
•	Tests de performance : Ils serviront à mesurer les temps de traitement et la consommation de ressources du service. Ils seront aussi exécutés avec pytest, à l’aide de marqueurs spécifiques pour pouvoir les isoler pendant les campagnes de test.
 
2. Tests unitaires
Les tests unitaires concernent principalement le module de logique du projet (logic.py).
Chaque test suivra le modèle Arrange / Act / Assert et couvrira à la fois les cas normaux et les cas d’erreur.
Les tests incluront également des jeux de données synthétiques, comprenant :
•	des cas simples (triangle de base, carré divisé en deux triangles),
•	des cas limites (points alignés, très proches ou en double),
•	des entrées mal formées (fichier binaire incomplet, nombre de points invalide).
Cela permettra de couvrir un éventail complet de scénarios, y compris les situations inattendues.

 
3. Tests d’intégration
Les tests d’intégration porteront sur le service Flask exposé par le microservice Triangulator.
Ils visent à tester le bon enchaînement des appels et le comportement global du système.
Pour cela, le client de test Flask sera utilisé pour simuler des requêtes HTTP. Les dépendances externes (comme les appels à PointSetManager) seront remplacées par des objets simulés à l’aide du module unittest.mock.
Les tests devront couvrir la validation des codes HTTP, le contenu des réponses, ainsi qu’une gestion correcte des erreurs et exceptions.
 
4. Tests de performance
Les tests de performance mesureront la rapidité d’exécution des fonctions critiques comme la triangulation et les conversions binaires.
Ces tests ne seront pas systématiquement lancés pour ne pas ralentir les tests quotidiens.
Ils seront identifiés par le marqueur @pytest.mark.performance, permettant de les exclure ou de les exécuter séparément selon la commande utilisée.
Ces tests seront effectués sur des jeux de données de tailles variées (de quelques points à plusieurs milliers), afin d’évaluer la scalabilité de l’algorithme de triangulation. Des mesures précises de temps et de consommation mémoire pourront être enregistrées via des outils Python standard (time, tracemalloc, etc.).
 
5. Organisation des fichiers
La structure du dossier de tests sera la suivante :
tests/
├── unit/
│   ├── test_logic.py
│   └── test_encoding.py
├── integration/
│   └── test_api.py
└── performance/
    └── test_perf.py
Cette organisation facilitera la maintenance et permettra de distinguer clairement les différents types de tests.
Des fichiers de test supplémentaires (fixtures, données binaires exemples, mocks) pourront être placés dans un sous-dossier tests/data/ pour faciliter la réutilisation et améliorer la lisibilité des tests.
 
6. Méthodologie
Le développement suivra la méthode Test Driven Development (TDD), selon le cycle classique :
•	Red : écrire un test qui échoue.
•	Green : écrire le minimum de code pour le faire passer.
•	Refactor : améliorer le code sans casser les tests existants.
 
7. Objectif final
À la fin du projet, le microservice Triangulator devra :
•	Réussir l’ensemble des tests unitaires et d’intégration,
•	Atteindre une couverture de code élevée,
•	Respecter les standards de qualité et de documentation,
•	Offrir un service fiable, performant et stable.

8. Livrables attendus

Conformément au cahier des charges du TP, les livrables suivants seront produits :
- `PLAN.md` : Plan de tests détaillant la stratégie de validation (ce document).
- Mise en place complète de l’environnement de tests (structure des dossiers, Makefile, premiers tests unitaires en erreur), même sans implémentation.
- Version finale de l’implémentation avec l’ensemble des tests fonctionnels, une couverture élevée, une documentation HTML générée et un code validé par `ruff`.
- `RETEX.md` : Retour d’expérience sur le projet, les choix effectués, les difficultés rencontrées, et les axes d’amélioration.

