from enum import IntEnum, unique, auto


@unique
class ErrorPrecedence(IntEnum):
    LOWEST = auto()
    MISSING_EXPR = auto()
    MISSING_FORMULA_NAME = auto()
    MISSING_RHS_EXPR = auto()
    MISSING_RPAREN = auto()
    ILLEGAL_CHAR = auto()


class ParserErrorUserMsg:
    @staticmethod
    def illegal_str(illegal: str) -> str:
        return f"Illegal character: {illegal}"

    @staticmethod
    def extra_input_in_line(next_str: str) -> str:
        return f"Extra character: {next_str} after the expression. Maybe move to next line?"

    @staticmethod
    def missing_rhs_in_expr(lhs: str, op: str) -> str:
        return f"The expression `{lhs} {op}` is incomplete, something should come after the operator"

    @staticmethod
    def invalid_prefix(current: str) -> str:
        return f"Expression can't start with `{current}`"

    @staticmethod
    def no_rparen() -> str:
        return "Parentheses should close, write: `)`"

    @staticmethod
    def unexpected_eof() -> str:
        return "It looks like the expression ended before it was complete"

    @staticmethod
    def expected_expression_after(prev: str | None = None) -> str:
        ret = "Expected expression"
        if prev:
            ret += f" after: `{prev}`"
        return ret

    @staticmethod
    def invalid_atom_prefix(current: str) -> str:
        return f"Can't do much with `{current}` after `/`, try `+`/`-`/`*`/`^`"

    @staticmethod
    def no_formula_name() -> str:
        return "There should be formula name after `!`"

    @staticmethod
    def missing_comma_in_formula() -> str:
        return "There should be comma `,` between parameters"
