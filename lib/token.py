from dataclasses import dataclass
from enum import Enum
from typing import Optional

import re


# TODO: Complete the list
class TokenType(Enum):
    AND = "AND"
    APOS = "APOS"
    ARROW = "ARROW"
    ASYNC = "ASYNC"
    BIN_AND = "BIN_AND"
    BIN_OR = "BIN_OR"
    BREAK = "BREAK"
    CLASS = "CLASS"
    CLOSE_BRACE = "CLOSE_BRACE"
    CLOSE_BRACKET = "CLOSE_BRACKET"
    CLOSE_PAREN = "CLOSE_PAREN"
    COLON = "COLON"
    COLON_EQ = "COLON_EQ"
    COMMA = "COMMA"
    CONTINUE = "CONTINUE"
    DEF = "DEF"
    DIV = "DIV"
    DIV_EQ = "DIV_EQ"
    DOT = "DOT"
    ELIF = "ELIF"
    ELLIPSIS = "ELLIPSIS"
    ELSE = "ELSE"
    EQ = "EQ"
    EQ_DOUBLE = "EQ_DOUBLE"
    EXCLAMATION = "EXCLAMATION"
    EXCLAMATION_EQ = "EXCLAMATION_EQ"
    FLOAT_LITERAL = "FLOAT_LITERAL"
    FOR = "FOR"
    FROM = "FROM"
    GT = "GT"
    GT_EQ = "GT_EQ"
    IDENTIFIER = "IDENTIFIER"
    IF = "IF"
    IMPORT = "IMPORT"
    IN = "IN"
    INDENT = "INDENT"
    INT_LITERAL = "INT_LITERAL"
    IS = "IS"
    LAMBDA = "LAMBDA"
    LT = "LT"
    LT_EQ = "LT_EQ"
    MINUS = "MINUS"
    MINUS_EQ = "MINUS_EQ"
    MULT = "MULT"
    MULT_EQ = "MULT_EQ"
    OPEN_BRACE = "OPEN_BRACE"
    OPEN_BRACKET = "OPEN_BRACKET"
    OPEN_PAREN = "OPEN_PAREN"
    OR = "OR"
    PASS = "PASS"
    PLUS = "PLUS"
    PLUS_EQ = "PLUS_EQ"
    RAISE = "RAISE"
    RETURN = "RETURN"
    SELF = "SELF"
    STR_LITERAL = "STR_LITERAL"
    WHILE = "WHILE"
    QUOT = "QUOT"
    # TODO: F-string and B-string (f"", b"")
    # TODO: Hash (comment)
    # TODO: Docstring (""")
    # TODO: Decorators (@)
    # TODO: Binary literals (0b101111, 0B010101)
    # TODO: Octal literals (0o123)
    # TODO: Hex literals (0x123)
    # TODO: Power operator (**)


@dataclass
class Token:
    value: str
    type: TokenType


def match_token_type(v: str):
    if v == "and": return TokenType.AND
    elif v == "'": return TokenType.APOS
    elif v == "->": return TokenType.ARROW
    elif v == "async": return TokenType.ASYNC
    elif v == "&": return TokenType.BIN_AND
    elif v == "|": return TokenType.BIN_OR
    elif v == "break": return TokenType.BREAK
    elif v == "class": return TokenType.CLASS
    elif v == "}": return TokenType.CLOSE_BRACE
    elif v == "]": return TokenType.CLOSE_BRACKET
    elif v == ")": return TokenType.CLOSE_PAREN
    elif v == ":": return TokenType.COLON
    elif v == ":=": return TokenType.COLON_EQ
    elif v == ",": return TokenType.COMMA
    elif v == "continue": return TokenType.CONTINUE
    elif v == "def": return TokenType.DEF
    elif v == "/": return TokenType.DIV
    elif v == "/=": return TokenType.DIV_EQ
    elif v == ".": return TokenType.DOT
    elif v == "elif": return TokenType.ELIF
    elif v == "...": return TokenType.ELLIPSIS
    elif v == "else": return TokenType.ELSE
    elif v == "=": return TokenType.EQ
    elif v == "==": return TokenType.EQ_DOUBLE
    elif v == "!": return TokenType.EXCLAMATION
    elif v == "!=": return TokenType.EXCLAMATION_EQ
    elif v == "for": return TokenType.FOR
    elif v == "from": return TokenType.FROM
    elif v == ">": return TokenType.GT
    elif v == ">=": return TokenType.GT_EQ
    elif v == "if": return TokenType.IF
    elif v == "import": return TokenType.IMPORT
    elif v == "in": return TokenType.IN
    elif v == '\t': return TokenType.INDENT
    elif v == "is": return TokenType.IS
    elif v == "lambda": return TokenType.LAMBDA
    elif v == "<": return TokenType.LT
    elif v == "<=": return TokenType.LT_EQ
    elif v == "-": return TokenType.MINUS
    elif v == "-=": return TokenType.MINUS_EQ
    elif v == "*": return TokenType.MULT
    elif v == "*=": return TokenType.MULT_EQ
    elif v == "{": return TokenType.OPEN_BRACE
    elif v == "[": return TokenType.OPEN_BRACKET
    elif v == "(": return TokenType.OPEN_PAREN
    elif v == "or": return TokenType.OR
    elif v == "pass": return TokenType.PASS
    elif v == "+": return TokenType.PLUS
    elif v == "+=": return TokenType.PLUS_EQ
    elif v == "raise": return TokenType.RAISE
    elif v == "return": return TokenType.RETURN
    elif v == "self": return TokenType.SELF
    elif v == "while": return TokenType.WHILE
    elif v == '\"': return TokenType.QUOT

    # STR_LITERAL is identified on the Lexer level
    # FLOAT_LITERAL is derived from two INT_LITERAL and one DOT on the Lexer level
    # Complex operands like MULT_EQ, PLUS_EQ etc. may not get detected upon initial tokenization

    if re.search("^(\d|_)+$", v) is not None:
        return TokenType.INT_LITERAL
    return TokenType.IDENTIFIER


OPERATOR_TOKENS_WITH_VARIANTS = [
    TokenType.PLUS, TokenType.MINUS, TokenType.MULT, TokenType.DIV,
    TokenType.LT, TokenType.GT, TokenType.EQ, TokenType.COLON, TokenType.EXCLAMATION
]
def get_eq_token_variant(t: TokenType) -> Optional[TokenType]:
    if t == TokenType.PLUS: return TokenType.PLUS_EQ
    elif t == TokenType.MINUS: return TokenType.MINUS_EQ
    elif t == TokenType.MULT: return TokenType.MULT_EQ
    elif t == TokenType.DIV: return TokenType.DIV_EQ
    elif t == TokenType.LT: return TokenType.LT_EQ
    elif t == TokenType.GT: return TokenType.GT_EQ
    elif t == TokenType.EQ: return TokenType.EQ_DOUBLE
    elif t == TokenType.COLON: return TokenType.COLON_EQ
    elif t == TokenType.EXCLAMATION: return TokenType.EXCLAMATION_EQ
    return None


SPACING_CHARS = ['\t', '\n', ' ']
RESTRICTED_CHARS = [":", "(", ")", "[", "]", "{", "}", "=", ",", "."]
STR_LITERAL_CHARS = ["\"", "'"]