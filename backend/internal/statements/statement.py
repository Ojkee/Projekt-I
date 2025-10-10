from abc import ABC, abstractmethod


class Statement(ABC):
    @abstractmethod
    def to_str(self) -> str:
        pass
