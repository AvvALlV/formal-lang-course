from scipy import sparse
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton


class BoolMatrices:
    """
    Сlass implements boolean decomposition
    """
    def __init__(self, nfa: NondeterministicFiniteAutomaton = None):
        if nfa is None:
            self.states, self.start_states, self.final_states, self.states_indices = set(), set(), set(), dict()
            self.bool_matrcies, self.count_of_states = dict(), 0
        else:
            self.states, self.start_states, self.final_states = nfa.states, nfa.start_states, nfa.final_states
            self.states_indices = {state: index for index, state in enumerate(nfa.states)}

            self.count_of_states = len(self.states)
            self.bool_matrcies = dict()
            for from_v, label, to_v in nfa:
                label_matrix = self.bool_matrcies.setdefault(label,
                                                             sparse.dok_matrix(
                                                                 (self.count_of_states, self.count_of_states),
                                                                 dtype=bool))
                label_matrix[self.states_indices[from_v], self.states_indices[to_v]] = True

    def intersect(self, other: 'BoolMatrices') -> 'BoolMatrices':
        """
        Intersection of two finite automaton in boolean decomposition
        :param other: Another finite automaton in boolean decomposition
        :return: result of intersection like bool matrix
        """
        intersect_labels = self.bool_matrcies.keys() & other.bool_matrcies.keys()
        result_bool_matrices = {label: sparse.kron(self.bool_matrcies[label], other.bool_matrcies[label])
                                for label in intersect_labels}

        result = BoolMatrices()
        result.bool_matrcies = result_bool_matrices

        for s1, s_ind1 in self.states_indices.items():
            for s2, s_ind2 in other.states_indices.items():
                state = s_ind1 * other.count_of_states + s_ind2
                result.states_indices[state] = state

                if s1 in self.start_states and s2 in other.start_states:
                    result.start_states.add(state)
                if s1 in self.final_states and s2 in other.final_states:
                    result.final_states.add(state)

        return result

    def to_nfa(self) -> NondeterministicFiniteAutomaton:
        """
        Convert bool decomposition to nfa
        :return: nondeterministic finite automaton
        """
        res_nfa = NondeterministicFiniteAutomaton()

        for label, mat in self.bool_matrcies.items():
            for from_v, to_v in zip(*mat.nonzero()):
                res_nfa.add_transition(from_v, label, to_v)

        for start_state in self.start_states:
            res_nfa.add_start_state(start_state)

        for final_state in self.final_states:
            res_nfa.add_final_state(final_state)

        return res_nfa

    def get_transitive_closure(self):
        """
        Create transitive closure
        :return: transitive closure
        """
        if len(self.bool_matrcies) == 0:
            return sparse.dok_matrix((0, 0), dtype=bool)

        transitive_closure = sum(self.bool_matrcies.values())
        prev, cur = 0, transitive_closure.nnz
        while prev != cur:
            transitive_closure += transitive_closure @ transitive_closure
            prev = cur
            cur = transitive_closure.nnz

        return transitive_closure
