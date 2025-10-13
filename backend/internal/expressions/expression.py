from abc import ABC, abstractmethod
from backend.internal.ast import ASTNode

class Expression(ASTNode, ABC):
    @abstractmethod
    def __eq__(self, value) -> bool:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def pretty_str(self) -> str:
        pass
