from lib.ast_node import AstNode, AstNodeType
from lib.lexer import Lexer
from lib.parser import Parser
from lib.token import TokenType, Token
import pathlib
import pytest

base_path = pathlib.Path(__file__).parent.resolve() / "test_data"
CODE_FILE_PATH = (base_path / "example.py").as_posix()


def run_parser_test(parser: Parser, expected_node: AstNode):
    assert expected_node in parser.ast, parser.ast


@pytest.fixture(scope="module")
def parser_of_code_file() -> Parser:
    lexer = Lexer(CODE_FILE_PATH)
    return Parser(lexer.tokens)


class TestDef:
    def test_identifies_def_without_arguments(self, parser_of_code_file: Parser):
        run_parser_test(
            parser=parser_of_code_file,
            expected_node=AstNode(type=AstNodeType.DEF, tokens=[
                Token(value='def', type=TokenType.DEF),
                Token(value='func_without_args', type=TokenType.IDENTIFIER),
                Token(value='(', type=TokenType.OPEN_PAREN),
                Token(value=')', type=TokenType.CLOSE_PAREN),
                Token(value=':', type=TokenType.COLON)
            ])
        )


class TestClass:
    @pytest.mark.parametrize("class_name", ("SuperException", "Foo"))
    def test_identifies_class_without_arguments(self, parser_of_code_file: Parser, class_name: str):
        run_parser_test(
            parser=parser_of_code_file,
            expected_node=AstNode(type=AstNodeType.CLASS, tokens=[
                Token(value='class', type=TokenType.CLASS),
                Token(value=class_name, type=TokenType.IDENTIFIER),
                Token(value=':', type=TokenType.COLON)
            ])
        )

    def test_identifies_class_with_one_argument(self, parser_of_code_file: Parser):
        run_parser_test(
            parser=parser_of_code_file,
            expected_node=AstNode(type=AstNodeType.CLASS, tokens=[
                Token(value='class', type=TokenType.CLASS),
                Token(value='Bar', type=TokenType.IDENTIFIER),
                Token(value='(', type=TokenType.OPEN_PAREN),
                Token(value='Foo', type=TokenType.IDENTIFIER),
                Token(value=')', type=TokenType.CLOSE_PAREN),
                Token(value=':', type=TokenType.COLON)
            ])
        )

    def test_identifies_class_with_multiple_arguments(self, parser_of_code_file: Parser):
        run_parser_test(
            parser=parser_of_code_file,
            expected_node=AstNode(type=AstNodeType.CLASS, tokens=[
                Token(value='class', type=TokenType.CLASS),
                Token(value='Baz', type=TokenType.IDENTIFIER),
                Token(value='(', type=TokenType.OPEN_PAREN),
                Token(value='Foo', type=TokenType.IDENTIFIER),
                Token(value=',', type=TokenType.COMMA),
                Token(value='Bar', type=TokenType.IDENTIFIER),
                Token(value=',', type=TokenType.COMMA),
                Token(value='SuperException', type=TokenType.IDENTIFIER),
                Token(value=')', type=TokenType.CLOSE_PAREN),
                Token(value=':', type=TokenType.COLON)
            ])
        )

class TestImport:
    def test_identifies_import_statement(self, parser_of_code_file: Parser):
        run_parser_test(
            parser=parser_of_code_file,
            expected_node=AstNode(type=AstNodeType.IMPORT, tokens=[
                Token(value='import', type=TokenType.IMPORT),
                Token(value='sys', type=TokenType.IDENTIFIER),
            ])
        )

    def test_identifies_import_from_statement_with_one_submodule(self, parser_of_code_file: Parser):
        run_parser_test(
            parser=parser_of_code_file,
            expected_node=AstNode(type=AstNodeType.IMPORT, tokens=[
                Token(value='from', type=TokenType.FROM),
                Token(value='typing', type=TokenType.IDENTIFIER),
                Token(value='import', type=TokenType.IMPORT),
                Token(value='List', type=TokenType.IDENTIFIER),
            ])
        )