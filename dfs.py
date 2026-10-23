from node import Node

def dfs(start, end):
    if start in visited:
        return False

    if start == end:
        return True

    visited.add(start)

    for n in start.neighbours:
        if dfs(n, end, visited):
            return True
    
    return False


if __name__ ==  "__main__":
 # --- Configuração dos Nós ---
    node_a = Node("A", cost=1)
    node_b = Node("B", cost=2)
    node_c = Node("C", cost=3)
    node_d = Node("D", cost=4) # Nó isolado

    # Criando as conexões (Grafos)
    node_a.neighbours = [node_b]
    node_b.neighbours = [node_c] # Caminho linear: A -> B -> C

    # --- Caso 1: Caminho Direto Existente (A até C) ---
    visited1 = set()
    res1 = dfs(node_a, node_c, visited1)
    print(f"Caso 1 (Caminho A -> C): Esperado: True | Obtido: {res1}")

    # --- Caso 2: Destino Inalcançável (A até D) ---
    visited2 = set()
    res2 = dfs(node_a, node_d, visited2)
    print(f"Caso 2 (Caminho A -> D): Esperado: False | Obtido: {res2}")

    # --- Caso 3: Grafo com Ciclo (A -> B -> A) ---
    node_b.neighbours = [node_c, node_a] # B agora aponta de volta para A
    visited3 = set()
    res3 = dfs(node_a, node_c, visited3)
    print(f"Caso 3 (Ciclo A -> B -> A): Esperado: True | Obtido: {res3}")

    # --- Caso 4: Início já é o Destino (A até A) ---
    visited4 = set()
    res4 = dfs(node_a, node_a, visited4)
    print(f"Caso 4 (Início == Fim): Esperado: True | Obtido: {res4}")
