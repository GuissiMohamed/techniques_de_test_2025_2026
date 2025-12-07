import pytest
from triangulator.logic import triangulate, validate_points


def test_triangulate_simple():
    # Cas simple : un triangle unique
    points = [(0, 0), (1, 0), (0, 1)]
    triangles = triangulate(points)
    assert len(triangles) == 1


def test_triangulate_too_few_points():
    # Moins de 3 points -> pas de triangulation
    points = [(0, 0), (1, 0)]
    triangles = triangulate(points)
    assert triangles == []


def test_triangulate_colinear_points():
    # Points alignés sur une même droite -> cas dégénéré, renvoie []
    points = [(0, 0), (1, 1), (2, 2), (3, 3)]
    triangles = triangulate(points)
    assert triangles == []


def test_triangulate_with_duplicate_points():
    # Points avec doublons -> ne plante pas, renvoie une liste
    points = [(0, 0), (1, 0), (0, 1), (0, 0)]
    triangles = triangulate(points)
    assert isinstance(triangles, list)


def test_validate_points_valid():
    points = [(0.0, 1.0), (1.0, 0.0)]
    validate_points(points)  # ne doit pas lever d'erreur


@pytest.mark.parametrize("invalid_points", [
    "not a list",                  # pas une liste
    [(1, 2, 3)],                   # trop de coordonnées
    [(1, "a")],                    # coordonnées non numériques
    [{"x": 1, "y": 2}],            # mauvais type
])
def test_validate_points_invalid(invalid_points):
    with pytest.raises(ValueError):
        validate_points(invalid_points)
