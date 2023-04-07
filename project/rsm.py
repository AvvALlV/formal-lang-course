import pyformlang.cfg
from project.ecfg import ECFG
from project.bool_matrices import BoolMatrices


class RSM:
    """
    Implement recursive state machine
    """

    def __init__(self, start_symbols, boxes):
        self.start_symbols, self.boxes = start_symbols, boxes

    def minimize(self):
        """
        Minimize nfa for each symbol
        :return: minimized rsm
        """
        for key, value in self.boxes.items():
            self.boxes[key] = value.minimize()

        return self

    def to_bool_matices(self):
        matrices = {}
        for key, value in self.boxes.items():
            matrices[key] = BoolMatrices(value)

        return matrices

    @staticmethod
    def ecfg_to_rsm(ecfg: ECFG):
        """
        Convert ecfg to rsm
        :param ecfg: ecfg
        :return: rsm derived from ecfg
        """
        boxes = {}
        for variable, regex in ecfg.productions.items():
            boxes[variable] = regex.to_epsilon_nfa()

        return RSM(ecfg.start_symbol, boxes)
