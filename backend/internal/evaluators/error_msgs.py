from enum import IntEnum, unique, auto


@unique
class ErrorPrecedence(IntEnum):
    LOWEST = auto()


class EvaluatorErrorUserMsg:
    @staticmethod
    def no_input() -> str:
        return "No input"

    @staticmethod
    def no_expr() -> str:
        return "First line must be equation or expression"

    @staticmethod
    def zero_division() -> str:
        return "Can't divide by zero"
