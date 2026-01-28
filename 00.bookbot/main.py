from stats import *
import sys

def get_book_text(filepath):
    content = ""
    with open(filepath) as f:
        content = f.read()
    return content

def main():

    if len(sys.argv) < 2:
        print("Usage: python3 main.py <path_to_book>")
        sys.exit(1)
    print("============ BOOKBOT ============")
    path = sys.argv[1]

    print(f"Analyzing book found at {path}")
    text = get_book_text(path)
    num_words = word_count(text)

    print("----------- Word Count ----------")
    print(f"Found {num_words} total words")
    
    print("----------- Character Count ----------")
    dictionary = sort_dictionary(char_count(text))
    for symbol in dictionary:
        if symbol["char"].isalpha():
            print(f"{symbol['char']}: {symbol['num']}")

    print("============= END ===============")

main()