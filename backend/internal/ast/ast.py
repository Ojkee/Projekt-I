from backend.internal.ast import ASTNode


class Program(ASTNode):
    def __init__(self) -> None:
        self._stmts: list["Statement"] = []

    def append(self, stmt: "Statement") -> None:
        self._stmts.append(stmt)

    def get(self) -> list["Statement"]:
        return self._stmts
