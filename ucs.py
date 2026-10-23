import heapq

def ucs(start, end):
    pq = [(0, start)]

    visited = {start: 0}

    while pq:
        cur_cost, cur_node = heapq.heappop(pq)

        # Goal reached, then pop the node with the lowest cost
        if cur_node == end:
            return cur_cost

        for neighbour in cur_node.neighbours:
            total_cost = cur_cost + neighbour.cost

            if neighbour not in visited or \
                total_cost < visited[neighbour][0]:
                
                visited[neighbour] = (total_cost, cur_node)

                heapq.heappush(pq, (total_cost, neighbour))
            
    return None
