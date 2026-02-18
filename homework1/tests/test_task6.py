# Explanation: Parametrized tests for file word count
# Referred to https://docs.pytest.org/en/7.1.x/example/parametrize.html 
# Text file contains 127 words

import os
import pytest
from src.task6 import count_words 

 # First get path to text file located homework1/
filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "task6_read_me.txt") 

# Parametrized test using file paths and expected word counts
@pytest.mark.parametrize(
    "file_path, content, expected_count",
    [
        # ORIGINAL file
        (filepath, None, 127), # 127 words (checked with online word count tool)

        # Temp files with different content
        ("empty.txt", "", 0),
        ("single.txt", "Hello", 1),
        ("multi_space.txt", "Hello   world   hello   w   orld", 5),
        ("multi_line.txt", "hello this\nis task\nsix", 5),
        ("punctuation.txt", "hello , world .", 4)
    ]
)

# test word_count with the Original file & temp files
def test_word_count(file_path, content, expected_count, tmp_path):
    if content is not None:
        # Create temp file in tmp_path
        test_file = tmp_path / file_path
        test_file.write_text(content)
        file_path_to_use = test_file
    else:
        # Use real file
        file_path_to_use = file_path

    assert count_words(file_path_to_use) == expected_count