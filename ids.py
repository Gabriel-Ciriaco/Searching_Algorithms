from dls import dls

def ids(start, end, max_l=500):
    l = 0
    while l <= max_l:
        res = dls(start, end, set(), l=l)

        if res:
            return res
        
        l += 1
    
    return False
    

if __name__ ==  "__main__":
    from node import Node

    # Grafo em linha: A -> B -> C
    node_a = Node("A")
    node_b = Node("B")
    node_c = Node("C")
    node_d = Node("D") # Nó totalmente isolado
    
    node_a.neighbours = [node_b]
    node_b.neighbours = [node_c]

    print("=== Testes do DLS ===")
    v1 = set()
    res1 = dls(node_a, node_c, v1, cur_l=0, l=2)
    print(f"Caso 1 (DLS Limite suficiente): Esperado: True | Obtido: {res1}")

    v2 = set()
    res2 = dls(node_a, node_c, v2, cur_l=0, l=1)
    print(f"Caso 2 (DLS Limite curto): Esperado: False | Obtido: {res2}")

    print("\n=== Testes do IDS ===")
    # --- Caso 3: IDS deve achar o nó C aumentando o limite sozinho ---
    res3 = ids(node_a, node_c)
    print(f"Caso 3 (IDS alcança C): Esperado: True | Obtido: {res3}")

    # --- Caso 4: IDS tenta buscar um nó que não existe ---
    res4 = ids(node_a, node_d)
    print(f"Caso 4 (IDS nó inalcançável): Esperado: False | Obtido: {res4}")