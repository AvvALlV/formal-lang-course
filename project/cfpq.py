import numpy as np
from networkx import MultiDiGraph
from pyformlang.cfg import CFG, Variable
from scipy.sparse import dok_matrix
from enum import Enum
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


def matrix_mult(cfg: CFG, graph: MultiDiGraph):
    """
    Implementation of the Matrix Algorithm for Solving Reachability Problems with CS Constraints
    :param cfg: the context-free grammar to query the graph
    :param graph: to analyze
    :return: set of tuples (start node, variable of the cfg, achievable node)
    """
    wcfg = cfg_to_wсnf(cfg)

    nodes = list(graph.nodes)
    n = len(nodes)
    matrices = {var: dok_matrix((n, n), dtype=np.bool_) for var in wcfg.variables}

    var_productions = {}
    for production in wcfg.productions:
        if len(production.body) == 0:
            for i in range(n):
                matrices[production.head][i, i] = True
        elif len(production.body) == 1:
            for u, v, label in graph.edges(data="label"):
                i = nodes.index(u)
                j = nodes.index(v)
                if Variable(label) == production.body[0]:
                    matrices[production.head][i, j] = True
        elif len(production.body) == 2:
            var1 = Variable(production.body[0].value)
            var2 = Variable(production.body[1].value)
            if (var1, var2) not in var_productions:
                var_productions[(var1, var2)] = set()
            var_productions[(var1, var2)].add(production.head)

    matrices_changed = True
    while matrices_changed:
        matrices_changed = False
        for production in wcfg.productions:
            if len(production.body) != 2:
                continue
            else:
                var1 = Variable(production.body[0].value)
                var2 = Variable(production.body[1].value)
                for i in range(n):
                    for j in range(n):
                        for k in range(n):
                            if (
                                matrices[var1][i, j]
                                and matrices[var2][j, k]
                                and not matrices[production.head][i, k]
                            ):
                                matrices[production.head][i, k] = True
                                matrices_changed = True
    result = set()
    for var in wcfg.variables:
        rows, cols = matrices[var].nonzero()
        for i in range(len(rows)):
            result.add((nodes[rows[i]], var, nodes[cols[i]]))
    return result


class cfpqAlgo(Enum):
    HELLINGS = hellings
    MATRIX = matrix_mult


def algo_from_text(cfg: str, graph: MultiDiGraph, algo: cfpqAlgo = cfpqAlgo.HELLINGS):
    return algo(CFG.from_text(cfg), graph)


def algo_from_file(
    filename: str, graph: MultiDiGraph, algo: cfpqAlgo = cfpqAlgo.HELLINGS
):
    with open(filename) as f:
        return algo(CFG.from_text(f.read()), graph)


def cfpq(
    cfg: CFG,
    graph: MultiDiGraph,
    start_nodes=None,
    final_nodes=None,
    symbol=Variable("S"),
    algo: cfpqAlgo = cfpqAlgo.HELLINGS,
):
    """
    A function that allows solving the reachability problem for a given set of start and end
    vertices and a given nonterminal.
    :param cfg: the context-free grammer
    :param graph: the graph to analyze
    :param start_nodes: start vertices
    :param final_nodes: final vertices
    :param symbol: any nonterminal
    :param algo: algorithm for find cfpq
    :return: dict { start_node: set of reachable final nodes}
    """
    if not start_nodes:
        start_nodes = set(graph.nodes)
    if not final_nodes:
        final_nodes = set(graph.nodes)

    result_hellings = algo(cfg, graph)
    result = {u: set() for u in start_nodes}
    for u, var, v in result_hellings:
        if var == symbol and u in start_nodes and v in final_nodes:
            result[u].add(v)

    return result


def cfpq_from_text(
    cfg: str,
    graph: MultiDiGraph,
    start_nodes=None,
    final_nodes=None,
    symbol=Variable("S"),
    algo: cfpqAlgo = cfpqAlgo.HELLINGS,
):
    return cfpq(CFG.from_text(cfg), graph, start_nodes, final_nodes, symbol, algo)


def cfpq_from_file(
    filename: str,
    graph: MultiDiGraph,
    start_nodes=None,
    final_nodes=None,
    symbol=Variable("S"),
    algo: cfpqAlgo = cfpqAlgo.HELLINGS,
):
    with open(filename) as f:
        return cfpq(
            CFG.from_text(f.read(filename)),
            graph,
            start_nodes,
            final_nodes,
            symbol,
            algo,
        )
