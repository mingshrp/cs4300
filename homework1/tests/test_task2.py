import pytest
from src.task2 import integer_type, float_type, string_type, bool_type

def test_integer_type():
    assert isinstance(integer_type(), int)
    assert integer_type() == 1234

def test_float_type():
    assert isinstance(float_type(), float)
    assert float_type() == 3.14

def test_string_type():
    assert isinstance(string_type(), str)
    assert string_type() == "Hello, World!"

def test_bool_type():
    assert isinstance(bool_type(), bool)
    assert bool_type() == False