from pyformlang.cfg import CFG, Terminal, Variable
from pyformlang.regular_expression import Regex


class ECFG:
    """
    Class implements extended context free grammar
    """

    def __init__(self, start_symbol, productions):
        self.start_symbol, self.productions = start_symbol, productions

    @staticmethod
    def from_text(text, start_symbol=Variable("S")):
        """
        Convert ecfg in text view to ECFG
        :param text:  in text view
        :param start_symbol: start symbol
        :return: ECFG
        """
        variables = set()
        productions = {}
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            production_objects = line.split("->")
            if len(production_objects) != 2:
                raise Exception(f"Invalid production line: {repr(line)}")

            head_text, body_text = production_objects
            head = Variable(head_text.strip())
            if head in variables:
                raise Exception(f"Rule for variable {head} encountered twice")
            variables.add(head)
            body = Regex(body_text)
            productions[head] = body

        return ECFG(start_symbol, productions)

    @staticmethod
    def from_CFG(cfg: CFG) -> "ECFG":
        """
        Convert cfg to ecfg
        :param cfg: lib cfg
        :return: ECFG
        """
        productions = {}
        for production in cfg.productions:
            regex = Regex(
                ".".join(variable.value for variable in production.body)
                if len(production.body) > 0
                else ""
            )
            productions[production.head] = regex if production.head not in productions else productions[
                production.head].union(regex)

        return ECFG(cfg.start_symbol, productions)
