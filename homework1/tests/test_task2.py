# Explanation: This verifies that each function of task2.py returns the correct data type and expected value

import pytest
from src.task2 import integer_type, float_type, string_type, bool_type

def test_integer_type():
    assert isinstance(integer_type(), int) # Check return type is int
    assert integer_type() == 1234   # also checks that the value matches

def test_float_type():
    assert isinstance(float_type(), float) # Check return type is float
    assert float_type() == 3.14

def test_string_type():
    assert isinstance(string_type(), str) # Check return type is string
    assert string_type() == "Hello, World!"

def test_bool_type():
    assert isinstance(bool_type(), bool) # Check return type is boolean
    assert bool_type() == False