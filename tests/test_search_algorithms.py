import itertools
import random

import pytest

import ids as ids_module
from node import Node
from bfs import bfs
from dfs import dfs
from ucs import ucs
from dls import dls
from ids import ids
from greedy_best_first_search import greedy_best_first_search
from a_star import a_star


ALGORITHMS = [
    ("BFS", bfs),
    ("DFS", dfs),
    ("UCS", ucs),
    ("DLS", lambda start, end: dls(start, end, l=10)),
    ("IDS", ids),
    ("Greedy", greedy_best_first_search),
    ("A*", a_star),
]

ALGORITHM_IDS = [name for name, _ in ALGORITHMS]


# Every simple path between start and end, used as an independent oracle
def all_simple_paths(start, end):
    paths = []

    def walk(cur_node, path, cost):
        if cur_node == end:
            paths.append((path, cost))
            return

        for neighbour, edge_cost in cur_node.neighbours:
            if neighbour.name not in path:
                walk(neighbour, path + [neighbour.name], cost + edge_cost)

    walk(start, [start.name], 0)

    return paths


# Sum of the edges of the path, failing if some edge does not exist
def path_cost(nodes, path):
    cost = 0

    for a, b in zip(path, path[1:]):
        edges = [edge_cost for neighbour, edge_cost in nodes[a].neighbours if neighbour.name == b]

        assert edges, f"edge {a} -> {b} does not exist"

        cost += min(edges)

    return cost


# Small random directed graphs where the cost of each edge is never lower
# than the euclidean distance, so the heuristic is admissible and consistent.
# Every ordered pair of nodes of each graph becomes a case
def random_graphs(count=200, seed=2026):
    rng = random.Random(seed)

    cases = []

    for _ in range(count):
        n = rng.randint(2, 8)

        nodes = {i: Node(i, x=rng.uniform(0, 10), y=rng.uniform(0, 10)) for i in range(n)}

        for i in range(n):
            for j in range(n):
                if i != j and rng.random() < 0.35:
                    euclid = nodes[i].distance_to(nodes[j])
                    nodes[i].add_neighbour(nodes[j], euclid * rng.uniform(1, 2) + rng.uniform(0, 1))

        for start, end in itertools.permutations(nodes.values(), 2):
            cases.append((nodes, start, end, all_simple_paths(start, end)))

    return cases


RANDOM_CASES = random_graphs()


@pytest.mark.parametrize("name, search", ALGORITHMS, ids=ALGORITHM_IDS)
def test_result_format_on_success(name, search, make_graph):
    g = make_graph([("A", "B", 2), ("B", "C", 3)])

    res = search(g["A"], g["C"])

    assert res["success"] is True
    assert res["path"] == ["A", "B", "C"]
    assert res["cost"] == 5
    assert isinstance(res["expanded_nodes"], int)
    assert res["expanded_nodes"] >= 0


@pytest.mark.parametrize("name, search", ALGORITHMS, ids=ALGORITHM_IDS)
def test_start_equals_end(name, search, make_graph):
    g = make_graph([("A", "B", 2)])

    res = search(g["A"], g["A"])

    assert res["success"] is True
    assert res["path"] == ["A"]
    assert res["cost"] == 0


@pytest.mark.parametrize("name, search", ALGORITHMS, ids=ALGORITHM_IDS)
def test_unreachable_goal(name, search, make_graph):
    g = make_graph([("A", "B", 1), ("B", "C", 1)])

    isolated = Node("Z", x=5, y=5)

    res = search(g["A"], isolated)

    assert res["success"] is False
    assert res["path"] is None
    assert res["cost"] == float("inf")


@pytest.mark.parametrize("name, search", ALGORITHMS, ids=ALGORITHM_IDS)
def test_goal_reachable_only_in_one_direction(name, search, make_graph):
    g = make_graph([("A", "B", 1), ("B", "C", 1)], directed=True)

    assert search(g["A"], g["C"])["success"] is True
    assert search(g["C"], g["A"])["success"] is False


@pytest.mark.parametrize("name, search", ALGORITHMS, ids=ALGORITHM_IDS)
def test_returned_path_is_valid_on_random_graphs(name, search):
    for nodes, start, end, paths in RANDOM_CASES:
        res = search(start, end)

        # Complete: finds a path whenever one exists
        assert res["success"] == bool(paths)

        if res["success"]:
            assert res["path"][0] == start.name
            assert res["path"][-1] == end.name
            assert res["cost"] == pytest.approx(path_cost(nodes, res["path"]))


@pytest.mark.parametrize("search", [bfs, ids], ids=["BFS", "IDS"])
def test_minimum_hops_on_random_graphs(search):
    for nodes, start, end, paths in RANDOM_CASES:
        if not paths:
            continue

        min_hops = min(len(path) - 1 for path, _ in paths)

        assert len(search(start, end)["path"]) - 1 == min_hops


@pytest.mark.parametrize("search", [ucs, a_star], ids=["UCS", "A*"])
def test_minimum_cost_on_random_graphs(search):
    for nodes, start, end, paths in RANDOM_CASES:
        if not paths:
            continue

        min_cost = min(cost for _, cost in paths)

        assert search(start, end)["cost"] == pytest.approx(min_cost)


def test_dls_succeeds_only_inside_the_limit():
    for nodes, start, end, paths in RANDOM_CASES:
        if not paths:
            continue

        min_hops = min(len(path) - 1 for path, _ in paths)

        for l in range(0, 7):
            res = dls(start, end, l=l)

            assert res["success"] == (min_hops <= l)

            if res["success"]:
                assert len(res["path"]) - 1 <= l


def test_dls_finds_path_first_reached_by_a_deeper_branch(make_graph):
    # S -> A -> C -> X is explored before S -> P -> X, so X is first reached
    # with depth 3. The path S -> P -> X -> Y -> G still fits in l = 4
    g = make_graph([
        ("S", "A", 1), ("S", "P", 1),
        ("A", "C", 1), ("C", "X", 1),
        ("P", "X", 1), ("X", "Y", 1), ("Y", "G", 1),
    ], directed=True)

    res = dls(g["S"], g["G"], l=4)

    assert res["success"] is True
    assert res["path"] == ["S", "P", "X", "Y", "G"]


def test_ids_returns_the_shallowest_path(make_graph):
    g = make_graph([
        ("S", "A", 1), ("S", "P", 1),
        ("A", "C", 1), ("C", "X", 1),
        ("P", "X", 1), ("X", "Y", 1), ("Y", "G", 1),
    ], directed=True)

    res = ids(g["S"], g["G"])

    assert res["path"] == bfs(g["S"], g["G"])["path"]


def test_dls_reports_cutoff(make_graph):
    g = make_graph([("S", "A", 1), ("A", "B", 1), ("B", "G", 1)])

    res = dls(g["S"], g["G"], l=2)

    assert res["success"] is False
    assert res["cutoff"] is True

    assert dls(g["S"], g["G"], l=3)["success"] is True


def test_dls_reports_failure_without_cutoff(make_graph):
    g = make_graph([("S", "A", 1)])

    # The whole graph fits in the limit, so the goal does not exist there
    res = dls(g["S"], Node("G"), l=5)

    assert res["success"] is False
    assert res["cutoff"] is False


def test_ids_stops_when_the_graph_is_exhausted(make_graph, monkeypatch):
    g = make_graph([("S", "A", 1)])

    limits = []

    def counting_dls(start, end, l=0):
        limits.append(l)
        return dls(start, end, l=l)

    monkeypatch.setattr(ids_module, "dls", counting_dls)

    res = ids_module.ids(g["S"], Node("G"), max_l=10)

    assert res["success"] is False

    # l = 2 already explores everything without cutoff
    assert limits == [0, 1, 2]


def test_ids_respects_the_max_limit(make_graph):
    g = make_graph([("S", "A", 1), ("A", "B", 1), ("B", "C", 1), ("C", "G", 1)])

    assert ids(g["S"], g["G"], max_l=3)["success"] is False
    assert ids(g["S"], g["G"], max_l=4)["success"] is True


def test_ids_counts_expanded_nodes_of_every_iteration(make_graph):
    g = make_graph([("S", "A", 1), ("A", "G", 1)])

    total = sum(dls(g["S"], g["G"], l=l)["expanded_nodes"] for l in range(0, 3))

    assert ids(g["S"], g["G"])["expanded_nodes"] == total


def test_dfs_does_not_overflow_on_long_chains(make_graph):
    # Deeper than the default recursion limit of Python
    edges = [(i, i + 1, 1) for i in range(3000)]

    g = make_graph(edges, directed=True)

    res = dfs(g[0], g[3000])

    assert res["success"] is True
    assert len(res["path"]) == 3001


def test_bfs_prefers_fewer_hops_over_lower_cost(make_graph):
    g = make_graph([("S", "G", 10), ("S", "A", 1), ("A", "G", 1)])

    assert bfs(g["S"], g["G"])["path"] == ["S", "G"]
    assert ucs(g["S"], g["G"])["path"] == ["S", "A", "G"]


def test_greedy_follows_the_heuristic_even_when_suboptimal(make_graph):
    coords = {"S": (0, 0), "A": (5, 0), "B": (0, 10), "G": (10, 0)}

    g = make_graph([("S", "A", 100), ("A", "G", 100), ("S", "B", 1), ("B", "G", 1)], coords)

    greedy = greedy_best_first_search(g["S"], g["G"])

    assert greedy["path"] == ["S", "A", "G"]
    assert greedy["cost"] == 200

    assert a_star(g["S"], g["G"])["cost"] == 2


def test_a_star_expands_fewer_nodes_than_ucs(make_graph):
    # Straight road to the goal and a dead end to the opposite side
    coords = {
        "S": (0, 0), "N1": (1, 0), "N2": (2, 0), "N3": (3, 0), "G": (4, 0),
        "D1": (-1, 0), "D2": (-2, 0), "D3": (-3, 0),
    }

    g = make_graph([
        ("S", "N1", 1), ("N1", "N2", 1), ("N2", "N3", 1), ("N3", "G", 1),
        ("S", "D1", 1), ("D1", "D2", 1), ("D2", "D3", 1),
    ], coords)

    res_a_star = a_star(g["S"], g["G"])
    res_ucs = ucs(g["S"], g["G"])

    assert res_a_star["cost"] == res_ucs["cost"] == 4
    assert res_a_star["expanded_nodes"] < res_ucs["expanded_nodes"]


@pytest.mark.parametrize("name, search", ALGORITHMS, ids=ALGORITHM_IDS)
def test_searches_do_not_share_state_between_calls(name, search, make_graph):
    g = make_graph([("A", "B", 1), ("B", "C", 1)])

    first = search(g["A"], g["C"])
    second = search(g["A"], g["C"])

    assert first == second
