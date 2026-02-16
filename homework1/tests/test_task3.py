import pytest
from src.task3 import check_number, sum_1_to_100

def test_check_number():
    assert check_number(1) == "Positive"
    assert check_number(-1) == "Negative"
    assert check_number(0) == "Zero"


def test_sum1_to_100():
    assert sum_1_to_100() == 5050 # check if it equals to the correct sum of 1 to 100