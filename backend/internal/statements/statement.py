from abc import ABC, abstractmethod


class Statement(ABC):
    @abstractmethod
    def __str__(self) -> str:
        pass
