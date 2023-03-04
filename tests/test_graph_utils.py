import pytest
import project.graph_utils as graphU
from tempfile import NamedTemporaryFile


def test_get_graph_info():
    graphSkos = graphU.get_graph_info_by_name("skos")
    assert graphSkos.number_of_vertices == 144
    assert graphSkos.number_of_edges == 252

    graphBzip = graphU.get_graph_info_by_name("bzip")
    assert graphBzip.number_of_vertices == 632
    assert graphBzip.number_of_edges == 556


def test_save_labeled_two_cycles_graph():
    path_to_graph = ""
    with NamedTemporaryFile(delete=False) as f:
        path_to_graph = f.name

    graphU.save_labeled_two_cycles_graph(path_to_graph, 2, 2)
    with open(path_to_graph) as f:
        output = "".join(f.readlines())
        excepted = """digraph  {
1;
2;
0;
3;
4;
1 -> 2  [key=0, label=a];
2 -> 0  [key=0, label=a];
0 -> 1  [key=0, label=a];
0 -> 3  [key=0, label=b];
3 -> 4  [key=0, label=b];
4 -> 0  [key=0, label=b];
}\n"""

        assert output == excepted
