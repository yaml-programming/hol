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
    G = nx.DiGraph()
    boundary = Id()
    for H in graphs:
        boundary >>= Id().tensor(*graph_spider_boundary(G, H))
        G = H
    return boundary or Id()

def graph_spider_boundary(G, H):
    # importa el orden de cables no de cajas
    for node in sorted(set(H.nodes).union(G.nodes)):
        n_legs_in = 0
        n_legs_out = 0
        if not node:
            continue
        if node in G and node in H:
            G_in = G.in_degree(node)
            G_out = G.out_degree(node)
            H_in = H.in_degree(node)
            H_out = H.out_degree(node)
            n_legs_in += G_in + H_in
            n_legs_out += G_out + H_out
        elif node in G:
            G_out = G.out_degree(node)
            n_legs_in += G_out
            if G_out == 0:
                n_legs_in += 1
        elif node in H:
            H_in = H.in_degree(node)
            n_legs_out += H_in
            if H_in == 0:
                n_legs_out += 1

        spider = Spider(n_legs_in, n_legs_out, Ty(node))
        yield spider

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
        G = itertools.chain(
            [root],
            yaml.compose_all(open(path), Loader=NxSafeLoader))
    G = compose_graphs(G)
    # TODO temporary path
    G.to_gif(path=path.with_suffix(".gif"), loop=True)
    return G

def compose_all_graphs():
    paths = iter(sys.argv[1:])
    for f in paths:
        compose_graph_file(pathlib.Path(f))

compose_all_graphs()
