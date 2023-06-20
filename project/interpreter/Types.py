from abc import ABC, abstractmethod


class Type(ABC):
    """
    Abstract base class for interpreter types.
    """

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def intersect(self, other):
        pass

    @abstractmethod
    def union(self, other):
        pass

    @abstractmethod
    def concatenate(self, other):
        pass

    @abstractmethod
    def inverse(self):
        pass

    @abstractmethod
    def kleene(self):
        pass
