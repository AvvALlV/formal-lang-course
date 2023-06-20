from typing import List, Dict
from project.interpreter.Types import Type
from project.interpreter.Exceptions import *


class Memory:
    def __init__(self):
        self.tables: List[Dict[str:Type]] = [{}]

    def next_scope(self):
        new_table = Memory()

        new_table.tables = self.tables.copy()
        new_table.tables.append({})

        return new_table

    def previous_scope(self):
        new_table = Memory()

        new_table.tables = self.tables.copy()
        new_table.tables = new_table.tables[:-1]

        return new_table

    def add_variable(self, name: str, value: Type, level: int = -1):
        if level >= len(self.tables):
            for _ in range(level - len(self.tables) + 1):
                self.tables.append({})

        self.tables[level][name] = value

    def find_variable(self, name: str):
        level = len(self.tables) - 1

        while level >= 0:
            value = self.tables[level].get(name)

            if value is not None:
                return value

            level -= 1

        raise VariableNotFoundException(name)
