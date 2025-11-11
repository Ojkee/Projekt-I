from copy import deepcopy
from typing import Callable, TypeAlias

from backend.internal.evaluators.error_msgs import EvaluatorErrorUserMsg
from backend.internal.expression_tree import Node, Pow, Numeric, Mul, Add
from backend.internal.objects.eval_object import Object


CheckerFn: TypeAlias = Callable[[Node], bool]


checkers: list[tuple[CheckerFn, str]] = []


def register(msg: str):
    def decorate(func: CheckerFn):
        checkers.append((func, msg))

    return decorate

class Validator:
    @staticmethod
    def check(obj: Object) -> str | None:
        for root in obj:
            reduced = deepcopy(root).reduce()
            for checker, msg in checkers:
                if Validator._dfs_check(reduced, checker):
                    return msg
        return None

    @staticmethod
    def _dfs_check(node: Node, checker: CheckerFn) -> bool:
        if checker(node):
            return True

        match node:
            case Add(a, b) | Mul(a, b) | Pow(a, b):
                lhs = Validator._dfs_check(a, checker)
                rhs = Validator._dfs_check(b, checker)
                return lhs or rhs

        return False


@register(EvaluatorErrorUserMsg.zero_division())
def is_zero_div(node: Node) -> bool:
    match node:
        case Pow(Numeric(0.0), Numeric(b)) if b < 0:
            return True
    return False


@register(EvaluatorErrorUserMsg.negative_root())
def is_negative_root(node: Node) -> bool:
    match node:
        case Pow(Numeric(a), Numeric(b)) if a < 0 and 0 < b and b < 1:
            return True
    return False
