# -*- coding: utf-8 -*-

from utils import *
import heapq

def ordenaEdgesPesos(Graph):
    ordenados = []

    for i in range(Graph.number_of_nodes()):
        aux = [(chave, dados['weight']) for chave, dados in Graph.adj[i].items()]
        pesos_ordenados = sorted(aux, key=lambda x: x[1])
        ordenados.append(pesos_ordenados)

    return ordenados

def calcula_custo_caminho(graph, caminho):
    """
    Calcula o custo total de um caminho em um grafo ponderado.
    Args:
        graph: Um grafo ponderado (networkx.Graph).
        caminho: Uma lista representando o caminho, onde cada elemento é um vértice.
    Returns:
        O custo total do caminho.
    """
    custo_total = 0
    for i in range(len(caminho) - 1):
        u, v = caminho[i], caminho[i + 1]
        if graph.has_edge(u, v):
            custo_total += graph[u][v]['weight']
        else:
            raise ValueError(f"Aresta inexistente entre os vértices {u} e {v}.")
    return custo_total

def bound(graph, edgesOrdenados, path):
    """
    Calcula o limite inferior (bound) para o nó atual.
    A estimativa considera a soma das duas menores arestas incidentes em cada vértice / 2.
    """
    n = graph.number_of_nodes()
    # Custo acumulado do caminho atual
    cost = sum(graph[path[i]][path[i + 1]]['weight'] for i in range(len(path) - 1))

    # Estimar custo mínimo para visitar os nós restantes
    unvisited = set(range(n)) - set(path)
    if not unvisited:
        return cost

    bound_estimate = 0
    for node in unvisited:
        # Considera apenas arestas incidentes que levam a outros vértices não visitados
        unvisited_edges = [weight for neighbor, weight in edgesOrdenados[node] if neighbor in unvisited or neighbor == path[0]]
        if len(unvisited_edges) >= 2:
            bound_estimate += unvisited_edges[0] + unvisited_edges[1]
        elif len(unvisited_edges) == 1:
            bound_estimate += unvisited_edges[0]

    return math.ceil(cost + bound_estimate / 2)

def BaB_TSP(graph):
    """
    Resolve o problema do caixeiro viajante (TSP) usando Branch-and-Bound.

    Args:
        graph: Um grafo ponderado (networkx.Graph) representando o problema.

    Returns:
        Uma tupla (melhor_caminho, melhor_custo).
    """
    n = graph.number_of_nodes()
    # Pré-calcula as arestas ordenadas
    ordenados = ordenaEdgesPesos(graph)

    # Nó raiz (bound, nível, custo, caminho)
    root = (bound(graph, ordenados, [0]), 0, 0, [0])
    queue = []
    heapq.heappush(queue, root)  # Adiciona o nó raiz na fila
    # Caminho inicial qualquer
    best_path = []
    for i in range(n):
        best_path.append(i)
    best_path.append(0)
    best_cost = calcula_custo_caminho(graph, best_path)

    while queue:
        current_bound, level, current_cost, path = heapq.heappop(queue)

        # Se o nível atingir n-1
        if level == n - 1:
            total_cost = current_cost + graph[path[-1]][0]['weight']
            if total_cost < best_cost:
                best_cost = total_cost
                best_path = path + [0]

        # Expandir nós filhos se o limite for promissor
        elif current_bound < best_cost:
            for neighbor in graph[path[-1]]:
                if neighbor not in path:
                    new_path = path + [neighbor]
                    new_cost = current_cost + graph[path[-1]][neighbor]['weight']
                    new_bound = bound(graph, ordenados, new_path)

                    if new_bound < best_cost:
                        heapq.heappush(queue, (new_bound, level + 1, new_cost, new_path))

    return best_path, best_cost