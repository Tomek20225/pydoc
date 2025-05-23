import sys

from lib.lexer import Lexer
from lib.parser import Parser


def main():
    if not len(sys.argv) > 1:
        print("Provide the script to be parsed")
        return

    file_path = sys.argv[1]

    lexer = Lexer(file_path)
    parser = Parser(lexer.tokens)
    parser.print_ast()

if __name__ == "__main__":
    main()