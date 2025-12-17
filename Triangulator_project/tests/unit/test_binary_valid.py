import pytest
import struct
from triangulator.binary import (
    pointset_to_bytes,
    bytes_to_pointset,
    triangles_to_bytes,
    bytes_to_triangles
)

def test_pointset_roundtrip_small():
    pts = [(0, 0), (1.5, -2.5), (10, 10)]
    encoded = pointset_to_bytes(pts)
    decoded = bytes_to_pointset(encoded)
    for (x, y), (x2, y2) in zip(pts, decoded):
        assert x2 == pytest.approx(x)
        assert y2 == pytest.approx(y)

def test_pointset_roundtrip_large():
    pts = [(i*0.1, i*0.2) for i in range(200)]
    encoded = pointset_to_bytes(pts)
    decoded = bytes_to_pointset(encoded)
    assert len(decoded) == 200

def test_pointset_big_endian_header():
    pts = [(0, 0), (1, 1)]
    data = pointset_to_bytes(pts)
    header = struct.unpack(">I", data[:4])[0]
    assert header == 2


def test_triangles_roundtrip_basic():
    pts = [(0, 0), (1, 0), (0, 1)]
    tris = [(0,1,2)]
    data = triangles_to_bytes(pts, tris)
    pts2, tris2 = bytes_to_triangles(data)
    assert pts2 == pytest.approx(pts)
    assert tris2 == tris

def test_triangles_roundtrip_multiple():
    pts = [(0, 0), (1, 0), (1, 1), (0, 1)]
    tris = [(0,1,2),(0,2,3)]
    data = triangles_to_bytes(pts, tris)
    pts2, tris2 = bytes_to_triangles(data)
    assert pts2 == pytest.approx(pts)
    assert tris2 == tris

def test_binary_length_matches_expected():
    pts = [(0, 0), (1, 0)]
    tris = [(0,1,1)]
    data = triangles_to_bytes(pts, tris)
    expected = 4 + len(pts)*8 + 4 + len(tris)*12
    assert len(data) == expected

def test_many_triangles():
    pts = [(i, i) for i in range(50)]
    tris = [(0, i, i+1) for i in range(1, 48)]
    data = triangles_to_bytes(pts, tris)
    pts2, tris2 = bytes_to_triangles(data)
    assert pts2 == pytest.approx(pts)
    assert tris2 == tris
