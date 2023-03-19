from scipy import sparse
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State


class BoolMatrices:
    """
    Сlass implements boolean decomposition
    """

    def __init__(self, nfa: NondeterministicFiniteAutomaton = None):
        if nfa is None:
            self.states, self.start_states, self.final_states, self.states_indices = (
                set(),
                set(),
                set(),
                dict(),
            )
            self.bool_matrices, self.count_of_states = dict(), 0
        else:
            self.states, self.start_states, self.final_states = (
                nfa.states,
                nfa.start_states,
                nfa.final_states,
            )
            self.states_indices = {
                state: index for index, state in enumerate(nfa.states)
            }

            self.count_of_states = len(self.states)
            self.bool_matrices = dict()
            for from_v, label, to_v in nfa:
                label_matrix = self.bool_matrices.setdefault(
                    label,
                    sparse.dok_matrix(
                        (self.count_of_states, self.count_of_states), dtype=bool
                    ),
                )
                label_matrix[
                    self.states_indices[from_v], self.states_indices[to_v]
                ] = True

    def intersect(self, other: "BoolMatrices") -> "BoolMatrices":
        """
        Intersection of two finite automaton in boolean decomposition
        :param other: Another finite automaton in boolean decomposition
        :return: result of intersection like bool matrix
        """
        intersect_labels = self.bool_matrices.keys() & other.bool_matrices.keys()
        result_bool_matrices = {
            label: sparse.kron(self.bool_matrices[label], other.bool_matrices[label])
            for label in intersect_labels
        }

        result = BoolMatrices()
        result.bool_matrices = result_bool_matrices

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

        for label, mat in self.bool_matrices.items():
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
        if len(self.bool_matrices) == 0:
            return sparse.dok_matrix((0, 0), dtype=bool)

        transitive_closure = sum(self.bool_matrices.values())
        prev, cur = 0, transitive_closure.nnz
        while prev != cur:
            transitive_closure += transitive_closure @ transitive_closure
            prev = cur
            cur = transitive_closure.nnz

        return transitive_closure

    def bfs_based_rpq(self, other: "BoolMatrices", separate: bool = False):
        direct_sum = other._direct_sum(self)
        n, k = self.count_of_states, other.count_of_states

        start_states_indices = [
            index
            for index, state in enumerate(self.states)
            if state in self.start_states
        ]
        final_states_indices = [
            index
            for index, state in enumerate(self.states)
            if state in self.final_states
        ]
        other_final_states_indices = [
            index
            for index, state in enumerate(other.states)
            if state in other.final_states
        ]

        if not separate:
            front = self._make_front(other)
        else:
            front = self._make_separated_front(other)

        visited = sparse.csr_matrix(front.shape)

        while True:
            prev_visited = visited.copy()
            for matrix in direct_sum.bool_matrices.values():
                if front is not None:
                    front2 = front @ matrix
                else:
                    front2 = visited @ matrix

                visited += self._transform_rows(front2, other)

            front = None

            if visited.nnz == prev_visited.nnz:
                break

        result = set()
        for i, j in zip(*visited.nonzero()):
            if (
                j >= k
                and i % k in other_final_states_indices
                and j - k in final_states_indices
            ):
                if not separate:
                    result.add(j - k)
                else:
                    result.add((start_states_indices[i // n], j - k))

        return result

    def _direct_sum(self, other: "BoolMatrices"):
        result = BoolMatrices()
        symbols = self.bool_matrices.keys() & other.bool_matrices.keys()

        for symbol in symbols:
            result.bool_matrices[symbol] = sparse.bmat(
                [
                    [self.bool_matrices[symbol], None],
                    [None, other.bool_matrices[symbol]],
                ]
            )

        start_states = {
            State(state.value + self.count_of_states) for state in other.start_states
        }
        final_states = {
            State(state.value + self.count_of_states) for state in other.final_states
        }

        for first_index in self.states_indices.values():
            for second_index in other.states_indices.values():
                state = first_index * other.count_of_states + second_index
                result.states_indices[state] = state

        if not isinstance(self.start_states, set):
            self.start_states = set()
        result.states = self.states | set(
            (State(state.value + self.count_of_states) for state in other.states)
        )
        result.num_of_states = self.count_of_states + other.count_of_states
        result.start_states = self.start_states | start_states
        result.final_states = self.final_states | final_states

        result.bool_matrices = result.bool_matrices

        return result

    def _make_front(self, other: "BoolMatrices"):
        n, k = self.count_of_states, other.count_of_states
        front = sparse.lil_matrix((k, n + k))

        right_part = sparse.lil_array(
            [[state in self.start_states for state in self.states]]
        )

        for index in other.states_indices.values():
            front[index, index] = True
            front[index, k:] = right_part

        return front.tocsr()

    def _make_separated_front(self, other: "BoolMatrices"):
        start_indices = {
            index
            for index, state in enumerate(self.states)
            if state in self.start_states
        }
        fronts = [self._make_front(other) for _ in start_indices]

        if len(fronts) > 0:
            return sparse.csr_matrix(sparse.vstack(fronts))
        else:
            return sparse.csr_matrix(
                (other.count_of_states, other.count_of_states + self.count_of_states)
            )

    def _transform_rows(self, part: sparse.csr_matrix, other: "BoolMatrices"):
        transformed_part = sparse.lil_array(part.shape)

        for i, j in zip(*part.nonzero()):
            if j < other.count_of_states:
                non_zero_right = part.getrow(i).tolil()[[0], other.count_of_states :]

                if non_zero_right.nnz > 0:
                    shift_row = i // other.count_of_states * other.count_of_states
                    transformed_part[shift_row + j, j] = 1
                    transformed_part[
                        [shift_row + j], other.count_of_states :
                    ] += non_zero_right

        return transformed_part.tocsr()
