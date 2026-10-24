> 🌐 **Language / Idioma:** **Português (Brasil)** | [English Version (AI_REPORT.md)](AI_REPORT.md)

# Relatório Técnico de Transparência e Uso de Inteligência Artificial
**Disciplina:** Inteligência Artificial  
**Instituição:** Universidade Estadual Paulista (UNESP)  
**Projeto:** Implementação e Aplicação de Algoritmos de Busca em Grafos (Malha Rodoviária Intercampus)  
**Repositório:** `Gabriel-Ciriaco/Searching_Algorithms`  

---

## 1. Declaração de Integridade Acadêmica e Metodologia

Este documento tem como objetivo relatar de forma transparente, detalhada e ética como ferramentas de Inteligência Artificial Generativa (atuando como copiloto de programação e consultoria técnica em modo *pair programming*) foram utilizadas no desenvolvimento deste trabalho prático.

A utilização da IA não teve como objetivo gerar uma solução automática sem intervenção humana. Pelo contrário, o processo seguiu um método de **engenharia orientada a diálogo (*interview-driven development / /grill-me*)**, onde o aluno guiou todas as tomadas de decisão de design, modelagem de problemas e arquitetura, utilizando o modelo para diagnóstico de erros de execução, revisão teórica e auxílio na construção da interface interativa em Matplotlib.

---

## 2. O que foi Desenvolvido Originalmente pelo Aluno

Antes de qualquer consulta ou refinamento assistido, o aluno já havia concebido e implementado de forma autoral a base estrutural do repositório:

1. **Implementação Preliminar dos 7 Algoritmos de Busca:**
   * Busca em Largura (`bfs.py`)
   * Busca em Profundidade (`dfs.py`)
   * Busca de Custo Uniforme (`ucs.py`)
   * Busca em Profundidade Limitada (`dls.py`)
   * Busca em Profundidade Iterativa (`ids.py`)
   * Busca Gananciosa (`greedy_best_first_search.py`)
   * Busca A* (`a_star.py`)
2. **Modelagem Orientada a Objetos dos Nós (`node.py`):**
   * Definição da classe `Node` com atributos de nome, custo, heurística e lista de vizinhos.
   * Implementação dos métodos especiais `__lt__`, `__eq__` e `__hash__` para viabilizar o uso em tabelas hash e filas de prioridade.
3. **Concepção do Cenário Prático Real:**
   * A ideia criativa de aplicar a busca em uma **malha logística de transporte entre os câmpus da UNESP** no Estado de São Paulo (Presidente Prudente, Assis, Marília, Ourinhos, Bauru, Botucatu, Araraquara, Rio Claro, São José do Rio Preto e Ilha Solteira) foi proposta integralmente pelo aluno.
4. **Visualização Inicial (`graph_visualizer.py`):**
   * Estruturação preliminar de renderização gráfica utilizando as bibliotecas `networkx` e `matplotlib`.

---

## 3. Diagnóstico Técnico de Falhas e Refatorações Apoiadas por IA

Durante a fase de testes e integração no arquivo `app.py`, o aluno utilizou o assistente de IA para conduzir um *code review* aprofundado. Esse processo identificou e corrigiu falhas conceituais e de sintaxe que impediam o funcionamento correto das buscas:

### 3.1. Busca em Largura (`bfs.py`)
* **Problema Identificado pelo Review:** O nó inicial estava sendo adicionado ao conjunto de visitados antes do laço (`visited = {start}`) e, na primeira iteração, a condição `if top in visited: continue` descartava a raiz imediatamente, fazendo com que o algoritmo retornasse `False` mesmo havendo caminho existente. Além disso, utilizava-se `heapq` ordenando por custo do nó, descaracterizando a política FIFO de busca em largura.
* **Correção Realizada:** Substituição do `heapq` por `collections.deque` com remoção à esquerda (`popleft()`), inclusão em `visited` no momento da inserção dos vizinhos e reconstrução dinâmica do caminho percorrido.

### 3.2. Busca em Profundidade (`dfs.py`)
* **Problema Identificado pelo Review:** A assinatura original continha o parâmetro padrão mutável `visited=set()`, armadilha clássica do Python em que chamadas consecutivas compartilham o mesmo conjunto na memória, gerando falsos negativos em testes subsequentes.
* **Correção Realizada:** Transição para uma implementação iterativa com pilha explícita (`stack`), imune a problemas de estouro de recursão (*RecursionError*) em grafos extensos.

### 3.3. Busca de Custo Uniforme (`ucs.py`)
* **Problema Identificado pelo Review:** Inconsistência de tipagem no dicionário de visitados: o nó inicial gravava um inteiro (`visited = {start: 0}`), enquanto os nós expandidos gravavam tuplas (`visited[viz] = (custo, no)`). Em caso de ciclos que retornassem à raiz, o acesso `visited[start][0]` quebrava com `TypeError`.
* **Correção Realizada:** Padronização do dicionário para armazenar estritamente o menor custo numérico acumulado por nó, e cálculo do custo acumulado somando o peso real da estrada (`edge_cost`), em vez de custo fixo municipal.

### 3.4. Profundidade Limitada e Iterativa (`dls.py` e `ids.py`)
* **Problema Identificado pelo Review:** O algoritmo DLS não diferenciava se a busca falhou por atingir o limite estipulado (*cutoff*) ou se o subgrafo havia terminado (*failure*). Isso forçava o algoritmo IDS a executar cegamente até 500 iterações quando uma cidade era inalcançável (como no teste de Ilha Solteira).
* **Correção Realizada:** Adição da flag de corte (`cutoff`), controle de ciclo pelo histórico do caminho (`neighbour.name not in path`) e parada antecipada no IDS assim que uma iteração esgota a malha sem gerar nenhum corte.

### 3.5. Busca A* (`a_star.py`)
* **Problema Identificado pelo Review:** A instrução `visited[neighbour].cost = total_g_cost` disparava erro fatal de `KeyError` (caso a chave não existisse) ou `AttributeError` (por tentar acessar `.cost` em um tipo primitivo float/int).
* **Correção Realizada:** Atribuição direta do custo `visited[neighbour] = total_g_cost` e garantia da ordenação por $f(n) = g(n) + h(n)$.

---

## 4. Padronização e Modelagem da Heurística

Para que todos os algoritmos pudessem ser comparados de forma justa e uniforme no trabalho:

1. **Retorno Unificado:** Todos os 7 algoritmos passaram a retornar um dicionário padronizado:
   ```python
   {
       "success": bool,          # Se o objetivo foi alcançado
       "path": list,             # Lista com os nomes das cidades na ordem
       "cost": float,            # Custo acumulado total (em R$ ou km)
       "expanded_nodes": int     # Métrica acadêmica de esforço computacional
   }
   ```
2. **Modelagem da Heurística Euclidiana:** A classe `Node` recebeu coordenadas relativas aproximadas em km no Estado de São Paulo (`x`, `y`). O cálculo $h(n) = \sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}$ foi estabelecido para fornecer uma estimativa geométrica admissível ($h(n) \le h^*(n)$) e consistente, válida para qualquer par de cidades.

---

## 5. Desenvolvimento do Dashboard Interativo no Matplotlib (`app.py`)

Em vez de um script com saídas estáticas de terminal, foi construído um **ambiente interativo em Matplotlib** utilizando seus componentes nativos (`matplotlib.widgets.Button` e `RadioButtons`):

* **Seleção Reativa de Cidades:** Menus de rádio à esquerda que permitem ao avaliador selecionar qualquer cidade de Origem e Destino com atualização imediata da rota no mapa.
* **Execução sob Demanda:** Botões dedicados para cada um dos 7 algoritmos e um botão especial de *Benchmark Comparativo*.
* **Controle Dinâmico de Passo do DLS:** Adição dos botões `[-]` e `[+]` na interface gráfica, permitindo alterar o limite $L$ em tempo real e visualizar na prática o instante em que a restrição de profundidade passa de corte (*cutoff*) para sucesso.
* **Painel Inferior de Métricas e Teoria:** Exibição sincronizada do propósito prático de cada busca, seus custos, saltos, nós expandidos e a justificativa pedagógica da decisão tomada pelo algoritmo.

---

## 6. O que NÃO foi Feito pela IA

Para garantir a transparência da autoria:

* **A IA não fez o trabalho de forma autônoma:** Nenhuma linha de código foi implementada sem solicitação, validação e refinamento conduzidos pelo aluno.
* **A IA não inventou o tema nem a malha:** A proposta das cidades da UNESP e conexões rodoviárias partiu do aluno.
* **A IA não decidiu o estilo de código final:** Após uma primeira versão que continha padrões verbosos típicos de geradores de texto, o aluno exigiu a refatoração do código para preservar seu estilo autêntico (comentários breves em inglês, ausência de divisórias artificiais e nomenclatura limpa).

---

## 7. Quadro Resumo de Atribuições

| Componente / Etapa | Papel do Aluno | Papel do Assistente de IA |
| :--- | :--- | :--- |
| **Algoritmos de Busca Base** | Concepção e codificação inicial dos 7 arquivos. | Revisão de código, detecção de bugs e correção de laços. |
| **Classe de Nós (`node.py`)** | Criação inicial e lógica de hash/igualdade. | Adição de método de distância euclidiana e segurança no `__lt__`. |
| **Cenário Prático da UNESP** | Escolha do tema, seleção das cidades e distâncias reais. | Organização das arestas ponderadas na estrutura do grafo. |
| **Teoria de Heurísticas** | Compreensão dos conceitos de admissibilidade. | Validação formal de otimalidade entre UCS e A*. |
| **Interface Gráfica (`app.py`)** | Definição dos requisitos (Dashboard sem terminal, controle DLS). | Implementação dos widgets nativos do Matplotlib e layout 16:9. |
| **Refatoração de Estilo** | Instrução de descaracterização do padrão "IA" para código pessoal. | Aplicação das regras de formatação e remoção de redundâncias. |

---

## 8. Reflexão Crítica e Aprendizados

O uso de Inteligência Artificial como ferramenta de programação em par demonstrou alto valor formativo:
1. Permitiu transformar erros sutis de implementação (como a diferença entre filas de prioridade e filas FIFO no BFS, ou mutabilidade de parâmetros em Python) em oportunidades reais de aprendizado teórico.
2. Viabilizou a criação de uma ferramenta visual rica em recursos pedagógicos, proporcionando uma compreensão muito mais intuitiva sobre como cada algoritmo navega no espaço de estados.
3. Consolidou o entendimento prático de que **UCS e A\* encontram exatamente a mesma rota ótima**, mas o A\* atinge o objetivo expandindo significativamente menos nós (até 62% de economia de processamento na malha testada) graças à heurística admissível.
