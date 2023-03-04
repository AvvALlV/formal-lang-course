import cfpq_data
from collections import namedtuple
import networkx as nx

GraphInfo = namedtuple("GraphInfo", ["number_of_vertices", "number_of_edges", "labels"])


def get_graph_by_name(name: str) -> nx.MultiDiGraph:
    graph_path = cfpq_data.download(name)
    graph = cfpq_data.graph_from_csv(graph_path)

    return graph


def get_graph_info_by_name(name: str) -> GraphInfo:
    graph = get_graph_by_name(name)
    return GraphInfo(
        graph.number_of_nodes(), graph.number_of_edges(), graph.edges(data=True)
    )


def create_labeled_two_cycles_graph(n: int, m: int, labels=("a", "b")):
    return cfpq_data.labeled_two_cycles_graph(n=n, m=m, labels=labels)


def save_labeled_two_cycles_graph(path: str, n: int, m: int, labels=("a", "b")):
    graph = create_labeled_two_cycles_graph(n, m, labels)
    pydot_graph = nx.nx_pydot.to_pydot(graph)
    pydot_graph.write(path=path)
