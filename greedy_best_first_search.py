import heapq

def greedy_best_first_search(start, end):
    visited = set()

    pq = []

    heapq.heappush(pq, (start.heuristic, start))

    while pq:
        _, cur_node = heapq.heappop(pq)

        if cur_node == end:
            return True
        
        if cur_node == end:
            return True
        
        if cur_node not in visited:
            visited.add(cur_node)

            for neighbour in cur_node.neighbours:
                if neighbour not in visited:
                    heapq.heappush(pq, (neighbour.heuristic, neighbour))
    
    return False

if __name__ ==  "__main__":
    from node import Node
    # --- Configuração dos Nós (Simulando sua classe Node com o atributo heuristic) ---
    node_a = Node("A")
    node_b = Node("B")
    node_c = Node("C")
    node_d = Node("D") # Nó isolado

    # Definindo as Heurísticas (h(n) = estimativa de distância até o objetivo 'C')
    node_a.heuristic = 5  # Distante do objetivo
    node_b.heuristic = 2  # Mais perto do objetivo
    node_c.heuristic = 0  # O objetivo sempre tem heurística 0
    node_d.heuristic = 10 # Muito distante e isolado

    # Criando as conexões (Grafo linear: A -> B -> C)
    node_a.neighbours = [node_b]
    node_b.neighbours = [node_c]

    print("=== Testes do Greedy Best-First Search ===")

    # --- Caso 1: Caminho Existente até o Objetivo ---
    res1 = greedy_best_first_search(node_a, node_c)
    print(f"Caso 1 (Caminho A -> C): Esperado: True | Obtido: {res1}")

    # --- Caso 2: Destino Inalcançável ---
    res2 = greedy_best_first_search(node_a, node_d)
    print(f"Caso 2 (Caminho A -> D): Esperado: False | Obtido: {res2}")

    # --- Caso 3: Início já é o Destino ---
    res3 = greedy_best_first_search(node_a, node_a)
    print(f"Caso 3 (Início == Fim): Esperado: True | Obtido: {res3}")
