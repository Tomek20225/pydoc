from enum import Enum
from typing import List, Optional, Tuple
import os
from lib.token import Token, SPACING_CHARS, TokenType, RESTRICTED_CHARS, STR_LITERAL_CHARS, match_token_type, \
    get_eq_token_variant, OPERATOR_TOKENS_WITH_VARIANTS
from lib.utils import convert_leading_spaces_to_tabs


class Lexer:
    path: str = ""
    cursor: int = 0
    content: str = ""
    tokens: List[Token] = []

    def __init__(self, path: str):
        self.path = path

        if not os.path.isfile(path):
            print("The path provided doesn't lead to a file")
            raise FileNotFoundError

        if not path.endswith(".py"):
            print("The path provided doesn't lead to a valid Python file")
            raise AttributeError

        self.read()
        self.tokenize()

    def read(self):
        print(f"Reading {self.path}...")
        self.content = '\n'.join(convert_leading_spaces_to_tabs(line) for line in open(self.path))

    def tokenize(self):
        print(f"Tokenizing {self.path}...")

        while (word_tup := self._read_next_word()) is not None:
            word, t_type = word_tup
            if t_type is None:
                t_type = match_token_type(word)
            token = Token(value=word, type=t_type)
            self.tokens.append(token)

        self._simplify_tokens()

    def print_tokens(self):
        for token in self.tokens:
            print(repr(token))

    def _simplify_tokens(self):
        new_tokens = []
        token_amount = len(self.tokens)
        i = 0

        while i < token_amount:
            token = self.tokens[i]

            # Float literals
            if token.type == TokenType.INT_LITERAL and i + 2 < token_amount:
                next_token = self.tokens[i + 1]
                next_next_token = self.tokens[i + 2]
                if next_token.type == TokenType.DOT and next_next_token.type == TokenType.INT_LITERAL:
                    float_value = f"{token.value}.{next_next_token.value}"
                    new_token = Token(value=float_value, type=TokenType.FLOAT_LITERAL)
                    new_tokens.append(new_token)
                    i += 3
                    continue

            # Complex operators
            if token.type in OPERATOR_TOKENS_WITH_VARIANTS and i + 1 < token_amount:
                next_token = self.tokens[i + 1]
                if next_token.type == TokenType.EQ:
                    new_value = f"{token.value}{next_token.value}"
                    new_type = get_eq_token_variant(token.type)
                    new_token = Token(value=new_value, type=new_type)
                    new_tokens.append(new_token)
                    i += 2
                    continue

            # TODO: Ellipsis
            # TODO: Pow

            new_tokens.append(self.tokens[i])
            i += 1

        self.tokens = new_tokens

    def _read_next_word(self) -> Optional[Tuple[str, Optional[TokenType]]]:
        acc: str = ""
        mode: ReadMode = ReadMode.WORD
        str_literal_start: Optional[str] = None

        while (char := self._read_next_char()) is not None:
            if acc == "":
                if char in SPACING_CHARS:
                    mode = ReadMode.INDENT
                elif char in RESTRICTED_CHARS:
                    mode = ReadMode.RESTRICTED
                elif char in STR_LITERAL_CHARS:
                    mode = ReadMode.STR_LITERAL
                    str_literal_start = char

            if mode == ReadMode.INDENT and (
                char not in SPACING_CHARS
                or (char == '\t' and acc != "")
            ):
                self.cursor -= 1
                if acc == "" or (all([c == ' ' for c in acc]) and len(acc) % 4 != 0):
                    acc = ""
                    mode = ReadMode.WORD
                    str_literal_start = None
                    continue
                return acc, None

            if mode == ReadMode.RESTRICTED:
                return char, None

            if mode == ReadMode.STR_LITERAL and char is str_literal_start:
                if acc == "":
                    continue
                elif acc != "" and not acc.endswith('\\'):
                    return acc, TokenType.STR_LITERAL

            if mode == ReadMode.WORD and (char in SPACING_CHARS or char in RESTRICTED_CHARS):
                self.cursor -= 1
                return acc, None

            if char != '\n':
                acc += char

        return (acc, None) if acc else None

    def _read_next_char(self) -> Optional[str]:
        if self.cursor >= len(self.content):
            return None
        char = self.content[self.cursor]
        self.cursor += 1
        return char


class ReadMode(Enum):
    INDENT = "INDENT"
    RESTRICTED = "RESTRICTED"
    STR_LITERAL = "STR_LITERAL"
    WORD = "WORD"
