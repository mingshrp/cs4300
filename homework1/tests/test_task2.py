import pytest
from src.task2 import integer_type, float_type, string_type, bool_type

def test_integer_type():
    assert isinstance(integer_type(), int)
    assert integer_type() == 1234

    