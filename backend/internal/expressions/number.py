from backend.internal.expressions import Expression


class Number(Expression):
    def __init__(self, value: float) -> None:
        super().__init__()
        self.value: float = value

    def __eq__(self, other):
        return isinstance(other, Number) and self.value == other.value

    def __repr__(self) -> str:
        return f"NUMBER({self.value})"

    def pretty_str(self) -> str:
        return self._number_to_str()

    def _number_to_str(self) -> str:
        if self.value.is_integer():
            return str(int(self.value))
        return f"{self.value:.3f}".rstrip("0")
