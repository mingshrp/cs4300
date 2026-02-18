# Explanation: Test the calculate_discount function for all cases of price & discount data type

import pytest
from src.task4 import calculate_discount

# Case 1: Int price & Int discount
def test_discount_int_int():
    assert calculate_discount(100, 20) == 80

# Case 2: Float price & Float discount
def test_discount_float_float():
    assert calculate_discount(100.0, 10.0) == 90.0

# Case 3: Float price & Int discount
def test_discount_float_int():
    assert calculate_discount(100.0, 10) == 90.0

# Case 4: Int price & float discount
def test_discount_int_float():
    assert calculate_discount(100, 12.5) == 87.5

# Case 5: Account for zero discount 
def test_zero_discount():
    assert calculate_discount(50, 0) == 50  # price stays the same

# Case 6: Account for full discount
def test_full_discount():
    assert calculate_discount(300, 100) == 0 
