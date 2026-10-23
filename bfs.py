from collections import deque
from node import Node

def bfs(start, end):
    pq = [start]

    visited = {}
    
    while pq:
        top = deque.popleft(pq)

        if top in visited:
            continue

        if top == end:
            return True
        
        for n in top.neighbours:
            visited.add(n)

            deque.append(pq, n)
    
    return False

if __name__ == "__main__":

    # --- Configuração dos Nós ---
    node_a = Node("A", cost=1)
    node_b = Node("B", cost=2)
    node_c = Node("C", cost=3)
    node_d = Node("D", cost=4) # Nó isolado

    # Criando as conexões (Grafo linear: A -> B -> C)
    node_a.neighbours = [node_b]
    node_b.neighbours = [node_c]

    # --- Caso 1: Caminho Direto Existente (A até C) ---
    res1 = bfs(node_a, node_c)
    print(f"Caso 1 (Caminho A -> C): Esperado: True | Obtido: {res1}")

    # --- Caso 2: Destino Inalcançável (A até D) ---
    res2 = bfs(node_a, node_d)
    print(f"Caso 2 (Caminho A -> D): Esperado: False | Obtido: {res2}")

    # --- Caso 3: Início já é o Destino (A até A) ---
    res3 = bfs(node_a, node_a)
    print(f"Caso 3 (Início == Fim): Esperado: True | Obtido: {res3}")