from node import Node

def dfs(start: Node, end: Node) -> dict:
    # We are going to use a stack to avoid stackoverflow of
    # the traditional recursive way
    stack = [(start, [start.name], 0)]

    visited = set()

    while stack:
        cur_node, path, cost = stack.pop()

        if cur_node in visited:
            continue

        visited.add(cur_node)

        if cur_node == end:
            return {
                "success": True,
                "path": path,
                "cost": cost,
                "expanded_nodes": len(visited)
            }

        # We reverse the neighbours to get the LIFO behavior of the stack
        for neighbour, edge_cost in cur_node.neighbours[::-1]:
            if neighbour not in visited:
                stack.append((neighbour, path + [neighbour.name], cost + edge_cost))
    
    return {
        "success": False,
        "path": None,
        "cost": float("inf"),
        "expanded_nodes": len(visited)
    }
