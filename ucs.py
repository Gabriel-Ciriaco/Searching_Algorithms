import heapq

from node import Node

def ucs(start: Node, end: Node) -> dict:

    pq = [(0, start, [start.name])]
    
    visited = {}

    while pq:
        cur_cost, cur_node, path = heapq.heappop(pq)

        # We already have a lower cost path
        if cur_node in visited and visited[cur_node] <= cur_cost:
            continue

        visited[cur_node] = cur_cost

        # Goal reached, then pop the node with the lowest cost
        if cur_node == end:
            return {
                "success": True,
                "path": path,
                "cost": cur_cost,
                "expanded_nodes": len(visited)
            }

        for neighbour, edge_cost in cur_node.neighbours:
            total_cost = cur_cost + edge_cost

            if neighbour not in visited or \
                total_cost < visited[neighbour]:

                heapq.heappush(pq, (
                    total_cost,
                    neighbour,
                    path + [neighbour.name]
                ))
            
    return {
        "success": False,
        "path": None,
        "cost": float("inf"),
        "expanded_nodes": len(visited)
    }
