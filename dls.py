from node import Node

def dls(start: Node, end: Node, l=0) -> dict:
    stack = [(start, [start.name], 0, 0)]

    visited = set()

    any_cutoff = False

    while stack:
        cur_node, path, cost, cur_l = stack.pop()

        if cur_node == end:
            return {
                "success":True,
                "path": path,
                "cost": cost,
                "cutoff": False,
                "expanded_nodes": len(visited)
            }

        # If we reached the limite, mark as cutoff and continue
        if cur_l >= l:
            any_cutoff = True
            continue

        visited.add(cur_node)

        for neighbour, edge_cost in cur_node.neighbours[::-1]:
            if neighbour not in visited:
                stack.append((
                    neighbour,
                    path + [neighbour.name],
                    cost + edge_cost,
                    cur_l + 1
                ))

    return {
        "success": False,
        "path": None,
        "cost": float("inf"),
        "cutoff": any_cutoff,
        "expanded_nodes": len(visited)
    }
