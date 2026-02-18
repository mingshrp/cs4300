# Explanation: Tests for valid matrix multiplications and raises an error for incompatible matrices

# test_task7.py
import pytest
from src.task7 import matrix_multiply

@pytest.mark.parametrize(
    "A, B, expected",
    [
        # 2x2 matrices
        (
            [[1, 2], [3, 4]],
            [[5, 6], [7, 8]],
            [[19, 22], [43, 50]]
        ),
        # 2x3 and 3x2 matrices
        (
            [[1, 2, 3], [4, 5, 6]],
            [[7, 8], [9, 10], [11, 12]],
            [[58, 64], [139, 154]]
        ),
        # 1x2 and 2x1 matrices
        (
            [[2, 3]],
            [[4], [5]],
            [[23]]
        ),
        # multiplying with identity matrix
        (
            [[1, 2], [3, 4]],
            [[1, 0], [0, 1]],
            [[1, 2], [3, 4]]
        )
    ]
)
def test_matrix_multiply(A, B, expected):
    assert matrix_multiply(A, B) == expected

# Test for error
def test_matrix_multiply_incompatible():
    A = [[1, 2]]
    B = [[3, 4]]  
    with pytest.raises(ValueError, match="Number of columns in the first matrix must equal the number of rows in the second matrix."):
        matrix_multiply(A, B)
