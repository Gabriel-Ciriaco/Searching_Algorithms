from node import Node
from dls import dls

def ids(start: Node, end: Node, max_l: int = 10) -> dict:
    l = 0
    expanded_nodes = 0

    while l <= max_l:
        res = dls(start, end, l=l)
        expanded_nodes += res["expanded_nodes"]

        if res["success"]:
            res["expanded_nodes"] = expanded_nodes
            return res
        
        # All achievable path was explored
        if not res.get("cutoff", False):
            break
        
        l += 1

    return {
        "success": False,
        "path": None,
        "cost": float("inf"),
        "expanded_nodes": expanded_nodes
    }
