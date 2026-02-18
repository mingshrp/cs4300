# Explanation: Demonstrates Matrix Multiplication with numpy np.matmul (can also use np.dot)
# Refer to https://numpy.org/doc/stable/user/absolute_beginners.html

import numpy as np

# A = 1st matrix
# B = 2nd matrix 
def matrix_multiply(A, B):
    if len(A[0]) != len(B):
        raise ValueError(
            "Number of columns in the first matrix must equal "
            "the number of rows in the second matrix."
        )
    return np.matmul(A, B).tolist()
