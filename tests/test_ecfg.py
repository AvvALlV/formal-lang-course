from  project.ecfg import ECFG
from pyformlang.cfg import Variable, CFG
from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import Symbol
from textwrap import dedent


def test_from_text():
    ecfg = ECFG.from_text(dedent("""
                                S->A.B
                                A->a*b
                                """))
    assert ecfg.start_symbol == Variable("S")
    assert ecfg.productions[Variable("S")].sons[0].head.value == Regex('A.B').sons[0].head.value
    assert ecfg.productions[Variable("S")].sons[1].head.value == Regex('A.B').sons[1].head.value
    assert ecfg.productions[Variable("A")].sons[0].head.value == Regex('a*b').sons[0].head.value
    assert ecfg.productions[Variable("A")].sons[1].head.value == Regex('a*b').sons[1].head.value

def test_from_cfg():
    cfg = CFG.from_text(
        dedent(
            """
        S -> A S B
        A -> a
        A -> b
        S -> epsilon
        W -> w
        B -> b
        """
        )
    )

    ecfg = ECFG.from_CFG(cfg)
    assert ecfg.start_symbol == Variable("S")
    assert ecfg.productions[Variable("A")].sons[0].head.value == Symbol('b') or Symbol('a')
    assert ecfg.productions[Variable("A")].sons[1].head.value == Symbol('b') or Symbol('a')
    assert ecfg.productions[Variable("B")].head.value == Symbol('b')
