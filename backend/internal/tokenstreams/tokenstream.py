from backend.internal.lexing import Lexer
from backend.internal.tokens import Token, TokenType


class TokenStream:
    def __init__(self, lexer: Lexer) -> None:
        self._read_idx: int = 0
        self._tokens: list[Token] = lexer.tokenize()

        self._mul_dict: dict[TokenType, set[TokenType]] = {
            TokenType.IDENT: {TokenType.NUMBER, TokenType.LPAREN},
            TokenType.NUMBER: {TokenType.IDENT, TokenType.LPAREN},
            TokenType.RPAREN: {TokenType.IDENT, TokenType.NUMBER, TokenType.LPAREN},
        }

        self._preprocess()

    def preprocess(self) -> list[Token]:
        return self._tokens

    def next(self) -> Token:
        token = self._tokens[self._read_idx]
        if token.ttype != TokenType.EOF:
            self._read_idx += 1
        return token

    def _preprocess(self) -> None:
        tokens: list[Token] = []

        i: int = 0
        while i < len(self._tokens) - 1:
            current = self._tokens[i]
            next = self._tokens[i + 1]

            if current.ttype == TokenType.BANG:
                i += 2
                tokens.append(current)
                tokens.append(next)
                continue
            if current.ttype == TokenType.IDENT and len(current.literal) > 1:
                idents = self._mul_split(current.literal)
                tokens.extend(idents)
            else:
                tokens.append(current)
            if self._should_mul_between(current.ttype, next.ttype):
                tokens.append(Token(TokenType.ASTERISK, "*"))
            i += 1
        last = self._tokens[len(self._tokens) - 1]
        tokens.append(last)
        self._tokens = tokens

    def _mul_split(self, ident: str) -> list[Token]:
        value: list[Token] = []
        for i, sym in enumerate(ident):
            token = Token(TokenType.IDENT, sym)
            value.append(token)
            if i < len(ident) - 1:
                value.append(Token(TokenType.ASTERISK, "*"))

        return value

    def _should_mul_between(self, lhs: TokenType, rhs: TokenType) -> bool:
        if lhs in self._mul_dict and rhs in self._mul_dict[lhs]:
            return True
        return False
