# Explanation: This tests the CORRECTNESS of task5.py for each data structure 

import pytest
from src.task5 import first_three_books, student_database

def test_first_three_books():
    # Check if sliced list matches the expected books
    assert first_three_books == [
        ("Pride and Prejudice", "Jane Austen"),
        ("Lord of the Flies", "William Golding"),
        ("Harry Potter and the Sorcerer's Stone", "J.K. Rowling")
    ]

def test_student_database():
    assert isinstance(student_database, dict) # ensure it is a dictionary 
    assert student_database["Mingma"] == 0000
    assert student_database["Janet"] == 1010
    assert student_database["George"] == 2100
    assert student_database["Will"] == 5678
