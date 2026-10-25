import heapq

from node import Node


def test_nodes_with_same_name_are_equal():
    a = Node("Bauru")
    b = Node("Bauru")

    assert a == b
    assert hash(a) == hash(b)

    # Works as key of sets and dicts
    assert len({a, b}) == 1


def test_node_is_not_equal_to_other_types():
    assert Node("Bauru") != "Bauru"
    assert Node("Bauru") != None


def test_add_neighbour_stores_cost():
    a = Node("A")
    b = Node("B")

    a.add_neighbour(b)
    a.add_neighbour(b, cost=7)

    assert a.neighbours == [(b, 1.0), (b, 7)]

    # The edge is directed, the other node is not changed
    assert b.neighbours == []


def test_neighbours_are_not_shared_between_nodes():
    a = Node("A")
    b = Node("B")

    a.add_neighbour(Node("C"))

    assert b.neighbours == []


def test_distance_to_is_euclidean():
    a = Node("A", x=0, y=0)
    b = Node("B", x=3, y=4)

    assert a.distance_to(b) == 5
    assert b.distance_to(a) == 5
    assert a.distance_to(a) == 0


def test_lt_allows_ties_in_heapq():
    # Same priority forces the heap to compare the nodes
    pq = []

    heapq.heappush(pq, (1, Node("B")))
    heapq.heappush(pq, (1, Node("A")))

    assert heapq.heappop(pq)[1].name == "A"
