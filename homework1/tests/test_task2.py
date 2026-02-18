# Explanation: This verifies that each function of task2.py returns the correct data type and expected value 
# Referred to https://docs.pytest.org/en/7.1.x/example/parametrize.html 

import pytest
from src.task2 import integer_type, float_type, string_type, bool_type

# Parametrize with function, expected type, expected value
@pytest.mark.parametrize(
    "func, expected_type, expected_value",
    [
        (integer_type, int, 1234),
        (float_type, float, 3.14),
        (string_type, str, "Hello, World!"),
        (bool_type, bool, False)
    ]
)
def test_types_and_values(func, expected_type, expected_value):
    # Check each func returns the correct type & expected value
    result = func()
    assert isinstance(result, expected_type), f"{func.__name__} unexpected"
    assert result == expected_value, f"{func.__name__} unexpected"