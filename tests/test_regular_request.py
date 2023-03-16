from networkx import MultiDiGraph
import project.regular_request as rr
import project.finite_automaton as fa


def test_request_intersect_nfa():
    regexes = [
        "bebs lex",
        "asf|asf",
        "abc def*",
        "(xyz* mem*)*",
    ]
    dfas = [fa.regex_to_dfa(expr) for expr in regexes]
    for fa1 in dfas:
        for fa2 in dfas:
            expected = fa1.get_intersection(fa2)
            got = rr.regular_path_querying(fa1, fa2)
            assert expected.is_equivalent_to(got)


def test_regular_requests_to_graph1():
    graph = MultiDiGraph()
    graph.add_edges_from(
        [
            (0, 1, {"label": "a"}),
            (1, 2, {"label": "b"}),
            (2, 3, {"label": "o"}),
            (3, 4, {"label": "r"}),
            (4, 5, {"label": "t"}),
        ]
    )
    assert rr.regular_requests_to_graph("a b o r t", graph) == {(0, 5)}


def test_regular_requests_to_graph2():
    graph = MultiDiGraph()
    assert rr.regular_requests_to_graph("something or someone", graph) == set()


def test_regular_requests_to_graph3():
    graph = MultiDiGraph()
    graph.add_edges_from(
        [
            (0, 1, {"label": "s"}),
            (1, 2, {"label": "o"}),
            (2, 3, {"label": "m"}),
            (3, 4, {"label": "t"}),
            (4, 5, {"label": "h"}),
            (5, 6, {"label": "i"}),
            (6, 7, {"label": "n"}),
            (8, 9, {"label": "g"}),
        ]
    )
    assert rr.regular_requests_to_graph("", graph) == set()
