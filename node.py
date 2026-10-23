class Node:
    def __init__(self, name=None, cost=None, neighbours=None, heuristic=None):
        self.name = name

        self.cost = cost

        self.heuristic = heuristic

        self.neighbours = neighbours if neighbours is not None else []
    
    # Allows to use the heappq library
    def __lt__(self, other):
        return self.cost < other.cost

    # Better comparison
    def __eq__(self, value):
        return self.name == value.name
    
    def __hash__(self):
        return hash(self.name)