from abc import ABC, abstractmethod


class Expression(ABC):
    @abstractmethod
    def debug_str(self) -> str:
        pass

    @abstractmethod
    def pretty_str(self) -> str:
        pass
