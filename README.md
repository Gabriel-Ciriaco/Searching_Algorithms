<div align="center">
	<h1>Searching Algorithms
		<br/>
		<sub>UNESP Intercampus Route Planner & Classical AI Search Simulator</sub>
	</h1>
	<h4>A practical implementation and interactive Matplotlib dashboard comparing 7 classical graph search algorithms on the road network of São Paulo State University (UNESP).</h4>
</div>

---

* **7 Classical Search Algorithms**: BFS, DFS, UCS (Dijkstra), DLS, IDS, Greedy Best-First Search, and A*.
* **Real-World UNESP Logistics Scenario**: Models highway connections, toll/fuel costs, and geographical distances across São Paulo State campus cities (Presidente Prudente, Assis, Marília, Ourinhos, Bauru, Botucatu, Araraquara, Rio Claro, São José do Rio Preto, and Ilha Solteira).
* **Interactive Matplotlib Dashboard**: 100% native desktop GUI with dynamic city selection (`RadioButtons`), live recalculation, and real-time step controls (`[-]` and `[+]`) for depth-limited search (DLS).
* **Unified Metrics**: Compares travel costs, number of road hops, and nodes expanded across all algorithms.
* **AI Methodology & Transparency**: Fully documented pair-programming and review process available in [English (AI_REPORT.md)](AI_REPORT.md) and [Português (RELATORIO_IA.md)](RELATORIO_IA.md).

---

### Usage

#### 1. Running the Interactive Dashboard
Launch the standalone desktop visualization application:

```bash
python app.py
```

* Use the **RadioButtons** on the left to pick any Origin and Destination.
* Click any **Algorithm Button** to compute the route and display the path live on the map.
* Use the **[-]** and **[+]** controls to adjust the depth limit of DLS in real time and see cutoff vs. success.
* Click **Comparar Todos** to generate an analytical comparison table across all 7 algorithms.

#### 2. Using Search Algorithms in Python
Each search algorithm can also be imported and executed as an independent module:

```python
from node import Node
from a_star import a_star

# Define nodes with coordinates (x, y)
prudente = Node("Presidente Prudente", x=0, y=50)
marilia = Node("Marília", x=160, y=90)
bauru = Node("Bauru", x=265, y=70)

# Connect roads with edge costs
prudente.add_neighbour(marilia, cost=178)
marilia.add_neighbour(bauru, cost=105)

# Execute A* search
result = a_star(prudente, bauru)
print(result)

/*
{
  'success': True,
  'path': ['Presidente Prudente', 'Marília', 'Bauru'],
  'cost': 283,
  'expanded_nodes': 3
}
*/
```

#### 3. Running the Tests
The `tests/` folder contains an automated validation suite written with `pytest`:

```bash
pip install pytest networkx matplotlib
python -m pytest
```

* **Algorithms**: result format, start equal to destination, unreachable goals and paths that only exist in one direction.
* **Correctness**: BFS and IDS are compared with the minimum number of hops, and UCS and A* with the minimum cost, against an exhaustive enumeration of every simple path on random graphs.
* **DLS and IDS**: cutoff vs. failure, depth limit, early stop of IDS and paths first reached by a deeper branch.
* **UNESP Network**: bidirectional roads, admissible and consistent heuristic for every pair of cities, A* equal to UCS, unreachable Ilha Solteira and the benchmark table of this README.
* **Dashboard**: headless execution (`Agg` backend) of every button, the benchmark mode and the DLS step controls.

---

### Implemented Algorithms

| Algorithm | Search Type | Heuristic | UNESP Logistics Purpose | Optimality |
| :--- | :--- | :--- | :--- | :---: |
| **BFS** | Uninformed | None | Finds the route with the minimum number of bus connections/hops | Optimal in hops |
| **UCS** | Uninformed | None | Finds the cheapest financial route in fuel and toll costs ($g$) | Optimal in cost |
| **DFS** | Uninformed | None | Fast exploration following a single highway branch until the end | Suboptimal |
| **DLS** | Uninformed | None | Route planning constrained by a strict maximum limit of stops ($L$) | Optimal within $L$ |
| **IDS** | Uninformed | None | Discovers the minimum hop count iteratively with minimal memory | Optimal in hops |
| **Greedy** | Informed | Straight-line ($h$) | Ultra-fast compass/GPS directional search toward the target city | Suboptimal |
| **A\*** | Informed | Straight-line ($h$) | Global optimal route balancing road cost and euclidean distance ($g+h$) | Optimal & efficient |

---

### Benchmark Comparison (Prudente $\rightarrow$ Bauru)

| Algorithm | Success | Total Cost | Expanded Nodes | Computed Path |
| :--- | :---: | :---: | :---: | :--- |
| **BFS** | Yes | R$ 330.0 | 6 | Prudente $\rightarrow$ Assis $\rightarrow$ Bauru |
| **DFS** | Yes | R$ 328.0 | 4 | Prudente $\rightarrow$ Assis $\rightarrow$ Ourinhos $\rightarrow$ Bauru |
| **UCS** | Yes | **R$ 283.0** | 5 | Prudente $\rightarrow$ Marília $\rightarrow$ Bauru |
| **DLS ($L=2$)** | Yes | R$ 330.0 | 2 | Prudente $\rightarrow$ Assis $\rightarrow$ Bauru |
| **IDS** | Yes | R$ 330.0 | 3 | Prudente $\rightarrow$ Assis $\rightarrow$ Bauru |
| **Greedy** | Yes | **R$ 283.0** | **3** | Prudente $\rightarrow$ Marília $\rightarrow$ Bauru |
| **A\*** | Yes | **R$ 283.0** | **4** | Prudente $\rightarrow$ Marília $\rightarrow$ Bauru |

> **Key Takeaway:** UCS and A* always find the exact same optimal financial cost (R$ 283.0), but A* expands fewer nodes due to its admissible euclidean distance heuristic!

---

### Project Structure

```text
.
├── app.py                      # Interactive Matplotlib Dashboard
├── graph_visualizer.py         # NetworkX & Matplotlib visualization module
├── node.py                     # Node class with coordinates and edge weights
├── bfs.py                      # Breadth-First Search
├── dfs.py                      # Depth-First Search
├── ucs.py                      # Uniform Cost Search (Dijkstra)
├── dls.py                      # Depth-Limited Search
├── ids.py                      # Iterative Deepening Search
├── greedy_best_first_search.py # Greedy Best-First Search
├── a_star.py                   # A* Search
├── tests/                      # Automated validation suite (pytest)
│   ├── conftest.py             # Shared fixtures and headless backend
│   ├── test_node.py            # Node class
│   ├── test_search_algorithms.py # The 7 search algorithms
│   ├── test_unesp_network.py   # UNESP road network and README benchmark
│   └── test_app.py             # Interactive dashboard
├── AI_REPORT.md                # AI Transparency & Methodology Report (English)
└── RELATORIO_IA.md             # Relatório de Transparência e Metodologia de IA (Português)
```

---

### AI Transparency & Methodology

This project includes a comprehensive academic report detailing how Generative AI tools were used during development in pair-programming mode for code review, bug diagnostics, and UI construction.

Read the full report in [English (AI_REPORT.md)](AI_REPORT.md) or in [Português (RELATORIO_IA.md)](RELATORIO_IA.md).

---

## Author ✨

<table>
	<tr>
		<td align="center">
			<a href="https://github.com/Gabriel-Ciriaco">
				<img src="https://avatars.githubusercontent.com/u/66225865" width="100px;" alt=""/>
				<br>
				<sub>
					<b>Gabriel C. de Carvalho</b>
				</sub>
		</td>
	</tr>
</table>
