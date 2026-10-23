import heapq

def a_star(start, end):
    pq = [(start.heuristic, 0, start)]

    visited = {start: 0}

    while pq:
        _, g_cost, cur_node = heapq.heappop(pq)

        if cur_node == end:
            return g_cost
        
        for neighbour in cur_node.neighbours:
            total_g_cost = g_cost + neighbour.cost

            total_f_cost = total_g_cost + neighbour.heuristic

            if neighbour not in visited or \
                total_g_cost < visited[neighbour]:
                visited[neighbour] = total_g_cost

                heapq.heappush(pq, (total_f_cost, total_g_cost, neighbour))
    
    return None

if __name__ ==  "__main__":
    from node import Node
    # --- Configuração dos Nós ---
    node_start = Node("Início")
    node_rota_b = Node("Rota B_Longa") # Rota longa em nós, mas barata em custo
    node_rota_g = Node("Rota G_Gananciosa") # Parece perto por heurística, mas é caríssima
    node_goal = Node("Destino")
    node_isolado = Node("Isolado")

    # 1. Definindo os custos individuais das arestas/nós (g(n))
    node_start.cost = 0
    node_rota_b.cost = 1   # Caminho muito barato
    node_rota_g.cost = 10  # Caminho muito caro
    node_goal.cost = 2     # Custo para entrar no destino
    node_isolado.cost = 5

    # 2. Definindo as Heurísticas (h(n) = estimativa em linha reta até o Destino)
    node_start.heuristic = 6
    node_rota_b.heuristic = 5 # Heurística alta (parece longe no mapa)
    node_rota_g.heuristic = 1 # Heurística baixa (parece colado no destino)
    node_goal.heuristic = 0   # Objetivo sempre tem heurística 0
    node_isolado.heuristic = 10

    # 3. Criando as conexões do Grafo
    # Do Início você pode escolher ir pela rota barata (B) ou pela ilusão gananciosa (G)
    node_start.neighbours = [node_rota_b, node_rota_g]
    
    # Ambas chegam ao mesmo destino
    node_rota_b.neighbours = [node_goal]
    node_rota_g.neighbours = [node_goal]

    print("=== Testes do Algoritmo A* ===")

    # --- Caso 1: Rota Ótima (Início até Destino) ---
    # Caminho B: custo 1 + 2 = 3. Caminho G: custo 10 + 2 = 12. 
    # O A* deve escolher o caminho B (Custo total: 3).
    res1 = a_star(node_start, node_goal)
    print(f"Caso 1 (Rota Eficiente): Esperado: 3 | Obtido: {res1}")

    # --- Caso 2: Destino Inalcançável ---
    res2 = a_star(node_start, node_isolado)
    print(f"Caso 2 (Nó Isolado): Esperado: None | Obtido: {res2}")

    # --- Caso 3: Início já é o Destino ---
    res3 = a_star(node_start, node_start)
    print(f"Caso 3 (Início == Fim): Esperado: 0 | Obtido: {res3}")

