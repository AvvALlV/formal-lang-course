from project.interpreter.Types import *
from project.interpreter.Exceptions import *
from project.interpreter.Set import Set
from networkx import MultiDiGraph
from project.finite_automaton import *
from project.bool_matrices import *


class FiniteAutomaton(Type):
    def __init__(self, nfa: NondeterministicFiniteAutomaton):
        self.nfa = nfa

    def __str__(self):
        return str(self.nfa.minimize().to_regex())

    def __eq__(self, other: "FiniteAutomaton") -> bool:
        return self.nfa.is_equivalent_to(other.nfa)

    @classmethod
    def from_graph(cls, graph: MultiDiGraph):
        return cls(graph_to_nfa(graph))

    @classmethod
    def from_string(cls, regex_str):
        try:
            return cls(regex_to_dfa(regex_str))
        except Exception as e:
            raise RuntimeException(str(e))

    @property
    def start(self):
        return Set(self.nfa.start_states)

    @property
    def finals(self):
        return Set(self.nfa.final_states)

    @property
    def edges(self):
        edges_set = set()

        edges_dict = self.nfa.to_dict()
        for u in edges_dict.keys():
            for label, v_set in edges_dict.get(u).items():
                for v in v_set:
                    edges_set.add((u, label, v))

        return Set(edges_set)

    @property
    def labels(self):
        return Set(self.nfa.symbols)

    @property
    def vertices(self):
        return Set(self.nfa.states)

    def setStart(self, start_states: Set) -> "FiniteAutomaton":
        return FiniteAutomaton(set_states(self.nfa, start_states=start_states.set))

    def setFinal(self, final_states: Set):
        return FiniteAutomaton(set_states(self.nfa, final_states=final_states.set))

    def addStart(self, start_states: Set) -> "FiniteAutomaton":
        return FiniteAutomaton(add_states(self.nfa, start_states=start_states.set))

    def addFinal(self, final_states: Set) -> "FiniteAutomaton":
        return FiniteAutomaton(add_states(self.nfa, final_states=final_states))

    def intersect(self, other: "FiniteAutomaton") -> "FiniteAutomaton":
        bm_nfa = BoolMatrices(self.nfa)
        bm_other_nfa = BoolMatrices(other.nfa)
        return FiniteAutomaton(bm_nfa.intersect(bm_other_nfa).to_nfa())

    def union(self, other: "FiniteAutomaton") -> "FiniteAutomaton":
        return FiniteAutomaton(self.nfa.union(other.nfa).to_deterministic())

    def concatenate(self, other):
        regex = self.nfa.to_regex()
        other_regex = self.nfa.to_regex()
        return FiniteAutomaton(
            regex.concatenate(other_regex).to_epsilon_nfa().to_deterministic()
        )

    def inverse(self) -> "FiniteAutomaton":
        return FiniteAutomaton(self.nfa.get_complement().to_deterministic())

    def kleene(self) -> "FiniteAutomaton":
        return FiniteAutomaton(self.nfa.kleene_star().to_deterministic())

    def getReachable(self):
        bm_nfa = BoolMatrices(self.nfa)
        transitive_closure = bm_nfa.get_transitive_closure()
        reachable_state_nums = set()

        for state_from_num, state_to_num in zip(*transitive_closure.nonzero()):
            state_from = bm_nfa.states_indices[state_from_num]
            state_to = bm_nfa.states_indices[state_to_num]

            if state_from in bm_nfa.start_states and state_to in bm_nfa.final_states:
                reachable_state_from_num = bm_nfa.states_indices
                reachable_state_to_num = bm_nfa.states_indices

                reachable_state_nums.add(
                    (reachable_state_from_num, reachable_state_to_num)
                )

        return reachable_state_nums
