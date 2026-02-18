# Explanation: This tests verifies the print output of script capturing stdout

import pytest
# Import function to be tested from the task1 module
from src.task1 import hello_world

# Uses capsys to capture system output
def test_hello_world(capsys):
    hello_world()
    captured = capsys.readouterr()

    assert captured.out.strip() == "Hello, World!"
