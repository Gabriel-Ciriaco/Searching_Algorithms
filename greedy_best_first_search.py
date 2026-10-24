import heapq
from node import Node

def greedy_best_first_search(start: Node, end: Node) -> dict:
    visited = set()

    # Priority queue with (distance_to_end, cur_node, path, accumulated_cost)
    pq = [(start.distance_to(end), start, [start.name], 0)]

    while pq:
        h_cost, cur_node, path, cur_cost = heapq.heappop(pq)

        if cur_node in visited:
            continue
        
        visited.add(cur_node)

        if cur_node == end:
            return {
                "success": True,
                "path": path,
                "cost": cur_cost,
                "expanded_nodes": len(visited)
            }

        for neighbour, edge in cur_node.neighbours:
            if neighbour not in visited:
                heur_neighbour = neighbour.distance_to(end)

                heapq.heappush(pq, (
                    heur_neighbour,
                    neighbour,
                    path + [neighbour.name],
                    cur_cost + edge
                ))
    
    return {
        "success": False,
        "path": None,
        "cost": float("inf"),
        "expanded_nodes": len(visited)
    }
