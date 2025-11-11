from abc import ABC, abstractmethod
from typing import Generator

from backend.internal.expression_tree.node import Node


class Object(ABC):
    @abstractmethod
    def __iter__(self) -> Generator[Node]:
        yield from ()
