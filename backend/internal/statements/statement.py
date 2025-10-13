from abc import ABC, abstractmethod
from backend.internal.ast.astNode import ASTNode

class Statement(ASTNode, ABC):
    @abstractmethod
    def __str__(self) -> str:
        pass
