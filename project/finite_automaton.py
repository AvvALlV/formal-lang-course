from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
)
import networkx as nx


def regex_to_dfa(regex_str: str) -> DeterministicFiniteAutomaton:
    """
    Build deterministic finite automaton from a regular expression
    :param regex_str: academic regular expression in string representation
    :return: minimized deterministic finite automaton
    """

    regex = Regex(regex_str)
    nfa_from_regex = regex.to_epsilon_nfa()
    return nfa_from_regex.minimize()


def graph_to_nfa(
    graph: nx.MultiDiGraph, starts_states=None, final_states=None
) -> NondeterministicFiniteAutomaton:
    """
    Build nondeterministic finite automaton from directed graph
    :param graph: the graph with field 'label' on edges for conversion to NFA
    :param starts_states: iterable object with initial states, can be None
    :param final_states: iterable object with final states, can be None.
    :return: not minimized nfa
    """

    nfa_from_graph = NondeterministicFiniteAutomaton(graph.graph)

    if starts_states is None:
        starts_states = graph.nodes

    if final_states is None:
        final_states = graph.nodes

    for node in starts_states:
        nfa_from_graph.add_start_state(node)

    for node in final_states:
        nfa_from_graph.add_final_state(node)

    nfa_from_graph.add_transitions(
        [(u, data_dict["label"], v) for u, v, data_dict in graph.edges(data=True)]
    )

    return nfa_from_graph
