import sys

from lib.lexer import Lexer


def main():
    if not len(sys.argv) > 1:
        print("Provide the script to be parsed")
        return

    file_path = sys.argv[1]
    lexer = Lexer(file_path)

    lexer.print_tokens()

if __name__ == "__main__":
    main()