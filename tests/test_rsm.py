from project.ecfg import ECFG
from project.rsm import RSM
from project.finite_automaton import regex_to_dfa
from pyformlang.cfg import Variable, CFG
from pyformlang.regular_expression import Regex
from textwrap import dedent


def test_ecfg_to_rsm():
    cfg = CFG.from_text(
        dedent(
            """
        S -> A S B
        A -> a
        A -> b
        W -> w
        B -> b
        """
        )
    )

    ecfg = ECFG.from_CFG(cfg)
    rsm = RSM.ecfg_to_rsm(ecfg)
    assert rsm.boxes[Variable("B")] == Regex("b").to_epsilon_nfa()
    assert rsm.boxes[Variable("W")] == Regex("w").to_epsilon_nfa()
    assert rsm.boxes[Variable("S")] == Regex("A.(S.B)").to_epsilon_nfa()
    assert rsm.boxes[Variable("A")] == Regex("a|b").to_epsilon_nfa()


def test_rsm_minimize():
    cfg = CFG.from_text(
        dedent(
            """
        S -> A S B
        A -> a
        A -> b
        W -> w
        B -> b
        """
        )
    )

    ecfg = ECFG.from_CFG(cfg)
    rsm = RSM.ecfg_to_rsm(ecfg)
    rsm.minimize()
    assert rsm.boxes[Variable("B")] == Regex("b").to_epsilon_nfa().minimize()
    assert rsm.boxes[Variable("W")] == Regex("w").to_epsilon_nfa().minimize()
    assert rsm.boxes[Variable("S")] == Regex("A.(S.B)").to_epsilon_nfa().minimize()
    assert rsm.boxes[Variable("A")] == Regex("a|b").to_epsilon_nfa().minimize()
