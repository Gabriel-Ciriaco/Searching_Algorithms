import itertools

import pytest

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

# Benchmark table of the README (Presidente Prudente -> Bauru)
README_BENCHMARK = [
    ("BFS", bfs, 330, 6, ["Presidente Prudente", "Assis", "Bauru"]),
    ("DFS", dfs, 328, 4, ["Presidente Prudente", "Assis", "Ourinhos", "Bauru"]),
    ("UCS", ucs, 283, 5, ["Presidente Prudente", "Marília", "Bauru"]),
    ("DLS (L=2)", lambda start, end: dls(start, end, l=2), 330, 2, ["Presidente Prudente", "Assis", "Bauru"]),
    ("IDS", ids, 330, 3, ["Presidente Prudente", "Assis", "Bauru"]),
    ("Greedy", greedy_best_first_search, 283, 3, ["Presidente Prudente", "Marília", "Bauru"]),
    ("A*", a_star, 283, 4, ["Presidente Prudente", "Marília", "Bauru"]),
]


def city_pairs(unesp):
    return list(itertools.permutations(unesp.keys(), 2))


def test_network_has_the_ten_campus_cities(unesp):
    assert len(unesp) == 10

    for name, node in unesp.items():
        assert node.name == name


def test_roads_are_bidirectional_with_same_cost(unesp):
    for city in unesp.values():
        for neighbour, cost in city.neighbours:
            assert cost > 0
            assert (city, cost) in neighbour.neighbours


def test_heuristic_is_consistent_for_every_goal(unesp):
    # h(n) <= c(n, n') + h(n') for every road and every possible destination
    for goal in unesp.values():
        for city in unesp.values():
            for neighbour, cost in city.neighbours:
                assert city.distance_to(goal) <= cost + neighbour.distance_to(goal)


def test_heuristic_is_admissible_for_every_pair(unesp):
    for a, b in city_pairs(unesp):
        res = ucs(unesp[a], unesp[b])

        if res["success"]:
            assert unesp[a].distance_to(unesp[b]) <= res["cost"]


@pytest.mark.parametrize("name, search", ALGORITHMS, ids=[name for name, _ in ALGORITHMS])
def test_ilha_solteira_is_unreachable(name, search, unesp):
    res = search(unesp["Presidente Prudente"], unesp["Ilha Solteira"])

    assert res["success"] is False
    assert res["path"] is None
    assert res["cost"] == float("inf")


def test_a_star_matches_ucs_on_every_pair(unesp):
    for a, b in city_pairs(unesp):
        res_a_star = a_star(unesp[a], unesp[b])
        res_ucs = ucs(unesp[a], unesp[b])

        assert res_a_star["success"] == res_ucs["success"]
        assert res_a_star["cost"] == res_ucs["cost"]


def test_a_star_never_expands_more_than_ucs(unesp):
    for a, b in city_pairs(unesp):
        assert a_star(unesp[a], unesp[b])["expanded_nodes"] <= ucs(unesp[a], unesp[b])["expanded_nodes"]


def test_ids_matches_bfs_hops_on_every_pair(unesp):
    for a, b in city_pairs(unesp):
        res_bfs = bfs(unesp[a], unesp[b])
        res_ids = ids(unesp[a], unesp[b])

        assert res_ids["success"] == res_bfs["success"]

        if res_bfs["success"]:
            assert len(res_ids["path"]) == len(res_bfs["path"])


def test_dls_succeeds_from_the_bfs_hop_count(unesp):
    for a, b in city_pairs(unesp):
        res_bfs = bfs(unesp[a], unesp[b])

        if not res_bfs["success"]:
            continue

        hops = len(res_bfs["path"]) - 1

        assert dls(unesp[a], unesp[b], l=hops - 1)["success"] is False
        assert dls(unesp[a], unesp[b], l=hops)["success"] is True


@pytest.mark.parametrize(
    "name, search, cost, expanded_nodes, path",
    README_BENCHMARK,
    ids=[row[0] for row in README_BENCHMARK]
)
def test_readme_benchmark(name, search, cost, expanded_nodes, path, unesp):
    res = search(unesp["Presidente Prudente"], unesp["Bauru"])

    assert res["success"] is True
    assert res["cost"] == cost
    assert res["expanded_nodes"] == expanded_nodes
    assert res["path"] == path


def test_readme_python_example():
    prudente = Node("Presidente Prudente", x=0, y=50)
    marilia = Node("Marília", x=160, y=90)
    bauru = Node("Bauru", x=265, y=70)

    prudente.add_neighbour(marilia, cost=178)
    marilia.add_neighbour(bauru, cost=105)

    assert a_star(prudente, bauru) == {
        "success": True,
        "path": ["Presidente Prudente", "Marília", "Bauru"],
        "cost": 283,
        "expanded_nodes": 3
    }
