import pytest
from src.task3 import check_number, is_prime , first_ten_primes , sum_1_to_100

def test_check_number():
    assert check_number(1) == "Positive"
    assert check_number(-1) == "Negative"
    assert check_number(0) == "Zero"

def test_is_prime():
    assert is_prime(2) == True
    assert is_prime(1) == False
    assert is_prime(29) == True
    assert is_prime(4) == False

def test_first_ten_primes():
    assert first_ten_primes() == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

def test_sum1_to_100():
    assert sum_1_to_100() == 5050 # check if it equals to the correct sum of 1 to 100