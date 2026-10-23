def dls(start, end, visited, cur_l=0, l=0):
    if start == end:
        return True

    if start in visited or cur_l >= l:
        return False

    
    visited.add(start)

    for n in start.neighbours:
        if dls(n, end, visited, cur_l + 1, l):
            return True

    # Allows to explor shorter paths in other ramifications    
    visited.remove(start)

    return False

if __name__ ==  "__main__":
    from node import Node

    # Grafo em linha: A -> B -> C
    node_a = Node("A")
    node_b = Node("B")
    node_c = Node("C")
    
    node_a.neighbours = [node_b]
    node_b.neighbours = [node_c]

    # --- Caso 1: Destino dentro do limite (Limite = 2, C está no nível 2) ---
    v1 = set()
    res1 = dls(node_a, node_c, v1, cur_l=0, l=2)
    print(f"Caso 1 (Limite suficiente): Esperado: True | Obtido: {res1}")

    # --- Caso 2: Destino fora do limite (Limite = 1, C está no nível 2) ---
    v2 = set()
    res2 = dls(node_a, node_c, v2, cur_l=0, l=1)
    print(f"Caso 2 (Limite curto): Esperado: False | Obtido: {res2}")