from project.cfpq import *
from project.graph_utils import create_labeled_two_cycles_graph


def test_hellings():
    # из конспекта:
    cfg = CFG.from_text(
        """
S -> A B
S -> A S1
S1 -> S B
A -> a
B -> b
"""
    )

    graph = create_labeled_two_cycles_graph(2, 1)
    result = hellings(cfg, graph)
    assert result == {
        (0, Variable("A"), 1),
        (1, Variable("A"), 2),
        (2, Variable("A"), 0),
        (0, Variable("B"), 3),
        (3, Variable("B"), 0),
        (2, Variable("S"), 3),
        (2, Variable("S1"), 0),
        (1, Variable("S"), 0),
        (1, Variable("S1"), 3),
        (0, Variable("S"), 3),
        (0, Variable("S1"), 0),
        (2, Variable("S"), 0),
        (2, Variable("S1"), 3),
        (1, Variable("S"), 3),
        (1, Variable("S1"), 0),
        (0, Variable("S"), 0),
        (0, Variable("S1"), 3),
    }


def test_matrix():
    # из конспекта:
    cfg = CFG.from_text(
        """
S -> A B
S -> A S1
S1 -> S B
A -> a
B -> b
"""
    )

    graph = create_labeled_two_cycles_graph(2, 1)
    result = matrix_mult(cfg, graph)
    assert result == {
        (0, Variable("A"), 1),
        (1, Variable("A"), 2),
        (2, Variable("A"), 0),
        (0, Variable("B"), 3),
        (3, Variable("B"), 0),
        (2, Variable("S"), 3),
        (2, Variable("S1"), 0),
        (1, Variable("S"), 0),
        (1, Variable("S1"), 3),
        (0, Variable("S"), 3),
        (0, Variable("S1"), 0),
        (2, Variable("S"), 0),
        (2, Variable("S1"), 3),
        (1, Variable("S"), 3),
        (1, Variable("S1"), 0),
        (0, Variable("S"), 0),
        (0, Variable("S1"), 3),
    }


def test_hellings_from_text():
    # из конспекта:
    graph = create_labeled_two_cycles_graph(2, 1)
    result = algo_from_text(
        """
S -> A B
S -> A S1
S1 -> S B
A -> a
B -> b
""",
        graph,
    )
    assert result == {
        (0, Variable("A"), 1),
        (1, Variable("A"), 2),
        (2, Variable("A"), 0),
        (0, Variable("B"), 3),
        (3, Variable("B"), 0),
        (2, Variable("S"), 3),
        (2, Variable("S1"), 0),
        (1, Variable("S"), 0),
        (1, Variable("S1"), 3),
        (0, Variable("S"), 3),
        (0, Variable("S1"), 0),
        (2, Variable("S"), 0),
        (2, Variable("S1"), 3),
        (1, Variable("S"), 3),
        (1, Variable("S1"), 0),
        (0, Variable("S"), 0),
        (0, Variable("S1"), 3),
    }


def test_cfpq_hellings():
    cfg = CFG.from_text(
        """
S -> A B
S -> A S1
S1 -> S B
A -> a
B -> b
"""
    )
    graph = create_labeled_two_cycles_graph(2, 1)
    result = cfpq(cfg, graph)
    assert result == {0: {0, 3}, 1: {0, 3}, 2: {0, 3}, 3: set()}


def test_cfpq_matrix():
    cfg = CFG.from_text(
        """
S -> A B
S -> A S1
S1 -> S B
A -> a
B -> b
"""
    )
    graph = create_labeled_two_cycles_graph(2, 1)
    result = cfpq(cfg, graph, algo=cfpqAlgo.MATRIX)
    assert result == {0: {0, 3}, 1: {0, 3}, 2: {0, 3}, 3: set()}


def test_cfpq_from_text():
    graph = create_labeled_two_cycles_graph(2, 1)
    result = cfpq_from_text(
        """
S -> A B
S -> A S1
S1 -> S B
A -> a
B -> b
""",
        graph,
    )
    assert result == {0: {0, 3}, 1: {0, 3}, 2: {0, 3}, 3: set()}
