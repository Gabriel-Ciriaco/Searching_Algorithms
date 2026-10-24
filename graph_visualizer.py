import networkx as nx
import matplotlib.pyplot as plt

class GraphVisualizer:
    def __init__(self):

        self.G = nx.Graph()
        self.positions = {}


    def add_node(self, node):
        self.G.add_node(node.name)

        self.positions[node.name] = (node.x, node.y)

    # Netowrkx configuration
    def add_edge(self, a, b, cost):
        self.G.add_edge(a.name, b.name, weight=cost)

    def visualize(self, highlighted_path=None, title=""):
        plt.figure(figsize=(11, 7))

        # Draw all the nodes
        nx.draw_networkx_nodes(
            self.G,
            self.positions,
            node_color="#d0e1fd",
            node_size=1200,
            edgecolors="#1a73e8"
        )
        nx.draw_networkx_labels(
            self.G,
            self.positions,
            font_size=8,
            font_weight="bold"
        )
        
        nx.draw_networkx_edges(
            self.G,
            self.positions,
            edge_color="#b0bec5",
            arrows=True,
            arrowsize=15,
            width=1.5
        )

        # Costos of the edges
        edge_labels = nx.get_edge_attributes(self.G, "weight")
        nx.draw_networkx_edge_labels(
            self.G,
            self.positions,
            edge_labels=edge_labels,
            font_size=7
        )

        # If there is a path to highlight, color the nodes and edges
        if highlighted_path and len(highlighted_path) > 1:
            path_edges = [
                (highlighted_path[i], highlighted_path[i+1]) for i in range(len(highlighted_path)-1)
            ]

            nx.draw_networkx_nodes(
                self.G,
                self.positions,
                nodelist=highlighted_path,
                node_color="#a5d6a7",
                node_size=1300,
                edgecolors="#2e7d32"
            )

            nx.draw_networkx_edges(
                self.G,
                self.positions,
                edgelist=path_edges,
                edge_color="#2e7d32",
                width=3,
                arrows=True,
                arrowsize=20
            )
        
        # Title and axes
        plt.title(title, fontsize=12, fontweight="bold")
        plt.axis("off")
        plt.tight_layout()
        plt.show()
