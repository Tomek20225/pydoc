from lib.ast_node import AstNode, AstNodeType
from lib.lexer import Lexer
from lib.parser import Parser
import pathlib

from lib.token import TokenType, Token

base_path = pathlib.Path(__file__).parent.resolve() / "test_data"
CODE_FILE_PATH = (base_path / "example.py").as_posix()


def run_parser_test(path: str, expected_node: AstNode):
    lexer = Lexer(path)
    parser = Parser(lexer.tokens)
    assert expected_node in parser.ast, parser.ast


class TestDef:
    def test_identifies_simple_def(self):
        run_parser_test(
            path=CODE_FILE_PATH,
            expected_node=AstNode(type=AstNodeType.DEF, tokens=[
                Token(type=TokenType.DEF, value='def'),
                Token(value='func_without_args', type=TokenType.IDENTIFIER),
                Token(value='(', type=TokenType.OPEN_PAREN),
                Token(value=')', type=TokenType.CLOSE_PAREN),
                Token(value=':', type=TokenType.COLON)
            ])
        )


class TestClass:
    def test_identifies_class_without_arguments(self):
        run_parser_test(
            path=CODE_FILE_PATH,
            expected_node=AstNode(type=AstNodeType.CLASS, tokens=[
                Token(type=TokenType.CLASS, value='class'),
                Token(value='Foo', type=TokenType.IDENTIFIER),
                Token(value=':', type=TokenType.COLON)
            ])
        )

    def test_identifies_class_with_one_argument(self):
        run_parser_test(
            path=CODE_FILE_PATH,
            expected_node=AstNode(type=AstNodeType.CLASS, tokens=[
                Token(type=TokenType.CLASS, value='class'),
                Token(value='Bar', type=TokenType.IDENTIFIER),
                Token(value='(', type=TokenType.OPEN_PAREN),
                Token(value='Foo', type=TokenType.IDENTIFIER),
                Token(value=')', type=TokenType.CLOSE_PAREN),
                Token(value=':', type=TokenType.COLON)
            ])
        )
