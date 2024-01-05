import yaml
from discopy.frobenius import Box, Ty, Spider, Diagram

from loader import HypergraphLoader

def test_monoid():
    d = (
            Spider(0, 1, Ty("0")) @ Box("μ", Ty("μ"), Ty("μ")) >> \
            Box("0", Ty("0"), Ty("0")) @ Spider(1, 0, Ty("μ"))
        ) @ \
        (
            Spider(0, 1, Ty("2")) @ Box("η", Ty("η"), Ty("η")) >> \
            Box("2", Ty("2"), Ty("2")) @ Spider(1, 0, Ty("η"))
        )
    t = yaml.compose(open("src/yaml/monoid.yaml"), Loader=HypergraphLoader)
    with Diagram.hypergraph_equality:
        assert t.to_diagram() == d
