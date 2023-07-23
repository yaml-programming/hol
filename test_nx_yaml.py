import networkx as nx
import yaml

from nx_yaml import to_digraph


def test_null():
    document = ""
    digraph = doc_digraph(document)
    assert nx.utils.graphs_equal(digraph, nx.null_graph())


def test_singleton():
    document = "false"
    digraph = doc_digraph(document)
    assert list(digraph.nodes) == [False]
    assert list(digraph.edges) == [(False, False)]


def doc_digraph(document: str):
    node = yaml.compose(document)
    return to_digraph(node)
