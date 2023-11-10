import fileinput
import itertools
import pathlib
import sys

import yaml
from nx_yaml import NxSafeDumper, NxSafeLoader
import networkx as nx
import matplotlib.pyplot as plt
from discopy import braided, cat, monoidal, frobenius, symmetric
from discopy.frobenius import Spider, Swap

Id = frobenius.Id
Ty = frobenius.Ty
Box = frobenius.Box

def compose_graphs(graphs):
    diagram = Id()
    for G in graphs:
        i = Id().tensor(*(Spider(0, G.in_degree(n) or 1, Ty(n)) for n in sorted(G.nodes) if n != '' and G.out_degree(n) == 0))
        o = Id().tensor(*(Spider(G.out_degree(n) or 1, 0, Ty(n)) for n in sorted(G.nodes) if n != '' and G.in_degree(n) == 0))
        diagram >>= i
        diagram >>= cospan_hypergraph(G)
        diagram >>= o
    return diagram

def cospan_hypergraph(G):
    # importa el orden de cables no de cajas
    s = Id()
    for node in sorted(G.nodes):
        if node == '':
            continue

        n_legs_out = 0
        n_legs_in = 0
        # n_legs_out += G.out_degree(node) or 1
        # n_legs_in += G.in_degree(node) or 1
        if G.in_degree(node) == 0:
            n_legs_out += G.out_degree(node) or 1
        if G.out_degree(node) == 0:
            n_legs_in += G.in_degree(node) or 1
        # if G.has_edge(node, ''):
        #     n_legs_out -= 1
        # if G.has_edge('', node):
            # n_legs_out -= 1
            # n_legs_in += 1
        spider = Spider(n_legs_in, n_legs_out, Ty(node))
        s @= spider
    return s

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
        G = (#root,
            *yaml.compose_all(open(path), Loader=NxSafeLoader),
            )
    G = compose_graphs(G)
    # TODO temporary path
    G.to_gif(path=path.with_suffix(".gif"), loop=True, margins=(0.2, 0.05))
    return G

def compose_all_graphs():
    paths = iter(sys.argv[1:])
    for f in paths:
        compose_graph_file(pathlib.Path(f))

compose_all_graphs()
