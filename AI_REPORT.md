> 🌐 **Language / Idioma:** **English** | [Versão em Português (RELATORIO_IA.md)](RELATORIO_IA.md)

# Technical Report: Transparency and Use of Artificial Intelligence
**Course:** Artificial Intelligence  
**Institution:** São Paulo State University (UNESP)  
**Project:** Implementation and Application of Graph Search Algorithms (Intercampus Highway Network)  
**Repository:** `Gabriel-Ciriaco/Searching_Algorithms`  

---

## 1. Academic Integrity Declaration and Methodology

This document provides a transparent, detailed, and ethical account of how Generative Artificial Intelligence tools were utilized as a programming copilot and technical consultant in a **pair-programming** workflow during this practical assignment.

The objective was not to produce an unassisted, black-box solution. Instead, the project followed an **interview-driven development methodology (/grill-me)**, in which the student led all design decisions, problem modeling, and software architecture, utilizing the AI model for runtime diagnostics, theoretical reviews, and assistance with building the interactive Matplotlib dashboard.

---

## 2. Original Work Developed by the Student

Prior to technical consultation and assisted refactoring, the student had independently conceived and implemented the core foundation of the repository:

1. **Preliminary Implementation of All 7 Search Algorithms:**
   * Breadth-First Search (`bfs.py`)
   * Depth-First Search (`dfs.py`)
   * Uniform Cost Search (`ucs.py`)
   * Depth-Limited Search (`dls.py`)
   * Iterative Deepening Search (`ids.py`)
   * Greedy Best-First Search (`greedy_best_first_search.py`)
   * A* Search (`a_star.py`)
2. **Object-Oriented Node Modeling (`node.py`):**
   * Definition of the `Node` class with name, cost, heuristic, and neighbor list attributes.
   * Implementation of Python special methods (`__lt__`, `__eq__`, and `__hash__`) to enable use in hash tables and priority queues.
3. **Conception of the Real-World Scenario:**
   * The creative application of graph search to an **intercampus highway logistics network connecting UNESP campus cities** across São Paulo State (Presidente Prudente, Assis, Marília, Ourinhos, Bauru, Botucatu, Araraquara, Rio Claro, São José do Rio Preto, and Ilha Solteira) was proposed entirely by the student.
4. **Initial Visualization (`graph_visualizer.py`):**
   * Early graph rendering structure using `networkx` and `matplotlib`.

---

## 3. Technical Diagnostics and AI-Assisted Refactorings

During testing and integration into `app.py`, the student used the AI assistant to conduct a thorough code review. This process identified and resolved key conceptual and execution bugs:

### 3.1. Breadth-First Search (`bfs.py`)
* **Identified Bug:** The root node was added to the visited set prior to entering the loop (`visited = {start}`). On the first iteration, `if top in visited: continue` immediately discarded the root without expanding its neighbors, causing the algorithm to return `False` even when valid paths existed. Furthermore, `heapq` was used, ordering by node cost and violating the pure FIFO queue requirement of breadth-first search.
* **Resolution:** Replaced `heapq` with `collections.deque` and left-side popping (`popleft()`), added nodes to `visited` upon enqueueing, and implemented dynamic path and cost tracking.

### 3.2. Depth-First Search (`dfs.py`)
* **Identified Bug:** The function signature contained a mutable default parameter (`visited=set()`), a known Python pitfall where consecutive calls share the same set in memory, leading to false negatives on subsequent runs.
* **Resolution:** Migrated to an iterative implementation using an explicit `stack`, avoiding recursion depth limits (*RecursionError*) on larger graphs.

### 3.3. Uniform Cost Search (`ucs.py`)
* **Identified Bug:** Type inconsistency in the visited dictionary: the root node stored an integer (`visited = {start: 0}`), whereas expanded nodes stored tuples (`visited[neighbor] = (cost, node)`). When cycles returned to the root, accessing `visited[start][0]` raised a `TypeError`.
* **Resolution:** Standardized the dictionary to store purely the minimum numeric accumulated cost per node, and accumulated road edge weights (`edge_cost`) rather than fixed city entrance costs.

### 3.4. Depth-Limited and Iterative Deepening Search (`dls.py` and `ids.py`)
* **Identified Bug:** DLS did not distinguish between a search that reached the depth limit (*cutoff*) versus a subtree that was fully exhausted (*failure*). This forced IDS to run blindly up to 500 iterations when a destination was unreachable (such as the isolated city of Ilha Solteira).
* **Resolution:** Implemented a cutoff flag, path-based cycle detection (`neighbor.name not in path`), and early termination in IDS as soon as an entire iteration finishes without triggering a cutoff.

### 3.5. A* Search (`a_star.py`)
* **Identified Bug:** The line `visited[neighbor].cost = total_g_cost` threw fatal `KeyError` (if the key did not exist) or `AttributeError` (attempting to set `.cost` on a primitive float/int).
* **Resolution:** Updated direct cost assignment `visited[neighbor] = total_g_cost` and enforced evaluation by $f(n) = g(n) + h(n)$.

---

## 4. Standardization and Heuristic Modeling

To enable a fair and uniform benchmark across all search strategies:

1. **Unified Return Format:** All 7 algorithms return a standardized dictionary:
   ```python
   {
       "success": bool,          # Whether the target city was reached
       "path": list,             # Ordered sequence of visited city names
       "cost": float,            # Total accumulated cost (in R$ or km)
       "expanded_nodes": int     # Academic metric of computational search effort
   }
   ```
2. **Euclidean Heuristic Modeling:** The `Node` class received approximate Cartesian coordinates (`x`, `y`) in km across São Paulo State. The euclidean straight-line distance $h(n) = \sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}$ was adopted, guaranteeing an admissible ($h(n) \le h^*(n)$) and consistent estimate for any pair of origin and destination cities.

---

## 5. Development of the Interactive Matplotlib Dashboard (`app.py`)

Instead of static console scripts, an interactive desktop application was built using native Matplotlib widgets (`matplotlib.widgets.Button` and `RadioButtons`):

* **Reactive City Selectors:** Side radio button menus allowing real-time selection of any Origin and Destination city with instant map recalculation.
* **On-Demand Search Execution:** Dedicated buttons for each of the 7 algorithms plus an analytical *Benchmark Comparison* mode.
* **Real-Time DLS Step Controls:** Interactive `[-]` and `[+]` buttons allowing users to step through depth limit $L$ live, demonstrating the exact transition from cutoff to success.
* **Dynamic Metric Panel:** Real-time display showing algorithmic purpose, status, road cost, hops, nodes expanded, and theoretical explanations.

---

## 6. What Was NOT Done by AI

To preserve academic authorship integrity:

* **No Autonomous Generation:** No code was produced without explicit instruction, verification, and technical refinement by the student.
* **Original Network & Problem Design:** The UNESP highway logistics theme and real-world road connections were designed by the student.
* **Preservation of Authentic Coding Style:** After an initial prototype featuring verbose AI-style headers and comments, the student mandated a complete refactoring to reflect their personal coding style (concise English comments, clean spacing, and uncluttered button labels).

---

## 7. Responsibility Matrix

| Component / Task | Student Role | AI Assistant Role |
| :--- | :--- | :--- |
| **Base Search Algorithms** | Authorial implementation of all 7 algorithms. | Code review, bug identification, and loop correction. |
| **Node Class (`node.py`)** | Class structure, hashing, and equality methods. | Euclidean distance method and priority queue tie-breaking. |
| **UNESP Real-World Network** | Problem proposal, city selection, and highway costs. | Graph edge modeling and coordinate layout. |
| **Heuristic Theory** | Conceptual understanding of admissibility. | Theoretical validation of optimality between UCS and A*. |
| **Desktop GUI (`app.py`)** | Requirements specification (Dashboard, live DLS). | Matplotlib widget implementation and 16:9 layout. |
| **Style Refactoring** | Instruction to remove AI tropes and match personal style. | Code clean-up, concise comments, and formatting. |

---

## 8. Critical Reflection and Key Learnings

Using AI as a pair-programming partner provided significant pedagogical value:
1. Subtle programming traps (such as FIFO queues vs. priority queues in BFS, or mutable default arguments in Python) were converted into concrete conceptual learning moments.
2. Building an interactive visualization deepened intuition regarding state-space exploration across informed and uninformed algorithms.
3. The project practically confirmed that **UCS and A* always find the exact same optimal financial cost**, but A* achieves this with significantly fewer node expansions (up to 62% search effort reduction on the tested UNESP network) thanks to its admissible heuristic.
