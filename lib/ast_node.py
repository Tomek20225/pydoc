from abc import abstractmethod, ABC, abstractstaticmethod
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Type

from lib.token import TokenType, Token


class AstNodeType(Enum):
    CLASS = 'CLASS'
    IMPORT = 'IMPORT'


@dataclass
class AstNode:
    tokens: List[Token]
    type: AstNodeType


@dataclass
class AstPatternElement:
    token: TokenType
    optional: bool = False


class AstPattern(ABC):
    cursor = -1
    tokens: List[Token] = []
    type: AstNodeType

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens

    def reset_cursor(self):
        self.cursor = -1

    def get_current_token(self):
        return self.tokens[self.cursor]

    def get_next_token(self) -> Token:
        self.cursor += 1
        return self.get_current_token()

    def is_current_token_type(self, token_type: TokenType) -> bool:
        token = self.get_current_token()
        return token.type == token_type

    def is_next_token_type(self, token_type: TokenType) -> bool:
        next_token = self.get_next_token()
        return next_token.type == token_type

    def get_resulting_node(self) -> AstNode:
        amount = self.cursor + 1
        return AstNode(tokens=self.tokens[0:amount], type=self.type)

    @abstractmethod
    def match(self) -> Optional[AstNode]:
        pass


class AstClassPattern(AstPattern):
    type = AstNodeType.CLASS

    def match(self) -> Optional[AstNode]:
        if not self.is_next_token_type(TokenType.CLASS):
            return None
        if not self.is_next_token_type(TokenType.IDENTIFIER):
            return None
        if self.is_next_token_type(TokenType.COLON):
            return self.get_resulting_node()
        if not self.is_current_token_type(TokenType.OPEN_PAREN):
            return None
        # TODO: Multiple comma-separated identifiers
        if not self.is_next_token_type(TokenType.IDENTIFIER):
            return None
        if not self.is_next_token_type(TokenType.CLOSE_PAREN):
            return None
        if self.is_next_token_type(TokenType.COLON):
            return self.get_resulting_node()
        return None

        # TODO: Class properties
        # TODO: Class methods


class AstImportPattern(AstPattern):
    type = AstNodeType.IMPORT

    def match_import_part(self) -> Optional[AstNode]:
        if not self.is_next_token_type(TokenType.IMPORT):
            return None
        # TODO: Multiple comma-separated identifiers
        if self.is_next_token_type(TokenType.IDENTIFIER):
            return self.get_resulting_node()
        return None

    def match(self) -> Optional[AstNode]:
        if self.is_next_token_type(TokenType.FROM):
            if not self.is_next_token_type(TokenType.IDENTIFIER):
                return None
            return self.match_import_part()

        self.reset_cursor()
        return self.match_import_part()



AST_PATTERNS: List[Type[AstPattern]] = [AstImportPattern, AstClassPattern]
