import heapq
from node import Node

def a_star(start: Node, end: Node) -> dict:

    # Priority queue with (f(n), g(n), node, path)
    pq = [(start.distance_to(end), 0, start, [start.name])]

    visited = {}

    while pq:
        f_cost, g_cost, cur_node, path = heapq.heappop(pq)

        if cur_node in visited and \
            visited[cur_node] <= g_cost:
            continue
        
        visited[cur_node] = g_cost

        if cur_node == end:
            return {
                "success": True,
                "path": path,
                "cost": g_cost,
                "expanded_nodes": len(visited)
            }
        
        for neighbour, edge_cost in cur_node.neighbours:
            total_g_cost = g_cost + edge_cost

            if neighbour not in visited or \
                total_g_cost < visited[neighbour]:

                total_h = neighbour.distance_to(end)
                total_f = total_g_cost + total_h

                heapq.heappush(pq, (
                    total_f,
                    total_g_cost,
                    neighbour,
                    path + [neighbour.name]
                ))
    
    return {
        "success": False,
        "path": None,
        "cost": float("inf"),
        "expanded_nodes": len(visited)
    }
