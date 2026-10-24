class Node:
    def __init__(self, name=None, cost=None, neighbours=None, x=0, y=0):
        self.name = name

        self.cost = cost

        self.neighbours = neighbours if neighbours is not None else []

        # Coordinates for the node
        self.x = x
        self.y = y
    
    def add_neighbour(self, node, cost=1.0):
        self.neighbours.append((node, cost))

    # The heuristic function is the euclidian distance to the target node
    def distance_to(self, other_node):
        return ((self.x - other_node.x)**2 + (self.y - other_node.y)**2)**0.5

    # Allows to use the heappq library
    def __lt__(self, other):
        return str(self.name) < str(other.name)

    # Better comparison
    def __eq__(self, value):
        # Ensure the value is a Node
        if not isinstance(value, Node):
            return False

        return self.name == value.name
    
    def __hash__(self):
        return hash(self.name)