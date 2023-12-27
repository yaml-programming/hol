import fileinput
import functools
import itertools
import pathlib
import sys

import yaml
import matplotlib.pyplot as plt
from discopy import braided, cat, monoidal, frobenius, symmetric
from discopy.frobenius import Diagram, Hypergraph as H

from loader import HypergraphLoader, compose_entry

Id = frobenius.Id
Ty = frobenius.Ty
Box = frobenius.Box

def compose_graphs(graphs):
    graph = functools.reduce(
        compose_entry,
        graphs)
    return graph.to_diagram()

def compose_graph_file(path: pathlib.Path):
    if path.is_dir():
        # TODO
        G = compose_dir(path)
    else:
        G = (
            *yaml.compose_all(open(path), Loader=HypergraphLoader),
        )
    diagram = compose_graphs(G)
    # TODO temporary path
    Diagram.to_gif(diagram.simplify(), path=path.with_suffix(".gif"), loop=True, timestep=100)
    return diagram

def compose_all_graphs():
    paths = iter(sys.argv[1:])
    for f in paths:
        compose_graph_file(pathlib.Path(f))

def compose_dir(path):
    diagram = H.id()
    for subpath in path.iterdir():
        if subpath.suffix == ".yaml":
            diagram @= H.id(Ty(subpath.stem))
    yield diagram


compose_all_graphs()
