import pathlib
from matplotlib import pyplot as plt
import yaml
import networkx as nx
from typing import Any, Iterator, List, Self, Union

from categories import *

YamlNode = Union[List, dict, str, nx.DiGraph]

def edgelist(node_from: YamlNode, node_to: YamlNode):
    if node_from is None or node_to is None:
        pass
    elif isinstance(node_from, list):
        current = node_to
        for neighbor_from in node_from:
            yield from edgelist(neighbor_from, current)
            current = neighbor_from
    elif isinstance(node_from, dict):
        for neighbor_from, neighbor_to in node_from.items():
            yamls = read_yamls(node_to)
            for digraph in read_digraphs(yamls):
                yield from edgelist(neighbor_from, digraph)
    # node_from is a scalar below
    else:
        if isinstance(node_to, list):
            neighbor_from = node_from
            for neighbor_to in node_to:
                yield from edgelist(neighbor_from, neighbor_to)
                neighbor_from = neighbor_to
        elif isinstance(node_to, dict):
            for neighbor_from, neighbor_to in node_to.items():
                # primitive as in LISP
                if neighbor_to == "read":
                    for digraph in read_digraphs(neighbor_from):
                        yield from edgelist(neighbor_from, digraph)
                else:
                    yield from edgelist(node_from, neighbor_from)
                    yield from edgelist(neighbor_from, neighbor_to)
        # both are scalars
        else:
            yield (node_from, node_to)



def read_yamls(path_stem: str) -> List[Any]:
    path = pathlib.Path(path_stem).with_suffix(".yaml")
    with path.open("r") as file:
        return list(yaml.safe_load_all(file))

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
    
    def __call__(self, obj):
        """calling a quiver works as calling the underlying function"""
        digraph = self.digraph.edge_subgraph(self.digraph.edges(obj))
        return NxQuiver(digraph)

class FreeDiagram:
    """
    
    """
    def __init__(self, quiver: NxQuiver):
        self.quiver = quiver

    def map(self, quiver: NxQuiver):
        # a functor of the form X:Free(I)->C
        return self.quiver(quiver)
    
    @property
    def digraph(self) -> nx.DiGraph:
        return self.digraph.digraph


def eval_digraphs(digraphs: Iterator[nx.DiGraph]) -> nx.DiGraph:
    """
    https://ncatlab.org/nlab/show/free+diagram
    quiero combinarlos de manera que se revele un DSL usable.
    por ejemplo si tengo un path parcial que es único
    quiero tener la info hacia ambos lados.
    """
    digraphs = iter(digraphs)
    diagram = FreeDiagram(NxQuiver(next(digraphs)))
    for digraph in digraphs:
        diagram = diagram.map(digraph)
        # a directed graph I
        # current_digraph = nx.transitive_closure(current_digraph, reflexive=True)
        # print_digraph(current_digraph)
        # current_digraph = current_digraph.subgraph(digraph, )
        # a functor of the form X:Free(I)->C
        # digraph = nx.transitive_reduction(digraph)
        # current_digraph = nx.transi(current_digraph, digraph)
        # print_digraph(digraph)
        # print_digraph(current_digraph)
    return diagram.digraph


def print_digraph(digraph: nx.DiGraph):
    # digraph = nx.single_source_shortest_path(digraph, "actors")
    # digraph = nx.DiGraph(digraph)
    # digraph = nx.transitive_reduction(digraph)
    nx.draw_spring(digraph, with_labels=True)
    plt.show()


def read_eval_print_loop(path_stem: str):
    yamls = read_yamls(path_stem)
    root = nx.DiGraph()
    root.add_node(path_stem)
    digraphs = read_digraphs(yamls, root)
    # digraphs = list(digraphs)
    # for digraph in digraphs:
    #     print_digraph(digraph)
    print_digraph(eval_digraphs(digraphs))

    # res_head = NxQuiver(d_head)
    # res_tail = NxQuiver(d_tail)
    # TailCat = Free(res_tail)
    # diag = FreeDiag(TailCat, res_head)
    # keseyo = res_head.paths.digraph
    # nx.draw_networkx(keseyo, pos=nx.shell_layout(keseyo))
    # res_mid = Free(NxQuiver(d_mid))

    # cat = SIndCat(res_head)
    # SIndFun
    # res = res_head.digraph.subgraph(nx.transitive_closure_dag(res_tail.digraph.adj)) #.edge_subgraph([("apellido", "fede")])
    # desc = nx.descendants(res_head.digraph, res_tail.digraph.adj)
    # asc = res_head.digraph.subgraph(res_tail.digraph.adj)
    # res = res_head.digraph.subgraph([desc, asc]) #.edge_subgraph([("apellido", "fede")])

read_eval_print_loop("actors")
