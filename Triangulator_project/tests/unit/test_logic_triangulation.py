import pytest
from triangulator.logic import triangulate

def test_no_points():
    assert triangulate([]) == []

def test_one_point():
    assert triangulate([(0,0)]) == []

def test_two_points():
    assert triangulate([(0,0),(1,1)]) == []

def test_three_points_simple():
    pts = [(0,0),(1,0),(0,1)]
    tris = triangulate(pts)
    assert tris == [(0,1,2)]

def test_four_points_fan():
    pts = [(0,0),(1,0),(1,1),(0,1)]
    tris = triangulate(pts)
    assert tris == [(0,1,2),(0,2,3)]

def test_colinear_points():
    pts = [(0,0),(1,1),(2,2),(3,3)]
    assert triangulate(pts) == []

def test_duplicate_points():
    pts = [(0,0),(1,0),(1,0),(0,1)]
    assert triangulate(pts) == [(0,1,2)]
