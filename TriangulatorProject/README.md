# 🔺 Triangulator — M1 ILSEN

Microservices • Format Binaire • Tests Unitaires • Intégration • Performance

---

## 🚀 Présentation du Projet

Triangulator est un système constitué de **deux microservices** capables de :

- 📌 stocker des ensembles de points 2D
- 📌 calculer leur triangulation (sans SciPy / NumPy)
- 📌 communiquer en **format binaire compact**
- 📌 être entièrement testés : unitaires, intégration, performance

Ce projet a été réalisé dans le cadre du module **Techniques de Test** (M1 ILSEN).

---

# 🏗️ Architecture Globale

Frontend (HTML/Canvas)
|
JSON | /triangulate
v
+-----------------+
| Triangulator |
| - Validation |
| - Triangulation|
| - Réponse JSON |
| - Réponse BIN |
+--------+--------+
|
BINAIRE 🔄 HTTP
|
+-----------------+
| PointSetManager |
| - Stockage |
| - JSON / BIN |
+-----------------+

yaml
Copier le code

---

# 🧩 Microservices

## 1️⃣ PointSetManager (PSM)

- Reçoit un PointSet en **JSON** ou **binaire**
- Stocke en mémoire
- Renvoie les points en :
  - JSON → debug
  - BINAIRE → communication inter-services

### 🔢 Format PointSet (binaire)

4 bytes → unsigned int N = nombre de points
N fois :
4 bytes → float32 X
4 bytes → float32 Y

yaml
Copier le code

---

## 2️⃣ Triangulator

- Récupère un PointSet depuis PSM
- Valide les données
- Calcule la triangulation (algorithme _from scratch_)
- Renvoie :
  - JSON pour les clients “classiques”
  - BINAIRE si Accept: application/octet-stream

### 🔺 Format Triangles (binaire)

Part 1 : mêmes données que PointSet
Part 2 :
4 bytes → unsigned int T = nombre de triangles
T fois :
4 bytes → index A
4 bytes → index B
4 bytes → index C

yaml
Copier le code

---

# 🧪 Stratégie de Tests (Complète & Professionnelle)

La force du projet est son **volume important de tests variés** :  
unitaires, intégration, robustesse, end-to-end, performance.

---

# ✔️ 1. Tests Unitaires

## ▶️ a) Tests du format binaire

Vérifient :

- encodage/décodage correct
- respect du big-endian
- structure exacte du protocole
- gestion des fichiers tronqués
- robustesse → headers incorrects, buffers trop courts

📁 `tests/unit/test_binary.py`  
📁 `tests/unit/test_binary_valid.py`  
📁 `tests/unit/test_binary_invalid.py`

---

## ▶️ b) Tests de triangulation

Vérifient :

- pas de triangles avec < 3 points
- fan triangulation correcte
- gestion des points colinéaires
- suppression automatique des doublons

📁 `tests/unit/test_logic_triangulation.py`  
📁 `tests/unit/test_logic.py`

---

## ▶️ c) Tests de validation

Vérifient que :

- seul `[ [x,y], ... ]` est accepté
- les types invalides provoquent une erreur
- une liste vide est valide

📁 `tests/unit/test_logic_validation.py`

---

# ✔️ 2. Tests d’Intégration

Ces tests lancent **réellement les deux microservices** et vérifient les échanges.

---

## ▶️ a) PSM

- POST binaire
- GET binaire
- ID inexistant
- JSON valide
- binaire invalide
- /ping

📁 `tests/integration/test_psm_routes.py`

---

## ▶️ b) Triangulator

- Triangulation JSON
- Triangulation BINAIRE via ID
- JSON invalide
- paramètre manquant
- PSM indisponible
- /ping

📁 `tests/integration/test_tri_routes.py`

---

# ✔️ 3. Tests End-to-End (workflow complet)

PointSet → Encode → PSM → Triangulator → Triangles → Decode

yaml
Copier le code

- vérification complète du pipeline
- stress test : répété 10 fois
- test sur gros dataset

📁 `tests/integration/test_end_to_end_binary.py`

---

# 🚀 4. Tests de Performance

Mesurent :

- vitesse triangulation
- vitesse encodage/décodage binaire
- scalabilité

📁 `tests/performance/test_perf.py`

---

# 📦 Installation

```bash
git clone <ton-depot>
cd Triangulator_project
python3 -m venv venv
source venv/bin/activate
make install
▶️ Lancer les microservices
Dans deux terminaux différents :

Terminal 1 : PSM
bash
Copier le code
make run_psm
Terminal 2 : Triangulator
bash
Copier le code
make run_triangulator
🧪 Lancer les tests
Tous les tests
bash
Copier le code
make test
Uniquement unitaires + intégration
bash
Copier le code
make unit_test
Performance uniquement
bash
Copier le code
make perf_test
Couverture
bash
Copier le code
make coverage
🎨 Frontend (demo.html)
Une interface graphique permet :

d’ajouter des points sur un canvas

de les déplacer

de les supprimer

de lancer la triangulation

de visualiser le résultat en temps réel

Aucun serveur web n’est requis — il suffit d’ouvrir :

Copier le code
demo.html
🔚 Conclusion
Ce projet met en œuvre :

✔️ une architecture microservices robuste

✔️ un protocole binaire conforme

✔️ une triangulation codée from scratch

✔️ une suite de tests large, variée, professionnelle

✔️ une documentation et un frontend complet

Un excellent exemple de développement piloté par les tests (TDD).

👤 Auteur
Mohamed Guissi — M1 ILSEN
Projet réalisé pour le module Techniques de Test

```
