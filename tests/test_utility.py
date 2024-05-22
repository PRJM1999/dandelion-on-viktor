import numpy as np
import pytest
from src.utility import valid_range, haversine

def test_all_elements_valid():
    x = np.array([1, 2, 3, 4])
    valid = (1, 4)
    expected = np.array([1, 2, 3, 4])
    np.testing.assert_array_equal(valid_range(x, valid), expected)

def test_no_elements_valid():
    x = np.array([10, 20, 30, 40])
    valid = (1, 9)
    expected = np.array([np.nan, np.nan, np.nan, np.nan])
    np.testing.assert_array_equal(valid_range(x, valid), expected)

def test_some_elements_valid():
    x = np.array([1, 2, 10, 4])
    valid = (1, 4)
    expected = np.array([1, 2, np.nan, 4])
    np.testing.assert_array_equal(valid_range(x, valid), expected)

def test_empty_array():
    x = np.array([])
    valid = (0, 1)
    expected = np.array([])
    np.testing.assert_array_equal(valid_range(x, valid), expected)

def test_non_numeric_input():
    x = np.array(['a', 'b', 'c'])
    valid = (0, 2)
    with pytest.raises(TypeError):
        valid_range(x, valid)

def test_distance_between_known_points():
    # Example: New York (40.7128° N, 74.0060° W) and London (51.5074° N, 0.1278° W)
    distance = haversine(-74.0060, 40.7128, 0.1278, 51.5074)
    expected = 5587
    assert int(distance) == expected

def test_distance_to_same_point():
    distance = haversine(-74.0060, 40.7128, -74.0060, 40.7128)
    expected = 0
    assert distance == expected

def test_invalid_input():
    with pytest.raises(TypeError):
        haversine('not a number', 'not a number', 'not a number', 'not a number')