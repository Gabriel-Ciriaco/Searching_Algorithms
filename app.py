import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons

from node import Node
from dfs import dfs
from bfs import bfs
from ucs import ucs
from dls import dls
from ids import ids
from greedy_best_first_search import greedy_best_first_search
from a_star import a_star


def build_network():
    # City coordinates in SP state (approximate km)
    cidades = {
        "Presidente Prudente": Node("Presidente Prudente", x=0, y=50),
        "Assis": Node("Assis", x=125, y=30),
        "Marília": Node("Marília", x=160, y=90),
        "Ourinhos": Node("Ourinhos", x=190, y=10),
        "Bauru": Node("Bauru", x=265, y=70),
        "Botucatu": Node("Botucatu", x=340, y=40),
        "Araraquara": Node("Araraquara", x=350, y=130),
        "Rio Claro": Node("Rio Claro", x=410, y=95),
        "São José do Rio Preto": Node("São José do Rio Preto", x=220, y=210),
        "Ilha Solteira": Node("Ilha Solteira", x=80, y=260)  # Isolated node to test unreachable goal
    }

    # Connect bidirectional roads with distances
    def connect(a, b, dist):
        a.add_neighbour(b, dist)
        b.add_neighbour(a, dist)

    connect(cidades["Presidente Prudente"], cidades["Assis"], 126)
    connect(cidades["Presidente Prudente"], cidades["Marília"], 178)
    connect(cidades["Assis"], cidades["Ourinhos"], 74)
    connect(cidades["Assis"], cidades["Bauru"], 204)
    connect(cidades["Marília"], cidades["Bauru"], 105)
    connect(cidades["Marília"], cidades["São José do Rio Preto"], 185)
    connect(cidades["Ourinhos"], cidades["Bauru"], 128)
    connect(cidades["Bauru"], cidades["Botucatu"], 93)
    connect(cidades["Bauru"], cidades["Araraquara"], 134)
    connect(cidades["Botucatu"], cidades["Rio Claro"], 145)
    connect(cidades["Araraquara"], cidades["Rio Claro"], 75)

    return cidades


class RouteApp:
    def __init__(self):
        self.cidades = build_network()
        self.city_names = list(self.cidades.keys())

        self.cur_origem = "Presidente Prudente"
        self.cur_destino = "Bauru"
        self.cur_algo = "A*"
        self.dls_limit = 2

        # Setup networkx graph
        self.G = nx.Graph()
        self.positions = {}

        for c in self.cidades.values():
            self.G.add_node(c.name)
            self.positions[c.name] = (c.x, c.y)

        for c in self.cidades.values():
            for viz, peso in c.neighbours:
                self.G.add_edge(c.name, viz.name, weight=peso)

        # Window setup
        self.fig = plt.figure(figsize=(16, 9), facecolor="#f5f7fa")
        self.fig.canvas.manager.set_window_title("UNESP - Roteirizador com Algoritmos de Busca")

        self.fig.suptitle(
            "SISTEMA DE ROTEIRIZAÇÃO INTERCAMPUS UNESP - IA",
            fontsize=13, fontweight="bold", y=0.975, color="#0d47a1"
        )

        # Origin and destination selectors
        self.ax_origem = self.fig.add_axes([0.015, 0.52, 0.125, 0.41], facecolor="#ffffff")
        self.ax_destino = self.fig.add_axes([0.015, 0.05, 0.125, 0.41], facecolor="#ffffff")

        self.radio_origem = RadioButtons(self.ax_origem, self.city_names, active=0)
        self.radio_destino = RadioButtons(self.ax_destino, self.city_names, active=4)

        for lbl in self.radio_origem.labels:
            lbl.set_fontsize(7.5)
        for lbl in self.radio_destino.labels:
            lbl.set_fontsize(7.5)

        self.ax_origem.set_title("Cidade Origem", fontsize=8.5, fontweight="bold", color="#1565c0", pad=6)
        self.ax_destino.set_title("Cidade Destino", fontsize=8.5, fontweight="bold", color="#e65100", pad=6)

        # Algorithm buttons layout
        btn_x = 0.148
        btn_w = 0.136
        btn_h = 0.043

        self.ax_btn_bfs = self.fig.add_axes([btn_x, 0.880, btn_w, btn_h])
        self.ax_btn_ucs = self.fig.add_axes([btn_x, 0.825, btn_w, btn_h])
        self.ax_btn_dfs = self.fig.add_axes([btn_x, 0.770, btn_w, btn_h])
        self.ax_btn_dls = self.fig.add_axes([btn_x, 0.715, btn_w, btn_h])

        # DLS step controls [-] [ L = 2 ] [+]
        ctl_y = 0.672
        ctl_h = 0.034
        self.ax_dls_minus = self.fig.add_axes([btn_x, ctl_y, 0.036, ctl_h])
        self.ax_dls_label = self.fig.add_axes([btn_x + 0.040, ctl_y, 0.056, ctl_h], facecolor="#fff3e0")
        self.ax_dls_plus  = self.fig.add_axes([btn_x + 0.100, ctl_y, 0.036, ctl_h])

        self.ax_btn_ids = self.fig.add_axes([btn_x, 0.615, btn_w, btn_h])
        self.ax_btn_greedy = self.fig.add_axes([btn_x, 0.560, btn_w, btn_h])
        self.ax_btn_astar = self.fig.add_axes([btn_x, 0.505, btn_w, btn_h])
        self.ax_btn_bench = self.fig.add_axes([btn_x, 0.405, btn_w, 0.065])

        # Action buttons
        self.btn_bfs = Button(self.ax_btn_bfs, "BFS (Menos Saltos)", color="#e3f2fd", hovercolor="#bbdefb")
        self.btn_ucs = Button(self.ax_btn_ucs, "UCS (Menor Custo)", color="#e8f5e9", hovercolor="#c8e6c9")
        self.btn_dfs = Button(self.ax_btn_dfs, "DFS (Profundidade)", color="#fbe9e7", hovercolor="#ffccbc")
        self.btn_dls = Button(self.ax_btn_dls, "DLS (Corte por Limite)", color="#fff3e0", hovercolor="#ffe0b2")

        self.btn_dls_minus = Button(self.ax_dls_minus, "-", color="#ffe0b2", hovercolor="#ffcc80")
        self.btn_dls_plus  = Button(self.ax_dls_plus, "+", color="#ffe0b2", hovercolor="#ffcc80")

        self.ax_dls_label.axis("off")
        self.dls_label_text = self.ax_dls_label.text(
            0.5, 0.5, f"L = {self.dls_limit}",
            fontsize=8.5, fontweight="bold", color="#e65100",
            ha="center", va="center"
        )

        self.btn_ids = Button(self.ax_btn_ids, "IDS (Aprofundamento)", color="#ede7f6", hovercolor="#d1c4e9")
        self.btn_greedy = Button(self.ax_btn_greedy, "Greedy (Ganancioso)", color="#fffde7", hovercolor="#fff9c4")
        self.btn_astar = Button(self.ax_btn_astar, "A* (Ótimo Admissível)", color="#e0f7fa", hovercolor="#b2ebf2")
        self.btn_bench = Button(self.ax_btn_bench, "Comparar Todos", color="#ffd54f", hovercolor="#ffca28")

        for b in [self.btn_bfs, self.btn_ucs, self.btn_dfs, self.btn_dls, self.btn_ids, self.btn_greedy, self.btn_astar, self.btn_bench]:
            b.label.set_fontsize(7.5)
            b.label.set_fontweight("bold")

        self.btn_dls_minus.label.set_fontsize(9)
        self.btn_dls_minus.label.set_fontweight("bold")
        self.btn_dls_plus.label.set_fontsize(9)
        self.btn_dls_plus.label.set_fontweight("bold")

        # Main graph axes and bottom info card
        self.ax_map = self.fig.add_axes([0.295, 0.28, 0.690, 0.61], facecolor="#ffffff")
        self.ax_info = self.fig.add_axes([0.295, 0.04, 0.690, 0.20], facecolor="#ffffff")

        # Event connections
        self.radio_origem.on_clicked(self.on_change_origem)
        self.radio_destino.on_clicked(self.on_change_destino)

        self.btn_bfs.on_clicked(lambda event: self.run_search("BFS"))
        self.btn_ucs.on_clicked(lambda event: self.run_search("UCS"))
        self.btn_dfs.on_clicked(lambda event: self.run_search("DFS"))
        self.btn_dls.on_clicked(lambda event: self.run_search("DLS"))
        self.btn_dls_minus.on_clicked(self.on_dls_minus)
        self.btn_dls_plus.on_clicked(self.on_dls_plus)
        self.btn_ids.on_clicked(lambda event: self.run_search("IDS"))
        self.btn_greedy.on_clicked(lambda event: self.run_search("Greedy"))
        self.btn_astar.on_clicked(lambda event: self.run_search("A*"))
        self.btn_bench.on_clicked(lambda event: self.run_all())

        # Start with A*
        self.run_search("A*")

    def on_change_origem(self, label):
        self.cur_origem = label
        if self.cur_algo == "BENCHMARK":
            self.run_all()
        else:
            self.run_search(self.cur_algo)

    def on_change_destino(self, label):
        self.cur_destino = label
        if self.cur_algo == "BENCHMARK":
            self.run_all()
        else:
            self.run_search(self.cur_algo)

    def on_dls_minus(self, event):
        if self.dls_limit > 0:
            self.dls_limit -= 1
            self.dls_label_text.set_text(f"L = {self.dls_limit}")
            self.run_search("DLS")

    def on_dls_plus(self, event):
        if self.dls_limit < 10:
            self.dls_limit += 1
            self.dls_label_text.set_text(f"L = {self.dls_limit}")
            self.run_search("DLS")

    def run_search(self, algo_name):
        self.cur_algo = algo_name
        origem = self.cidades[self.cur_origem]
        destino = self.cidades[self.cur_destino]

        # Call search algorithm
        if algo_name == "BFS":
            res = bfs(origem, destino)
            desc = "Busca em Largura (BFS): explora camada por camada, garantindo menor número de paradas."
            teoria = "Prioriza menos trocas de conexões, mesmo que o custo total seja maior."
            titulo_mapa = f"BFS | {self.cur_origem} -> {self.cur_destino}"

        elif algo_name == "UCS":
            res = ucs(origem, destino)
            desc = "Busca de Custo Uniforme (UCS): expande pelo menor custo financeiro acumulado."
            teoria = "Garante matematicamente a rota mais barata em R$, explorando caminhos de menor peso."
            titulo_mapa = f"UCS (Custo Uniforme) | {self.cur_origem} -> {self.cur_destino}"

        elif algo_name == "DFS":
            res = dfs(origem, destino)
            desc = "Busca em Profundidade (DFS): segue uma trilha até o fim antes de fazer backtracking."
            teoria = "Encontra um caminho viável, mas sem garantia de menor custo ou menos paradas."
            titulo_mapa = f"DFS | {self.cur_origem} -> {self.cur_destino}"

        elif algo_name == "DLS":
            res = dls(origem, destino, l=self.dls_limit)
            desc = f"Busca em Profundidade Limitada (DLS com Limite L = {self.dls_limit}): corta nós além do limite."
            if res["success"]:
                teoria = f"SUCESSO no Limite L={self.dls_limit}! Encontrou caminho respeitando a profundidade máxima."
            else:
                teoria = f"CORTE (CUTOFF) no Limite L={self.dls_limit}! Destino inalcançável com apenas {self.dls_limit} paradas. Clique no [+] para testar limites maiores."
            titulo_mapa = f"DLS (Limite L={self.dls_limit}) | {self.cur_origem} -> {self.cur_destino}"

        elif algo_name == "IDS":
            res = ids(origem, destino)
            desc = "Busca em Profundidade Iterativa (IDS): expande limites progressivos unindo BFS com economia de memória."
            teoria = "Acha a menor quantidade de escalas sem consumir a memória do BFS."
            titulo_mapa = f"IDS | {self.cur_origem} -> {self.cur_destino}"

        elif algo_name == "Greedy":
            res = greedy_best_first_search(origem, destino)
            desc = "Busca Gananciosa (Greedy): prioriza a estimativa euclidiana em linha reta (h)."
            teoria = "Rápido com poucos nós expandidos, mas pode escolher caminhos com arestas mais caras."
            titulo_mapa = f"Greedy | {self.cur_origem} -> {self.cur_destino}"

        elif algo_name == "A*":
            res = a_star(origem, destino)
            desc = "A*: Combina custo real g(n) com estimativa euclidiana h(n)."
            teoria = "Garante a rota de menor custo gastando menos expansões que o UCS graças à heurística."
            titulo_mapa = f"A* | {self.cur_origem} -> {self.cur_destino}"

        else:
            return

        # Render updates
        self.draw_map(highlighted_path=res.get("path"), title=titulo_mapa)
        self.update_panel(algo_name, desc, res, teoria)
        self.fig.canvas.draw_idle()

    def run_all(self):
        self.cur_algo = "BENCHMARK"
        origem = self.cidades[self.cur_origem]
        destino = self.cidades[self.cur_destino]

        algoritmos = [
            ("BFS", bfs(origem, destino)),
            ("UCS", ucs(origem, destino)),
            ("DFS", dfs(origem, destino)),
            (f"DLS (l={self.dls_limit})", dls(origem, destino, l=self.dls_limit)),
            ("IDS", ids(origem, destino)),
            ("Greedy", greedy_best_first_search(origem, destino)),
            ("A*", a_star(origem, destino)),
        ]

        melhor_caminho = None
        for nome, res in algoritmos:
            if nome == "A*" and res["success"]:
                melhor_caminho = res["path"]
            elif melhor_caminho is None and res["success"]:
                melhor_caminho = res["path"]

        self.draw_map(highlighted_path=melhor_caminho, title="Comparativo Geral - Rota Ótima A*")
        self.draw_table(algoritmos)
        self.fig.canvas.draw_idle()

    def draw_map(self, highlighted_path=None, title=""):
        self.ax_map.clear()
        self.ax_map.set_facecolor("#ffffff")
        self.ax_map.set_title(title, fontsize=10.5, fontweight="bold", pad=7, color="#0d47a1")

        # Draw base graph
        nx.draw_networkx_nodes(
            self.G, self.positions, ax=self.ax_map,
            node_color="#e3f2fd", node_size=1100, edgecolors="#1976d2", linewidths=1.5
        )
        nx.draw_networkx_labels(
            self.G, self.positions, ax=self.ax_map,
            font_size=7.5, font_weight="bold", font_color="#212121"
        )
        nx.draw_networkx_edges(
            self.G, self.positions, ax=self.ax_map,
            edge_color="#cfd8dc", width=1.5
        )

        edge_labels = nx.get_edge_attributes(self.G, "weight")
        nx.draw_networkx_edge_labels(
            self.G, self.positions, ax=self.ax_map,
            edge_labels=edge_labels, font_size=7, font_color="#546e7a"
        )

        # Highlight origin and destination
        if self.cur_origem in self.positions:
            nx.draw_networkx_nodes(
                self.G, self.positions, ax=self.ax_map,
                nodelist=[self.cur_origem], node_color="#42a5f5", node_size=1300, edgecolors="#0d47a1", linewidths=2.5
            )

        if self.cur_destino in self.positions:
            nx.draw_networkx_nodes(
                self.G, self.positions, ax=self.ax_map,
                nodelist=[self.cur_destino], node_color="#ff7043", node_size=1300, edgecolors="#bf360c", linewidths=2.5
            )

        # Highlight path
        if highlighted_path and len(highlighted_path) > 1:
            path_edges = [(highlighted_path[i], highlighted_path[i+1]) for i in range(len(highlighted_path)-1)]

            nx.draw_networkx_edges(
                self.G, self.positions, ax=self.ax_map,
                edgelist=path_edges, edge_color="#2e7d32", width=3.5
            )

            interm = [n for n in highlighted_path if n not in (self.cur_origem, self.cur_destino)]
            if interm:
                nx.draw_networkx_nodes(
                    self.G, self.positions, ax=self.ax_map,
                    nodelist=interm, node_color="#a5d6a7", node_size=1200, edgecolors="#1b5e20", linewidths=2
                )

        self.ax_map.axis("off")

    def update_panel(self, algo_name, desc, res, teoria):
        self.ax_info.clear()
        self.ax_info.set_facecolor("#f1f5f9")
        self.ax_info.axis("off")

        if res["success"]:
            status_text = "Sucesso (Caminho Encontrado)"
            status_color = "#1b5e20"
            caminho_text = " -> ".join(res["path"])
            custo_text = f"R$ {res['cost']:.1f} / km"
            saltos_text = f"{len(res['path']) - 1} saltos"
        else:
            status_text = "Falha (Destino Inalcançável)"
            status_color = "#b71c1c"
            caminho_text = "Nenhum caminho possível"
            custo_text = "N/A"
            saltos_text = "0 saltos"

        nos_text = f"{res.get('expanded_nodes', 'N/A')} nós visitados"

        self.ax_info.text(0.015, 0.88, f"Algoritmo: {algo_name} | Status: {status_text}", fontsize=9.5, fontweight="bold", color=status_color, va="top")
        self.ax_info.text(0.015, 0.68, f"Propósito: {desc}", fontsize=8, color="#263238", va="top")
        self.ax_info.text(0.015, 0.46, f"Métricas: Custo: {custo_text} | Saltos: {saltos_text} | Expansões: {nos_text}", fontsize=8.5, fontweight="bold", color="#0d47a1", va="top")
        self.ax_info.text(0.015, 0.28, f"Rota: {caminho_text}", fontsize=8, fontweight="bold", color="#37474f", va="top")
        self.ax_info.text(0.015, 0.10, f"Análise: {teoria}", fontsize=8, fontstyle="italic", color="#455a64", va="top")

    def draw_table(self, algoritmos):
        self.ax_info.clear()
        self.ax_info.set_facecolor("#f1f5f9")
        self.ax_info.axis("off")

        header = f"{'Algoritmo':<14} | {'Sucesso':<8} | {'Custo (R$)':<12} | {'Expansões':<10} | {'Rota Encontrada'}"
        linhas = [header, "-" * 92]

        for nome, res in algoritmos:
            suc = "Sim" if res["success"] else "Não"
            custo = f"R$ {res['cost']:.1f}" if res["success"] else "N/A"
            exp = str(res.get("expanded_nodes", "N/A"))
            rota = " -> ".join(res["path"]) if res["path"] else "Sem rota"
            linhas.append(f"{nome:<14} | {suc:<8} | {custo:<12} | {exp:<10} | {rota}")

        table_text = "\n".join(linhas)
        self.ax_info.text(
            0.015, 0.95,
            table_text,
            fontsize=7.2, family="monospace", color="#1a237e", va="top"
        )

    def show(self):
        plt.show()


if __name__ == "__main__":
    app = RouteApp()
    app.show()
