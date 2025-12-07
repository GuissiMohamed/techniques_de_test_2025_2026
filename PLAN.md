PLAN DE TESTS — Triangulator Project (M1 ILSEN)
🎯 Objectif du document

Ce document décrit de manière structurée la stratégie de tests mise en place pour valider le microservice Triangulator et son interaction avec le PointSetManager.
Le plan couvre :

les tests unitaires

les tests d’intégration

les tests de performance

les raisons derrière chaque choix

la couverture visée

1. Portée du système testé

Le projet comporte deux microservices :

🔹 PointSetManager

Enregistre des ensembles de points (PointSet)

Les renvoie au format binaire (exigence principale du sujet)

Communication via HTTP

🔹 Triangulator

Récupère les points auprès du PointSetManager

Valide les données

Calcule la triangulation (implémentation "from scratch", sans SciPy)

Renvoie les résultats en JSON ou binaire (Triangles)

2. Types de tests prévus
2.1 Tests unitaires
Objectifs

Vérifier individuellement le comportement des composants internes :

Encodage/décodage binaire (PointSet & Triangles)

Validation des points

Triangulation “from scratch”

Formatage des réponses JSON

Justification

La logique interne contient des points critiques :

La représentation binaire est sensible aux erreurs de format

Les floats doivent être traités avec tolérance (float32 ↔ float64)

La triangulation doit fonctionner dans tous les cas non dégénérés

Tests unitaires prévus
Fonction	Tests
pointset_to_bytes	encode un ensemble de points
bytes_to_pointset	decode correctement, tolérance float
triangles_to_bytes	encode points + triangles
bytes_to_triangles	decode un flux complet
validate_points	formats invalides, valeurs incorrectes
triangulate	cas normaux, 1 triangle, multiples triangles, doublons, colinéarité

Les tests unitaires sont situés dans :
➡️ tests/unit/

2.2 Tests d’intégration
Objectifs

Vérifier que les deux microservices communiquent réellement ensemble

Assurer le bon fonctionnement bout-en-bout :

stockage PointSet → récupération binaire → triangulation → réponse API

Justification

Le sujet insiste sur la communication binaire entre composants, ce qui nécessite une validation spécifique.

Tests d’intégration prévus
Scénario	Description
POST binaire /points	enregistre un PointSet
GET binaire /points/{id}/binary	récupère les points encodés
POST /triangulate (JSON)	triangulation simple
POST /triangulate + Accept: application/octet-stream	réponse binaire Triangles
Erreurs attendues	ID inexistant, formats invalides, PSM injoignable

Les tests d’intégration sont situés dans :
➡️ tests/integration/

2.3 Tests de performance
Objectifs

Évaluer la performance :

de la triangulation

de l’encodage et du décodage binaire

Vérifier que le système reste réactif avec plusieurs milliers de points

Justification

Le sujet indique explicitement que :

la conversion binaire peut être coûteuse

les tests de performance doivent être séparés

Tests prévus
Test	Charge	Critère
triangulation small	100 points	< 200 ms
triangulation medium	500 points	< 800 ms
encodage PointSet	2000 points	< 300 ms
décodage PointSet	idem	< 300 ms

Les tests de performance sont situés dans :
➡️ tests/performance/
et exclus du test global.

3. Couverture de code

Objectif : > 90% de lignes couvertes
Mesurée via :

make coverage


Les parties non couvertes acceptées :

gestion d’erreurs "imprévisibles"

code spécifique au lancement serveur Flask (main)

4. Outils utilisés

pytest : framework de tests

coverage : mesure de couverture

ruff : qualité du code

make : orchestration des commandes

pdoc3 : génération de documentation

5. Conclusion

Ce plan de test permet de garantir :

la conformité de l’implémentation aux spécifications du sujet

la stabilité entre composants

la performance du système

la qualité et la maintenabilité du code

➡️ Il constitue la base de la stratégie de validation appliquée dans ce projet.