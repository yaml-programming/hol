import pathlib
from matplotlib import pyplot as plt
import yaml
import networkx as nx
from typing import Any, Iterator, List, Self, Union

from categories import *

YamlNode = yaml.nodes.Node

def edgelist(node_from: YamlNode, node_to: YamlNode):
    if node_from is None or node_to is None:
        pass
    elif isinstance(node_from, yaml.nodes.SequenceNode):
        current = node_to
        for neighbor_from in node_from:
            yield from edgelist(neighbor_from, current)
            current = neighbor_from
    elif isinstance(node_from, yaml.nodes.MappingNode):
        for neighbor_from, neighbor_to in node_from.items():
            yamls = edgelist(node_to)
            for (neighbor_from, neighbor_to) in edgelist(yamls):
                yield from edgelist(neighbor_from, digraph)
    # node_from is a scalar below
    else:
        if isinstance(node_to, yaml.nodes.SequenceNode):
            neighbor_from = node_from
            for neighbor_to in node_to.value:
                yield from edgelist(neighbor_from, neighbor_to)
                neighbor_from = neighbor_to
        elif isinstance(node_to, yaml.nodes.MappingNode):
            for neighbor_from, neighbor_to in node_to.value:
                # primitive as in LISP
                if neighbor_to == "read":
                    for (neighbor_from, neighbor_to) in edgelist(neighbor_from):
                        yield from edgelist(neighbor_from, digraph)
                else:
                    yield from edgelist(node_from, neighbor_from)
                    yield from edgelist(neighbor_from, neighbor_to)
        # both are scalars
        else:
            yield (node_from.value, node_to.value)



def read_yamls(path_stem: str) -> List[Any]:
    path = pathlib.Path(path_stem).with_suffix(".yaml")
    with path.open("r") as file:
        return list(yaml.compose_all(file))

def read_digraphs(graphs_data: List[Any], root: nx.DiGraph) -> Iterator[nx.DiGraph]:
    for graph_data in graphs_data:
        from_edgelist = edgelist(root, graph_data)
        yield nx.from_edgelist(from_edgelist, create_using=nx.DiGraph)


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


def eval_digraphs(digraphs: Iterator[nx.DiGraph]) -> nx.DiGraph:
    """
    https://ncatlab.org/nlab/show/free+diagram
    quiero combinarlos de manera que se revele un DSL usable.
    por ejemplo si tengo un path parcial que es único
    quiero tener la info hacia ambos lados.
    """
    digraphs = iter(digraphs)
    head = NxQuiver(next(digraphs))
    tail = NxQuiver(nx.DiGraph())
    for digraph in digraphs:
        tail = tail.map(digraph)
    return FreeDiagram(tail).flat_map(head).digraph


def print_digraph(digraph: nx.DiGraph):
    nx.draw_spring(digraph, with_labels=True)
    plt.show()


def read_eval_print_loop(path_stem: str):
    yamls = read_yamls(path_stem)
    root = yaml.nodes.ScalarNode(tag='str', value=path_stem)
    digraphs = read_digraphs(yamls, root)
    print_digraph(eval_digraphs(digraphs))

read_eval_print_loop("actors")
