from tempfile import NamedTemporaryFile
from pyformlang.cfg import Variable, Terminal, Production
import pyformlang.cfg

from project.cfg_utils import *


def test_cfg_to_wcnf():
    cfg = CFG.from_text(
        dedent(
            """
        S -> A S B
        A -> a
        S -> epsilon
        W -> w
        B -> b
        """
        )
    )
    cfg.to_normal_form()
    wcnf = cfg_to_wсnf(cfg)

    assert Variable("W") in cfg.variables
    assert Variable("W") not in wcnf.variables

    for production in wcnf.productions:
        assert len(production.body) <= 2

    assert Production("S", []) in wcnf.productions


def test_cfg_from_file():
    path = ""
    with NamedTemporaryFile(mode="w", delete=False) as f:
        f.write(
            dedent(
                """
                S -> A S B
                A -> a
                S -> epsilon
                W -> w
                B -> b
                """
            )
        )
        path = f.name

    cfg = cfg_from_file(path)
    assert not cfg.is_empty()
    assert cfg.terminals == {Terminal("a"), Terminal("b"), Terminal("w")}
    assert cfg.variables == {Variable("S"), Variable("A"), Variable("B"), Variable("W")}
    assert cfg.start_symbol == Variable("S")
