from collections import deque
from node import Node


def bfs(start: Node, end: Node) -> dict:
    # Queue with (cur_node, accumulated_path, cost_accumulated)
    queue = deque([(start, [start.name], 0)])

    visited = {start}
    
    while queue:
        cur_node, path, cost = queue.popleft()

        if cur_node == end:
            return {
                "success": True,
                "path": path,
                "cost": cost,
                "expanded_nodes": len(visited)
            }
        
        for neighbour, edge_cost in cur_node.neighbours:
            if neighbour not in visited:
                visited.add(neighbour)

                queue.append((neighbour, path + [neighbour.name], cost + edge_cost))
    
    return {
        "success": False,
        "path": None,
        "cost": float("inf"),
        "expanded_nodes": len(visited)
    }
