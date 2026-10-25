import os
import sys

import matplotlib

# Headless backend, so the dashboard can be tested without a window
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pytest

# The algorithms are plain modules in the repository root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from node import Node
from app import build_network


@pytest.fixture
def make_graph():
    # Builds a graph from (a, b, cost) edges and returns {name: Node}
    def _make_graph(edges, coords=None, directed=False):
        coords = coords if coords is not None else {}

        nodes = {}

        for a, b, _ in edges:
            for name in (a, b):
                if name not in nodes:
                    x, y = coords.get(name, (0, 0))
                    nodes[name] = Node(name, x=x, y=y)

        for a, b, cost in edges:
            nodes[a].add_neighbour(nodes[b], cost)

            if not directed:
                nodes[b].add_neighbour(nodes[a], cost)

        return nodes

    return _make_graph


@pytest.fixture
def unesp():
    return build_network()


@pytest.fixture(autouse=True)
def close_figures():
    yield

    # Avoid accumulating open figures between tests
    plt.close("all")
