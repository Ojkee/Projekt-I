from abc import ABC, abstractmethod


class Expression(ABC):
    @abstractmethod
    def __eq__(self, value) -> bool:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass
