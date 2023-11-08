import fileinput
import itertools
import pathlib
import sys

import yaml
from nx_yaml import NxSafeDumper, NxSafeLoader
import networkx as nx
import matplotlib.pyplot as plt
from discopy import braided, cat, monoidal, frobenius, symmetric

Id = frobenius.Id
Ty = frobenius.Ty
Box = frobenius.Box

def compose_graphs(graphs):
    graphs = iter(graphs)
    G = next(graphs)
    G_tensor = Id().tensor(*graph_signature_boxes(G))
    for H in graphs:
        H_tensor = Id().tensor(*graph_signature_boxes(H))
        G_tensor >>= H_tensor
        G = H
    return G_tensor.bubble()

def path_edges(path: pathlib.Path):
    for subpath in path.iterdir():
        if path.is_dir() and subpath.suffix == ".yaml":
            yield path.stem, subpath.stem


def compose_graph_file(path: pathlib.Path):
    if path.is_dir():
        G = [nx.DiGraph(path_edges(path))]
    else:
        G = yaml.compose_all(open(path), Loader=NxSafeLoader)
    G = compose_graphs(G)
    # TODO temporary path
    G.to_gif(path=path.with_suffix(".gif"))
    return G

def compose_all_graphs():
    paths = iter(sys.argv[1:])
    for f in paths:
        compose_graph_file(pathlib.Path(f))

def graph_signature_boxes(G):
    for node in sorted(G.nodes):
        if node:
            yield Box(
                node,
                Ty(*sorted(n if n else node for n in G.successors(node))),
                Ty(*sorted(n if n else node for n in G.predecessors(node))))
        else:
            yield Id()

# def compose_all_boxes():
#     for G, H in nx.utils.pairwise(compose_all_graphs()):
#         G_tensor = Id().tensor(*graph_signature_boxes(G))
#         H_tensor = Id().tensor(*graph_signature_boxes(H))
#         boundary_box_names = sorted(set(n for n in itertools.chain(G.nodes, H.nodes)))
#         boundary = Id().tensor(*(
#             Box(name,
#                 Ty(*sorted(H.successors(name))),
#                 Ty(*sorted(G.predecessors(name))))
#             for name in boundary_box_names
#             if name in G and name in H))
#         yield G_tensor
#         combined = boundary.bubble(dom=H_tensor.cod, cod=G_tensor.dom)
#         yield boundary


compose_all_graphs()
