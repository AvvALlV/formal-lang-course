from networkx import MultiDiGraph
from pyformlang.cfg import CFG, Variable

from project.cfg_utils import cfg_to_wсnf


def hellings(cfg: CFG, graph: MultiDiGraph):
    """
    Implementation of the Hellings algorithm
    :param cfg: the context-free grammar to query the graph
    :param graph: to analyze
    :return: set of tuples (start node, variable of the cfg, achievable node)
    """
    wcfg = cfg_to_wсnf(cfg)

    result = set()
    for production in wcfg.productions:
        if len(production.body) == 0:
            for node in graph.nodes:
                result.add((node, production.head, node))
        elif len(production.body) == 1:
            for u, v, data in graph.edges(data="label"):
                if Variable(data) == production.body[0]:
                    result.add((u, production.head, v))

    queue = list(result.copy())

    while len(queue) > 0:
        u, var, v = queue.pop()
        for u_res, var_res, v_res in result.copy():
            if v_res == u:
                for production in wcfg.productions:
                    if production.body == [var_res, var]:
                        p = (u_res, production.head, v)
                        if p not in result:
                            queue.append(p)
                            result.add(p)
            elif u_res == v:
                for production in wcfg.productions:
                    if production.body == [var, var_res]:
                        p = (u, production.head, v_res)
                        if p not in result:
                            queue.append(p)
                            result.add(p)

    return result


def cfpq(
    cfg: CFG,
    graph: MultiDiGraph,
    start_nodes=None,
    final_nodes=None,
    symbol=Variable("S"),
):
    """
    A function that allows solving the reachability problem for a given set of start and end
    vertices and a given nonterminal.
    :param cfg: the context-free grammer
    :param graph: the graph to analyze
    :param start_nodes: start vertices
    :param final_nodes: final vertices
    :param symbol: any nonterminal
    :return: dict { start_node: set of reachable final nodes}
    """
    if not start_nodes:
        start_nodes = set(graph.nodes)
    if not final_nodes:
        final_nodes = set(graph.nodes)

    result_hellings = hellings(cfg, graph)
    result = {u: set() for u in start_nodes}
    for u, var, v in result_hellings:
        if var == symbol and u in start_nodes and v in final_nodes:
            result[u].add(v)

    return result
