from copy import deepcopy
from typing import Callable, TypeAlias

from backend.internal.evaluators.error_msgs import EvaluatorErrorUserMsg
from backend.internal.expression_tree.node import Node, Pow, Numeric, Mul, Add
from backend.internal.objects.result_object import SubjectObject


CheckerFn: TypeAlias = Callable[[Node], bool]


def is_zero_div(node: Node) -> bool:
    match node:
        case Pow(base, exponent):
            base = deepcopy(base).reduce()
            exponent = deepcopy(exponent).reduce()
            if not valid_pow(base, exponent):
                return True
            return is_zero_div(base) or is_zero_div(exponent)
        case Mul(left, right):
            return is_zero_div(left) or is_zero_div(right)
        case Add(left, right):
            return is_zero_div(left) or is_zero_div(right)
    return False


class Validator:
    checkers: list[tuple[CheckerFn, str]] = [
        (is_zero_div, EvaluatorErrorUserMsg.zero_division()),
    ]

    @staticmethod
    def check(subject: SubjectObject) -> str | None:
        for root in subject:
            for checker, msg in Validator.checkers:
                if checker(root):
                    return msg
        return None


def valid_pow(base: Node, exponent: Node) -> bool:
    match base, exponent:
        case Numeric(0.0), Numeric(value) if value < 0:
            return False
    return True
