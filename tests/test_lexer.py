from typing import List

from lib.lexer import Lexer
from lib.token import TokenType, Token
import pathlib
import pytest

base_path = pathlib.Path(__file__).parent.resolve() / "test_data"
CODE_FILE_PATH = (base_path / "lexer_test_data.py").as_posix()


def run_lexer_test(lexer: Lexer, expected_tokens: List[Token]) -> None:
    if not expected_tokens:
        return

    expected_tokens_counter = 0
    for token in lexer.tokens:
        if expected_tokens_counter == len(expected_tokens) - 1:
            assert True
            return
        if expected_tokens_counter > 0 and token != expected_tokens[expected_tokens_counter]:
            expected_tokens_counter = 0
            continue
        if token == expected_tokens[expected_tokens_counter]:
            expected_tokens_counter += 1
            continue

    assert False


def run_lexer_counter_test(lexer: Lexer, expected_token: Token, expected_count: int = 1) -> None:
    counter = 0
    for token in lexer.tokens:
        if token == expected_token:
            counter += 1

    assert expected_count == counter


@pytest.fixture(scope="module")
def lexer_of_code_file() -> Lexer:
    return Lexer(CODE_FILE_PATH)


class TestWhitespace:
    def test_handles_newlines(self, lexer_of_code_file: Lexer) -> None:
        run_lexer_test(
            lexer=lexer_of_code_file,
            expected_tokens=[
                Token(value='from', type=TokenType.FROM),
                Token(value='typing', type=TokenType.IDENTIFIER),
                Token(value='import', type=TokenType.IMPORT),
                Token(value='List', type=TokenType.IDENTIFIER),
                Token(value=',', type=TokenType.COMMA),
                Token(value='Callable', type=TokenType.IDENTIFIER),
                Token(value=',', type=TokenType.COMMA),
                Token(value='Any', type=TokenType.IDENTIFIER),
                # first newline in the file
                Token(value='import', type=TokenType.IMPORT),
                Token(value='sys', type=TokenType.IDENTIFIER),
            ]
        )

    def test_omits_whitespace_between_class_and_identifier(self, lexer_of_code_file: Lexer) -> None:
        run_lexer_test(
            lexer=lexer_of_code_file,
            expected_tokens=[
                Token(value='class', type=TokenType.CLASS),
                # plenty of unnecessary, but syntactically valid whitespace
                Token(value='Foo', type=TokenType.IDENTIFIER),
                Token(value=':', type=TokenType.COLON)
            ]
        )

class TestCounts:
    def test_finds_all_defs(self, lexer_of_code_file: Lexer):
        run_lexer_counter_test(
            lexer=lexer_of_code_file,
            expected_token=Token(value='def', type=TokenType.DEF),
            expected_count=9
        )


    def test_finds_all_classes(self, lexer_of_code_file: Lexer) -> None:
        run_lexer_counter_test(
            lexer=lexer_of_code_file,
            expected_token=Token(value='class', type=TokenType.CLASS),
            expected_count=4
        )


    @pytest.mark.parametrize("str_value", ("I'm screaming!", "__main__", "Adam \\\" night"))
    def test_finds_all_string_values(self, lexer_of_code_file: Lexer, str_value: str) -> None:
        run_lexer_counter_test(
            lexer=lexer_of_code_file,
            expected_token=Token(value=str_value, type=TokenType.STR_LITERAL),
        )

    def test_finds_edge_case_identifiers(self, lexer_of_code_file: Lexer) -> None:
        run_lexer_counter_test(
            lexer=lexer_of_code_file,
            expected_token=Token(value='def_anon', type=TokenType.IDENTIFIER),
            expected_count=2
        )
        run_lexer_counter_test(
            lexer=lexer_of_code_file,
            expected_token=Token(value='classless_freak', type=TokenType.IDENTIFIER),
            expected_count=2
        )
        run_lexer_counter_test(
            lexer=lexer_of_code_file,
            expected_token=Token(value='__name__', type=TokenType.IDENTIFIER),
        )
        run_lexer_counter_test(
            lexer=lexer_of_code_file,
            expected_token=Token(value='__init__', type=TokenType.IDENTIFIER),
        )

    @pytest.mark.parametrize("int_value", ('-2', '3', '20', '10', '1', '0', '3_0'))
    def test_finds_all_int_values(self, lexer_of_code_file: Lexer, int_value: str) -> None:
        run_lexer_counter_test(
            lexer=lexer_of_code_file,
            expected_token=Token(value=int_value, type=TokenType.INT_LITERAL),
        )

    @pytest.mark.parametrize("float_value", ('2.5', '3.33'))
    def test_finds_all_float_values(self, lexer_of_code_file: Lexer, float_value: str) -> None:
        run_lexer_counter_test(
            lexer=lexer_of_code_file,
            expected_token=Token(value=float_value, type=TokenType.FLOAT_LITERAL),
        )
