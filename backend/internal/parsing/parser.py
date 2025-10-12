from enum import IntEnum, auto, unique
from typing import Callable, Optional

from backend.internal.statements import Statement, Formula, Subject, AtomTransform
from backend.internal.expressions import Expression, Identifier, Number, Prefix, Infix
from backend.internal.parsing.parseerror import ParseErr
from backend.internal.tokens import Token, TokenType
from backend.internal.tokenstreams import TokenStream
from backend.internal.ast import Program


@unique
class Precedence(IntEnum):
    LOWEST = auto()
    EQUALS = auto()
    PLUSMINUS = auto()
    MULDIV = auto()
    PREFIX = auto()
    POWER = auto()
    FUNCTION = auto()


precedences: dict[TokenType, Precedence] = {
    TokenType.EQUALS: Precedence.EQUALS,
    TokenType.LT: Precedence.EQUALS,
    TokenType.GT: Precedence.EQUALS,
    TokenType.PLUS: Precedence.PLUSMINUS,
    TokenType.MINUS: Precedence.PLUSMINUS,
    TokenType.ASTERISK: Precedence.MULDIV,
    TokenType.SLASH: Precedence.MULDIV,
    TokenType.CARET: Precedence.POWER,
}

prefix_expr_fn = Callable[[], Expression | ParseErr]
infix_expr_fn = Callable[[Expression], Expression | ParseErr]
prefix_atom_fn = Callable[[], Statement | ParseErr]


class Parser:
    def __init__(self, stream: TokenStream) -> None:
        self._stream = stream
        self._current: Optional[Token] = None
        self._peek: Optional[Token] = None

        self._prefix_fns: dict[TokenType, prefix_expr_fn] = {
            TokenType.IDENT: self._parse_identifier,
            TokenType.NUMBER: self._parse_number,
            TokenType.MINUS: self._parse_prefix_epxr,
            TokenType.LPAREN: self._parse_grouped_expr,
        }
        self._infix_fns: dict[TokenType, infix_expr_fn] = {
            TokenType.EQUALS: self._parse_infix_expr,
            TokenType.LT: self._parse_infix_expr,
            TokenType.GT: self._parse_infix_expr,
            TokenType.PLUS: self._parse_infix_expr,
            TokenType.MINUS: self._parse_infix_expr,
            TokenType.ASTERISK: self._parse_infix_expr,
            TokenType.SLASH: self._parse_infix_expr,
            TokenType.CARET: self._parse_infix_expr,
        }
        self._atom_fns: dict[TokenType, prefix_atom_fn] = {
            TokenType.NUMBER: self._parse_atom_div,
            TokenType.IDENT: self._parse_atom_div,
            TokenType.PLUS: self._parse_atom,
            TokenType.MINUS: self._parse_atom,
            TokenType.ASTERISK: self._parse_atom,
            TokenType.CARET: self._parse_atom,
        }

        self._advance_token()
        self._advance_token()

    def parse(self) -> Program:
        assert self._current
        program = Program()
        while self._current.ttype != TokenType.EOF:
            stmt = self._parse_statement()
            program.append(stmt)
            if self._current.ttype == TokenType.NEW_LINE:
                self._advance_token()
  

        return program

    def _advance_token(self) -> None:
        self._current = self._peek
        self._peek = self._stream.next()

    def _parse_statement(self) -> Statement | ParseErr:
        assert self._current
        match self._current.ttype:
            case TokenType.ILLEGAL:
                return self._parse_illegal()
            case TokenType.SLASH:
                return self._parse_command()
            case TokenType.BANG:
                return self._parse_formula()
        return self._parse_subject()

    def _parse_illegal(self) -> ParseErr:
        assert self._current
        msg = f"Illegal character: {self._current.literal}"
        err = ParseErr(msg)
        err.append("parse_illegal")
        return err

    def _parse_command(self) -> Statement | ParseErr:
        assert self._current
        self._advance_token()
        match self._current.ttype:
            case TokenType.NEW_LINE | TokenType.EOF:
                err = ParseErr("Empty line")
                err.append("parse_command")
                return err

        result = self._parse_atom_transform()
        if isinstance(result, ParseErr):
            result.append("parse_command")
        self._advance_token()
        return result

    def _parse_formula(self) -> Statement | ParseErr:
        assert self._current
        self._advance_token()
        ident = self._current
        self._advance_token()
        params = self._parse_comma_sep_params()
        if isinstance(params, ParseErr):
            params.append("parse_formula")
            return params
        return Formula(ident, params)

    def _parse_subject(self) -> Statement | ParseErr:
        expr = self._parse_expr(Precedence.LOWEST)
        if isinstance(expr, ParseErr):
            expr.append("parse_subject")
            return expr
        assert self._peek
        if self._new_line_or_eof(self._peek):
            self._advance_token()
        return Subject(expr)

    def _parse_comma_sep_params(self) -> list[Expression] | ParseErr:
        assert self._current
        params: list[Expression] = []
        while self._new_line_or_eof(self._current):
            param = self._parse_expr(Precedence.LOWEST)
            if isinstance(param, ParseErr):
                param.append("parse_comma_sep_params")
                return param
            params.append(param)
            self._advance_token()
            if self._current.ttype == TokenType.COMMA:
                self._advance_token()
        return params

    def _parse_atom_transform(self) -> Statement | ParseErr:
        assert self._current
        if not self._current.ttype in self._atom_fns:
            msg = f"Error near: `{self._current.literal}`"
            err = ParseErr(msg)
            err.append("parse_atom_transform", self._current)
            return err

        prefix = self._atom_fns[self._current.ttype]
        match prefix():
            case ParseErr() as err:
                err.append("parse_atom_transform")
                return err
            case stmt:
                return stmt

    def _parse_identifier(self) -> Identifier:
        assert self._current
        return Identifier(self._current)

    def _parse_number(self) -> Number | ParseErr:
        assert self._current
        try:
            num = float(self._current.literal)
            return Number(num)
        except:
            msg = f"Parsing number error for: {self._current.literal}"
            err = ParseErr(msg)
            err.append("parse_number", self._current)
            return err

    def _parse_expr(self, precedence: Precedence) -> Expression | ParseErr:
        assert self._current
        if not self._current.ttype in self._prefix_fns:
            err = ParseErr(f"Error near `{self._current.literal}`")
            err.append("no prefix fn in parse_expr", self._current)
            return err

        lhs = self._prefix_fns[self._current.ttype]()
        if isinstance(lhs, ParseErr):
            lhs.append("parse_expr", self._current)
            return lhs

        assert self._peek
        while (
            not self._new_line_or_eof(self._peek) and precedence < self._peek_precedence()
        ):
            if not self._peek.ttype in self._infix_fns:
                return lhs
            infix = self._infix_fns[self._peek.ttype]
            self._advance_token()
            lhs = infix(lhs)
            if isinstance(lhs, ParseErr):
                lhs.append("parse_expr")
                return lhs
        return lhs

    def _parse_prefix_epxr(self) -> Expression | ParseErr:
        assert self._current
        operator = self._current
        self._advance_token()
        rhs = self._parse_expr(Precedence.PREFIX)
        if isinstance(rhs, ParseErr):
            rhs.append("prase_prefix_expression", self._current)
            return rhs
        return Prefix(operator, rhs)

    def _parse_grouped_expr(self) -> Expression | ParseErr:
        assert self._current
        self._advance_token()
        expr = self._parse_expr(Precedence.LOWEST)
        if isinstance(expr, ParseErr):
            expr.append("parse_groped_expr", self._current)
            return expr
        assert self._peek
        if self._peek.ttype != TokenType.RPAREN:
            err = ParseErr("Parentheses should close, write: `)`")
            err.append("parse_groped_expr", self._current)
            return err
        self._advance_token()
        return expr

    def _parse_infix_expr(self, lhs: Expression) -> Expression | ParseErr:
        assert self._current
        operator = self._current
        precedence = self._current_precedence()
        self._advance_token()
        rhs = self._parse_expr(precedence)
        if isinstance(rhs, ParseErr):
            rhs.append("parse_infix_expr", self._current)
            return rhs
        return Infix(operator, lhs, rhs)

    def _parse_atom_div(self) -> Statement | ParseErr:
        assert self._current
        operator = Token(TokenType.SLASH, "/")
        expr = self._parse_expr(Precedence.LOWEST)
        if isinstance(expr, ParseErr):
            expr.append("parse_atom_div", self._current)
            return expr
        return AtomTransform(operator, expr)

    def _parse_atom(self) -> Statement | ParseErr:
        assert self._current
        operator = self._current
        self._advance_token()
        expr = self._parse_expr(Precedence.LOWEST)
        if isinstance(expr, ParseErr):
            expr.append("parse_atom_div", self._current)
            return expr
        return AtomTransform(operator, expr)

    def _new_line_or_eof(self, token: Token) -> bool:
        return token.ttype == TokenType.NEW_LINE or token.ttype == TokenType.EOF

    def _current_precedence(self) -> Precedence:
        assert self._current
        return self._get_precedence(self._current.ttype)

    def _peek_precedence(self) -> Precedence:
        assert self._peek
        return self._get_precedence(self._peek.ttype)

    def _get_precedence(self, ttype: TokenType) -> Precedence:
        if not ttype in precedences:
            return Precedence.LOWEST
        return precedences[ttype]

# --- IGNORE ---

