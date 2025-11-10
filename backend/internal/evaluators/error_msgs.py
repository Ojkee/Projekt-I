from enum import IntEnum, unique, auto


@unique
class ErrorPrecedence(IntEnum):
    LOWEST = auto()


class EvaluatorErrorUserMsg:
    @staticmethod
    def no_input() -> str:
        return "No input"
