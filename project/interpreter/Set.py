from project.interpreter.Types import *
from project.interpreter.Exceptions import *


class Set(Type):
    def __init__(self, iset: set):
        self._type = self.getType(iset)
        self._set = iset

    def __len__(self):
        return len(self._set)

    def __str__(self):
        return "{" + ", ".join(map(lambda x: str(x), self._set)) + "}"

    @property
    def type(self):
        return self._type

    @property
    def set(self):
        return self._set

    @staticmethod
    def getType(s: set) -> type:
        if len(s) == 0:
            return type(None)

        iter_seq = iter(s)

        return type(next(iter_seq))

    @staticmethod
    def _typeConsistency(s: set) -> bool:
        if len(s) == 0:
            return True

        iter_seq = iter(s)
        t = type(next(iter_seq))

        return all(map(lambda x: isinstance(x, t), iter_seq))

    def fromSet(self, oset: set):
        if not Set._typeConsistency(oset):
            raise TypingError("Inonsistent types in a set")
        return Set(oset)

    def intersect(self, other: "Set") -> "Set":
        if self._set and other._set and self._type != other._type:
            raise TypingError(
                f"Types mismatched: {self._type} not equals {other._type}."
            )
        return Set(self._set & other._set)

    def union(self, other: "Set") -> "Set":
        if self._set and other._set and self._type != other._type:
            raise TypingError(
                f"Types mismatched: {self._type} not equals {other._type}."
            )
        return Set(self._set | other._set)

    def concatenate(self, other):
        raise NotImplementedException("Use union operation for sets.")

    def inverse(self):
        raise NotImplementedException("Set does not support 'NOT' operation.")

    def kleene(self):
        raise NotImplementedException("Set does not support '*' operation.")

    def find(self, value):
        return value in self._set
