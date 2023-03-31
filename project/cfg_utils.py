from pyformlang.cfg import CFG
from textwrap import dedent


def cfg_to_wсnf(cfg: CFG):
    new_cfg = cfg.eliminate_unit_productions().remove_useless_symbols()
    new_productions = new_cfg._get_productions_with_only_single_terminals()
    new_productions = new_cfg._decompose_productions(new_productions)
    return CFG(start_symbol=new_cfg._start_symbol, productions=set(new_productions))


def cfg_from_file(filename: str):
    with open(filename) as f:
        return CFG.from_text(f.read())
