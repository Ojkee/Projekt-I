from backend.internal.expressions import Expression
from backend.internal.statements import Statement
from backend.internal.tokens import Token


class Formula(Statement):
    def __init__(self, name: Token, params: list[Expression]) -> None:
        self._name = name
        self._params = params

    def to_str(self) -> str:
        params_str = map(lambda param: param.pretty_str(), self._params)
        buffer = [
            self._name.literal,
            " ",
            ", ".join(params_str),
        ]
        return "".join(buffer)
