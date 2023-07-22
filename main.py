import pathlib
import sys
from matplotlib import pyplot as plt
import yaml
import networkx as nx
from typing import Any, Iterator, Self, Tuple
from yaml.nodes import *

from categories import *


def edgelist(node_from: Node, node_to: Node) -> Iterator[Tuple[Any, Any]]:
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
                yield from edgelist(current, node)
                current = node
        case (SequenceNode(value=node_path_from), _):
            current = node_to
            for node in reversed(node_path_from):
                yield from edgelist(node, current)
                current = node
        case (_, MappingNode(value=edges_to)):
            for neighbor_from, neighbor_to in edges_to:
                yield from edgelist(node_from, neighbor_from)
                yield from edgelist(neighbor_from, neighbor_to)
        case (MappingNode(value=edges_from), _):
            for neighbor_from, neighbor_to in edges_from:
                yield from edgelist(neighbor_from, neighbor_to)
                yield from edgelist(neighbor_to, node_to)
        # case (MappingNode(value=edges_from), _):
        #     for neighbor_from, neighbor_to in edges_from:
        #         yield from edgelist(neighbor_from, neighbor_to)
        #         yield from edgelist(neighbor_to, node_to)

        # case (ScalarNode(value=scalar_from), ScalarNode(value=scalar_to)):
        #     yield (scalar_from, scalar_to)
        #     current = node_to
        #     for neighbor_from in node_list_from:
        #         yield from edgelist(neighbor_from, current)
        #         current = neighbor_from
        #         # yamls = edgelist(node_to)
        #         # for (neighbor_from, neighbor_to) in edgelist(yamls):
        # # node_from is a scalar below
        # case (_, MappingNode(value=node_to)):
        #     for neighbor_from, neighbor_to in node_to:
        #         yield from edgelist(node_from, neighbor_from)
        #         yield from edgelist(neighbor_from, neighbor_to)
        #         # # primitive as in LISP
        #         # if neighbor_to == "read":
        #         #     for (neighbor_from, neighbor_to) in edgelist(neighbor_from):
        #         #         yield from edgelist(neighbor_from, digraph)
        # case (_, SequenceNode(value=node_to)):
        #     neighbor_from = node_from
        #     for neighbor_to in node_to:
        #         yield from edgelist(neighbor_from, neighbor_to)
        #         neighbor_from = neighbor_to
        #     yield (node_from.value, node_to)


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


def eval_node(node: Node) -> nx.DiGraph:
    """
    https://ncatlab.org/nlab/show/free+diagram
    quiero combinarlos de manera que se revele un DSL usable.
    por ejemplo si tengo un path parcial que es único
    quiero tener la info hacia ambos lados.
    """
    return nx.DiGraph(edgelist(ScalarNode(tag="tag:yaml.org,2002:null", value="~"), node))


def print_digraph(digraph: nx.DiGraph):
    nx.draw_spring(digraph, with_labels=True)
    plt.show()


def read_eval_print_loop(root: Node):
    print_digraph(eval_node(root))


path = pathlib.Path(sys.argv[1]).with_suffix(".yaml")
with path.open("r") as file:
    yamls = yaml.compose_all(file)
    root = SequenceNode(tag="seq", value=yamls)
    read_eval_print_loop(root)
