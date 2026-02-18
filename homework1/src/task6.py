# Explanation: Read and count the # of words in the text file

def count_words(filename: str) -> int:
    # open file in read mode
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
    # split content into list of words and count # of items/words 
    return len(text.split())

