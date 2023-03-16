import project.bool_matrices as bm
import project.finite_automaton as fa
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton
import networkx as nx


def regular_path_querying(
    fa1: NondeterministicFiniteAutomaton, fa2: NondeterministicFiniteAutomaton
) -> NondeterministicFiniteAutomaton:
    """
    Intersections of two finite automaton
    :param fa1: first nondeterministic finite automaton
    :param fa2: second nondeterministic finite automaton
    :return: nondeterministic finite automaton which is the intersection of the other two
    """
    bool_fa1, bool_fa2 = bm.BoolMatrices(fa1), bm.BoolMatrices(fa2)
    return bool_fa1.intersect(bool_fa2).to_nfa()


def regular_requests_to_graph(
    regex: str,
    graph: nx.MultiDiGraph,
    start_states: set = None,
    final_states: set = None,
) -> set:
    """
    Given a graph with the given start and end vertices and a regular expression, returns those pairs of vertices
    from the given start and end vertices that are connected by a path that forms a word from the language given
    by the regular expression.
    :param regex: academic regular expression in string representation
    :param graph: the graph with field 'label' on edges for conversion to NFA
    :param start_states: iterable object with initial states, can be None
    :param final_states: iterable object with final states, can be None.
    :return: pairs of vertices from given start and end vertices that are connected by a path that
    forms a word from the language given by the regular expression.
    """
    nfa = fa.graph_to_nfa(graph, start_states, final_states)
    dfa = fa.regex_to_dfa(regex)

    bnfa, bdfa = bm.BoolMatrices(nfa), bm.BoolMatrices(dfa)

    bintersect = bnfa.intersect(bdfa)
    tc = bintersect.get_transitive_closure()

    result = set()
    for s1, s2 in zip(*tc.nonzero()):
        if s1 in bintersect.start_states and s2 in bintersect.final_states:
            result.add((s1 // bdfa.count_of_states, s2 // bdfa.count_of_states))

    return result
