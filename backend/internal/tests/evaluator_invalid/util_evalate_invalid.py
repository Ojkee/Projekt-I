from backend.internal.objects.eval_object import Object
from backend.internal.objects.result_object import ErrorObject


class AnyNonErrorObject(Object):
    def __str__(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: Object) -> bool:
        if isinstance(other, ErrorObject):
            return False
        return True


def wrap(msg: str) -> ErrorObject:
    return ErrorObject(msg)
