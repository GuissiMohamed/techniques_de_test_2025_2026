import pytest
from triangulator.logic import validate_points

def test_valid_points():
    validate_points([(0,0),(1.5,-2.5)])

def test_invalid_not_list():
    with pytest.raises(ValueError):
        validate_points("hello")

def test_invalid_wrong_len():
    with pytest.raises(ValueError):
        validate_points([(1,2,3)])

def test_invalid_non_numeric():
    with pytest.raises(ValueError):
        validate_points([(0,"A")])

def test_invalid_mixed():
    with pytest.raises(ValueError):
        validate_points([(0,0), "bad"])

def test_empty_list_valid():
    validate_points([])
