from backend.internal.expressions import Expression
from backend.internal.statements import Statement
from backend.internal.tokens import Token


class Formula(Statement):
    def __init__(self, name: Token, params: list[Expression]) -> None:
        self._name = name
        self._params = params

    def __repr__(self) -> str:
        return f"FORMULA({str(self)})"

    def __str__(self) -> str:
        params_str = ", ".join(map(str, self._params))
        return f"'{self._name.literal}' {params_str}"

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, Formula)
            and self._name == other._name
            and self.params == other.params
        )

    @property
    def name(self) -> Token:
        return self._name

    @property
    def params(self) -> list[Expression]:
        return self._params
