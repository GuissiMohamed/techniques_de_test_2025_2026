import time
import random

from triangulator.logic import triangulate
from triangulator.binary import (
    pointset_to_bytes,
    bytes_to_pointset,
    triangles_to_bytes,
    bytes_to_triangles,
)


def generate_points(n):
    """Génère n points aléatoires dans [0,1]."""
    return [(random.random(), random.random()) for _ in range(n)]


def test_perf_triangulation_small():
    points = generate_points(100)
    start = time.time()
    tris = triangulate(points)
    elapsed = time.time() - start
    assert elapsed < 0.2  # 200 ms max pour 100 points


def test_perf_triangulation_medium():
    points = generate_points(500)
    start = time.time()
    tris = triangulate(points)
    elapsed = time.time() - start
    assert elapsed < 0.8  # < 800 ms


def test_perf_binary_encode_decode():
    points = generate_points(2000)

    # encode
    start = time.time()
    data = pointset_to_bytes(points)
    elapsed_encode = time.time() - start

    # decode
    start = time.time()
    pts_out = bytes_to_pointset(data)
    elapsed_decode = time.time() - start

    assert elapsed_encode < 0.3
    assert elapsed_decode < 0.3


def test_perf_triangles_encode_decode():
    points = generate_points(2000)
    triangles = [(0, 1, 2)] * 1000  # 1000 triangles

    start = time.time()
    data = triangles_to_bytes(points, triangles)
    elapsed_encode = time.time() - start

    start = time.time()
    p2, t2 = bytes_to_triangles(data)
    elapsed_decode = time.time() - start

    assert elapsed_encode < 0.5
    assert elapsed_decode < 0.5
