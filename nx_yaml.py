import networkx as nx
from yaml.nodes import *
from categories import *


def to_digraph(node: Node) -> nx.DiGraph:
    match node:
        case ScalarNode(tag="tag:yaml.org,2002:null"):
            return nx.null_graph()
        case ScalarNode(value=scalar_from):
            return nx.DiGraph([(scalar_from, scalar_from)])
            # yield scalar_from, scalar_from
        case SequenceNode(value=node_path):
            return nx.compose_all(to_digraph(n) for n in node_path)
        case MappingNode(value=edges):
            return nx.compose_all(
                nx.compose(to_digraph(s), to_digraph(t))
                for (s, t) in edges)

# def to_ (SequenceNode(value=node_path_from), _):
#     current = node_to
#     for node in reversed(node_path_from):
#         yield from eval_to_digraphs(node, current)
#         current = node