import networkx as nx
from yaml import ScalarNode

from nx_yaml import to_digraph


def test_null_node():
    null_node = ScalarNode(tag="tag:yaml.org,2002:null", value=None)
    digraph = to_digraph(null_node)
    assert nx.utils.graphs_equal(digraph, nx.null_graph())
