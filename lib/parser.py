from typing import List

from lib.ast_node import AstNode, AST_PATTERNS
from lib.token import Token


class Parser:
    ast: List[AstNode] = []
    tokens: List[Token] = []

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.parse()

    def print_ast(self):
        for node in self.ast:
            print(repr(node))

    def parse(self):
        print(f"Parsing tokens...")

        # TODO: Multiple parsing passes
        i = 0
        while i < len(self.tokens):
            token_slice = self.tokens[i:]
            for pattern_class in AST_PATTERNS:
                ast_node = pattern_class(token_slice).match()
                if ast_node:
                    self.ast.append(ast_node)
                    i += len(ast_node.tokens) - 1
                    break
            i += 1