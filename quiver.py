import pathlib
from matplotlib import pyplot as plt
import yaml
import networkx as nx
from typing import Any, Dict, List
from dataclasses import dataclass


import yaml
import networkx as nx
from typing import Any, Dict, List


def edgelist(node_from, node_to):
    if node_from is None or node_to is None:
        yield (node_from, "~")
    # a graph
    elif isinstance(node_from, list):
        current = node_to
        for neighbor_from in node_from:
            yield from edgelist(neighbor_from, current)
            current = neighbor_from
    elif isinstance(node_from, dict):
        yield
        # for neighbor_from, neighbor_to in node_to.items():

        # for neighbor_from, neighbor_to in node_from.items():
        #     yield from edgelist(neighbor_from, neighbor_to)
    # node_from is a scalar below
    else:
        if isinstance(node_to, list):
            neighbor_from = node_from
            for neighbor_to in node_to:
                yield from edgelist(neighbor_from, neighbor_to)
                neighbor_from = neighbor_to
            yield (neighbor_from, "~")
        elif isinstance(node_to, dict):
            for neighbor_from, neighbor_to in node_to.items():
                yield from edgelist(node_from, neighbor_from)
                yield from edgelist(neighbor_from, neighbor_to)
        # both are scalars
        else:
            yield (node_from, node_to)


def read_graph_from_yaml(filename: str) -> nx.DiGraph:
    path = pathlib.Path(filename)
    with path.open("r") as file:
        graph_data: Dict[str, Any] = yaml.safe_load(file)

    # graph = nx.DiGraph(graph_data)
    from_edgelist = edgelist(path.stem, graph_data)
    graph = nx.from_edgelist(from_edgelist, create_using=nx.DiGraph)
    return graph

@dataclass
class Free:
    graph: nx.DiGraph
 
    def paths_graph(self) -> nx.DiGraph:
        paths_graph = nx.DiGraph()

        for source in self.graph.nodes():
            for target in self.graph.nodes():
                if source != target:
                    if nx.has_path(self.graph, source, target):
                        paths_graph.add_edge(source, target)

        return paths_graph

@dataclass
class Cat:
    pass

@dataclass
class Fun:
    J: Cat
    C: Cat


# # Read lhs graph from YAML
# lhs_filename: str = "lhs_graph.yaml"
# lhs: nx.DiGraph = read_graph_from_yaml(lhs_filename)

# Read rhs graph from YAML
rhs_filename: str = "main.yaml"
rhs: nx.DiGraph = read_graph_from_yaml(rhs_filename)

# # https://ncatlab.org/nlab/show/free+diagram
# # C: Cat
# C = ""
# # I:Quiv
# I = lhs
# # Free:Quiv->Cat (path category)
# J = Free(I)
# # X:J->Cat es un free diagram en Cat
# # Limit ~
# # Colimit [] {}
# # Free(Diagram)
# X = Fun(J, C)

# Compose quiver with rhs graph
# res: nx.DiGraph = nx.compose(Free(rhs).paths_graph(), lhs)
res = rhs
# res = Free(rhs).paths_graph()

# Print the composed graph
nx.draw_networkx(res)

# nx.draw_networkx(paths_graph)
plt.show()
