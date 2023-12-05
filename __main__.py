import fileinput
import functools
import itertools
import pathlib
import sys

import yaml
import networkx as nx
import matplotlib.pyplot as plt
from discopy import braided, cat, monoidal, frobenius, symmetric
from discopy.frobenius import Spider, Swap, Hypergraph as H

from loader import HypergraphLoader

Id = frobenius.Id
Ty = frobenius.Ty
Box = frobenius.Box

def compose_graphs(graphs):
    graph = functools.reduce(
        lambda g, h: g >> h,
        graphs)
    diagram = graph.to_diagram()
    # diagram.draw()
    return diagram.simplify()

def path_edges(path: pathlib.Path):
    for subpath in path.iterdir():
        if path.is_dir() and subpath.suffix == ".yaml":
            yield path.stem, subpath.stem


def compose_graph_file(path: pathlib.Path):
    if path.is_dir():
        G = [nx.DiGraph(path_edges(path))]
    else:
        root = nx.DiGraph()
        root.add_node(path.stem)
        G = (
            *yaml.compose_all(open(path), Loader=HypergraphLoader),
            )
    G = compose_graphs(G)
    # TODO temporary path
    G.to_gif(path=path.with_suffix(".gif"), loop=True, margins=(0.5, 0.05))
    return G

def compose_all_graphs():
    paths = iter(sys.argv[1:])
    for f in paths:
        compose_graph_file(pathlib.Path(f))

compose_all_graphs()
