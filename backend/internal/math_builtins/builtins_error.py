from typing import NamedTuple


class BuiltinsError(NamedTuple):
    msg: str


class NotMatchingParam(BuiltinsError): ...


class NotMatchingFormula(BuiltinsError): ...
