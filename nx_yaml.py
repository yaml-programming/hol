import networkx as nx
import yaml
from yaml.nodes import *
from categories import *


def to_digraph(node: Node) -> nx.DiGraph:
    match node:
        case None | ScalarNode(tag="tag:yaml.org,2002:null"):
            return nx.null_graph()
        case ScalarNode(value=scalar):
            scalar_obj = yaml.safe_load(scalar)
            return nx.DiGraph([(scalar_obj, scalar_obj)])
        case SequenceNode(value=path):
            return nx.compose_all(to_digraph(n) for n in path)
        case MappingNode(value=edges):
            return nx.compose_all(
                nx.compose(to_digraph(s), to_digraph(t))
                for (s, t) in edges)

# def to_ (SequenceNode(value=node_path_from), _):
#     current = node_to
#     for node in reversed(node_path_from):
#         yield from eval_to_digraphs(node, current)
#         current = node