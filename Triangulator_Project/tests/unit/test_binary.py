import pytest
from triangulator.binary import (
    pointset_to_bytes,
    bytes_to_pointset,
    triangles_to_bytes,
    bytes_to_triangles,
)


def test_pointset_encode_decode():
    """
    Vérifie que pointset_to_bytes -> bytes_to_pointset conserve les valeurs,
    avec tolérance car float32 n'est pas parfaitement précis.
    """
    points = [(0.0, 0.0), (1.5, -2.5), (3.14, 2.72)]

    data = pointset_to_bytes(points)
    decoded = bytes_to_pointset(data)

    # Comparaison point par point (pytest.approx accepté)
    for d, p in zip(decoded, points):
        assert d == pytest.approx(p)


def test_empty_pointset():
    """PointSet vide."""
    points = []
    data = pointset_to_bytes(points)
    decoded = bytes_to_pointset(data)

    assert decoded == points


def test_triangles_encode_decode():
    """Test complet : encodage et décodage d'un Triangles simple."""
    points = [(0, 0), (1, 0), (0, 1)]
    triangles = [(0, 1, 2)]

    data = triangles_to_bytes(points, triangles)
    decoded_points, decoded_triangles = bytes_to_triangles(data)

    for d, p in zip(decoded_points, points):
        assert d == pytest.approx(p)

    assert decoded_triangles == triangles


def test_triangles_multiple():
    """Plusieurs triangles encodés/décodés."""
    points = [(0, 0), (1, 0), (1, 1), (0, 1)]
    triangles = [(0, 1, 2), (0, 2, 3)]

    data = triangles_to_bytes(points, triangles)
    decoded_points, decoded_triangles = bytes_to_triangles(data)

    for d, p in zip(decoded_points, points):
        assert d == pytest.approx(p)

    assert decoded_triangles == triangles


