from utils import util
import networkx as nx # type: ignore
from timeout_decorator import timeout # type: ignore
import time

"""
Christofides(G):
    Step 1) Compute T uma árvore geradora mínima de G
    Step 2) Seja I o conjunto de vértices de grau ímpar de T. Compute M, um matching perfeito de peso mínimo no subgrafo induzido por I
    Step 3) Seja G' o multigrafo formado com os vértices de V e aresta de M e T. Compute um circuito euleriano eulerian_circuit em G' (aplicar DFS)
    Step 4) Elimine vértices duplicados, substituindo subcaminhos u-w-v por arestas u-v (Implicítamente é feito na conversão do circuito euleriano para o circuito hamiltoniano).
"""

@timeout(1800)
def approx_christofides_tour(G):
    start = time.time()
    # Step 1)
    MST_T = util.MST(G)
    
    # Step 2 (Parte 1)
    degrees = dict(MST_T.degree())
    I = util.get_odd_degress(degrees)

    # Step 2 (Parte 2)
    if not I:
        # Quando não há vértices de grau ímpar, não é necessário calcular o matching perfeito de peso mínimo
        G_prime = nx.MultiGraph(MST_T)
    elif len(I) % 2 == 0: 
        # Pelo lema do aperto de mão, I possui um número par de arestas. (Font: https://en.wikipedia.org/wiki/Christofides_algorithm)
        subgrafo_induzido_por_I = G.subgraph(I)
        M = nx.min_weight_matching(subgrafo_induzido_por_I)

    # Step 3)
        G_prime = nx.MultiGraph()
        for edge in M: G_prime.add_edge(*edge)
        for edge in MST_T.edges: G_prime.add_edge(*edge)

    if not all(degree % 2 == 0 for _, degree in G_prime.degree()):
        raise ValueError("Erro: O grafo G' gerado não possui circuito euleriano.")

    eulerian_circuit = util.eulerian_circuit(G_prime)
    
    # Step 4)
    max_node = G.number_of_nodes()
    H = util.shortcutting(eulerian_circuit, max_node)

    cost = util.cost_calculator_christophies(G, H)
    
    end = time.time()
    total_time = end - start
    
    return cost, total_time