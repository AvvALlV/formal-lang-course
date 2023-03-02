import pytest
import project.finite_automaton as fa
import project.graph_utils as gu
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton


def test_regex_to_dfa():
    expected_fa = NondeterministicFiniteAutomaton()
    expected_fa.add_start_state(0)
    expected_fa.add_final_state(1)
    expected_fa.add_transitions([(0, "aa", 1), (1, "bb", 1), (1, "cc", 1)])

    dfa = fa.regex_to_dfa("aa (bb+ cc*)*")

    assert expected_fa.is_equivalent_to(dfa)
    assert dfa.is_deterministic()
    min_dfa = dfa.minimize()
    assert dfa.is_equivalent_to(min_dfa)
    assert len(dfa.states) == len(min_dfa.states)
    assert dfa.get_number_transitions() == min_dfa.get_number_transitions()


def test_graph_to_nfa():
    graph_bzip = gu.get_graph_by_name("bzip")
    nfa_from_bzip = fa.graph_to_nfa(graph_bzip)

    assert graph_bzip.number_of_nodes() == len(nfa_from_bzip.states)
    assert len(nfa_from_bzip.final_states) == len(graph_bzip.nodes())
    assert len(nfa_from_bzip.start_states) == len(graph_bzip.nodes())

    graph_bzip = gu.get_graph_by_name("bzip")

    start_states, final_states = {1, 10, 150}, {2, 55, 60, 23}
    nfa_from_bzip = fa.graph_to_nfa(graph_bzip, start_states, final_states)

    assert graph_bzip.number_of_nodes() == len(nfa_from_bzip.states)
    assert nfa_from_bzip.start_states == start_states
    assert nfa_from_bzip.final_states == final_states
