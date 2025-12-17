# =======================================================
# Makefile - Triangulator Project (Mohamed Guissi - M1 ILSEN)
# =======================================================

PYTHON = python
PSM_PORT = 5051
TRIANGULATOR_PORT = 5050
POINTSET_MANAGER_URL = http://localhost:$(PSM_PORT)

# =======================================================
# ENVIRONNEMENT VIRTUEL
# =======================================================

venv:
	$(PYTHON) -m venv venv
	@echo "✅ Environnement virtuel créé."
	@echo "➡️  Active-le avec :"
	@echo "   source venv/bin/activate (macOS / Linux)"
	@echo "   venv\\Scripts\\activate (Windows)"

install:
	pip install -r requirements.txt
	pip install -r dev_requirements.txt

# =======================================================
# LANCEMENT DES SERVICES
# =======================================================

run_psm:
	@echo "🚀 Lancement du PointSetManager sur le port $(PSM_PORT)..."
	PSM_PORT=$(PSM_PORT) $(PYTHON) -m pointset_manager.app

run_triangulator:
	@echo "🚀 Lancement du Triangulator sur le port $(TRIANGULATOR_PORT)..."
	POINTSET_MANAGER_URL=$(POINTSET_MANAGER_URL) \
	TRIANGULATOR_PORT=$(TRIANGULATOR_PORT) \
	$(PYTHON) -m triangulator.app

# =======================================================
# TESTS
# =======================================================

# Tous les tests (unitaires + intégration + performance)
test:
	PYTHONPATH=. pytest -v

# Tous sauf performance
unit_test:
	PYTHONPATH=. pytest -v --ignore=tests/performance

# Seulement performance
perf_test:
	PYTHONPATH=. pytest -v tests/performance

# =======================================================
# COUVERTURE
# =======================================================

coverage:
	PYTHONPATH=. coverage run -m pytest
	coverage report -m

# =======================================================
# QUALITÉ DE CODE
# =======================================================

lint:
	ruff check .

# =======================================================
# DOCUMENTATION
# =======================================================

doc:
	pdoc3 --html triangulator -o docs --force
	@echo "📘 Documentation générée dans ./docs"

# =======================================================
# NETTOYAGE
# =======================================================

clean:
	rm -rf __pycache__ */__pycache__ .pytest_cache .coverage docs
	@echo "🧹 Nettoyage terminé"

# =======================================================
# HELP
# =======================================================

help:
	@echo "🔧 Commandes disponibles :"
	@echo "  make venv             -> crée l'environnement virtuel"
	@echo "  make install          -> installe les dépendances"
	@echo "  make run_psm          -> lance le PointSetManager"
	@echo "  make run_triangulator -> lance le Triangulator"
	@echo "  make test             -> tous les tests"
	@echo "  make unit_test        -> tests sans performance"
	@echo "  make perf_test        -> tests de performance"
	@echo "  make coverage         -> rapport de couverture"
	@echo "  make lint             -> qualité du code (ruff)"
	@echo "  make doc              -> documentation HTML"
	@echo "  make clean            -> nettoyage des fichiers temporaires"
