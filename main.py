import pathlib
import sys
from matplotlib import pyplot as plt
import yaml
import networkx as nx
from typing import Any, Iterator, Self, Tuple
from yaml.nodes import *

from categories import *


def eval_to_edgelist(node_from: Node, node_to: Node) -> Iterator[Tuple[Any, Any]]:
    match (node_from, node_to):
        case ScalarNode(tag="tag:yaml.org,2002:null"), ScalarNode(value=scalar_to):
            yield from []
            # yield scalar_to, scalar_to
        case ScalarNode(value=scalar_from), ScalarNode(tag="tag:yaml.org,2002:null"):
            yield from []
            # yield scalar_from, scalar_from
        case (ScalarNode(value=scalar_from), ScalarNode(value=scalar_to)):
            yield scalar_from, scalar_to
        case (_, SequenceNode(value=node_path_to)):
            current = node_from
            for node in node_path_to:
                yield from eval_to_edgelist(node, current)
                current = node
        case (SequenceNode(value=node_path_from), _):
            current = node_to
            for node in reversed(node_path_from):
                yield from eval_to_edgelist(node, current)
                current = node
        case (_, MappingNode(value=edges_to)):
            for neighbor_from, neighbor_to in edges_to:
                yield from eval_to_edgelist(neighbor_from, node_from)
                yield from eval_to_edgelist(neighbor_to, neighbor_from)
        case (MappingNode(value=edges_from), _):
            for neighbor_from, neighbor_to in edges_from:
                yield from eval_to_edgelist(neighbor_to, neighbor_from)
                yield from eval_to_edgelist(node_to, neighbor_to)


class NxQuiver:
    """
    Quiver in C is a Functor Self->C.
    This implementation is based on the NetworkX library.

    Four basic graph properties facilitate reporting: G.nodes, G.edges, G.adj and G.degree
    """
    def __init__(self, digraph: nx.DiGraph):
        self.digraph = digraph

    def opposite(self) -> Self:
        return NxQuiver(self.digraph.reverse())

    def paths(self) -> Self:
        return NxQuiver(nx.transitive_closure(self.digraph, reflexive=True))
    
    def map(self, digraph: nx.DiGraph):
        """calling a quiver works as calling the underlying function"""
        return NxQuiver(nx.compose(self.digraph, digraph))

class FreeDiagram:
    """
    
    """
    def __init__(self, quiver: NxQuiver):
        self.quiver = quiver
        self.digraph = quiver.digraph

    def map(self, quiver: NxQuiver):
        return FreeDiagram(self.quiver.map(quiver.digraph))
    
    def flat_map(self, quiver: NxQuiver):
        digraph: nx.DiGraph = self.quiver.paths().digraph
        digraph.remove_edges_from(nx.selfloop_edges(digraph))
        quiver = NxQuiver(nx.transitive_reduction(digraph)).map(quiver.digraph)
        return FreeDiagram(quiver)


def print_digraph(digraph: nx.DiGraph):
    digraph.remove_edges_from(nx.selfloop_edges(digraph))
    digraph = nx.transitive_reduction(digraph)
    nx.draw_spring(digraph, with_labels=True)
    plt.show()


path = pathlib.Path(sys.argv[1]).with_suffix(".yaml")
with path.open("r") as file:
    yaml_representation_trees = yaml.compose_all(file)
    root = ScalarNode(tag="str", value=path.stem)
    document = SequenceNode(tag="seq", value=yaml_representation_trees)
    edgelist = eval_to_edgelist(root, document)
    digraph = nx.DiGraph(edgelist)
    print_digraph(digraph)
