from typing import Generator
from _pytest.nodes import Node
from backend.internal.objects.eval_object import Object
from backend.internal.objects.result_object import ErrorObject


class AnyNonErrorObject(Object):
    def __str__(self) -> str:
        return type(self).__name__

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: Object) -> bool:
        if isinstance(other, ErrorObject):
            return False
        return True

    def __iter__(self) -> Generator[Node]:
        yield from ()


def wrap_obj(msg: str) -> ErrorObject:
    return ErrorObject(msg)
