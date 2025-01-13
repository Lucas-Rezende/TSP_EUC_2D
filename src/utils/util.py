import networkx as nx # type: ignore 
import argparse
import math

# Gerais

def tsp_input(data):
    """Interpreta entradas .tsp da TSPLIB"""
    nodes = {}
    reading_coords = False
    for line in data.splitlines():
        line = line.strip()
        if line.startswith("NODE_COORD_SECTION"):
            reading_coords = True
            continue
        if line == "EOF":
            break
        if reading_coords:
            parts = line.split()
            node_id = int(parts[0]) - 1
            x, y = float(parts[1]), float(parts[2])
            nodes[node_id] = (x, y)
    return nodes

def euclidean_distance(coord1, coord2):
    """Calcula a distância euclidiana entre dois pontos/vértices"""
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

def buildGraph(nodes):
    """Cria o grafo com NetworkX para a instância."""
    G = nx.Graph()
    for node, coords in nodes.items():
        G.add_node(node, pos=coords)
    for i in nodes:
        for j in nodes:
            if i != j:
                dist = euclidean_distance(nodes[i], nodes[j])
                G.add_edge(i, j, weight=dist)
    return G

def arguments_tsp():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('algorithm', choices=['TAT', 'C', 'BNB'])
    parser.add_argument('file_path', type=str)
    return parser.parse_args()

def starter():
    args = arguments_tsp()

    with open(args.file_path, 'r') as file:
        data = file.read()

    nodes = tsp_input(data)
    G = buildGraph(nodes)
    c = nx.get_edge_attributes(G, 'weight')
    
    return G, c, args.algorithm

# Códigos usados nos algoritmos aproximativos:

def MST(Graph):
    """Calcula a árvore geradora mínima com auxílio do algoritmo de Prim. Como as instâncias da tsplib são densas (i.e muitas arestas comparadas ao número de vértices), o algoritmo de Prim geralmente é recomendado."""
    return nx.minimum_spanning_tree(Graph, algorithm="prim")

def VertexListPreOrder(MST_T, root):
    """Usado para gerar a Lista de vértices (H) ordenados de acordo com o momento em que são visitados pela primeira vez em um passeio preorder na árvore T, no caso a MST gerada previamente
    Esse passeio começa num vértice arbitrário, porém como serão feitos testes com o retorno desse método, a raíz será fixada para evitar que os caminhos hamiltonianos para o mesmo problema tsp sejam diferentes eventualmente, mesmo que estejam dentro do intervalo de aproximação.
    """
    return list(nx.dfs_preorder_nodes(MST_T, source=list(MST_T.nodes)[0]))

def get_odd_degress(degrees):
    I = []
    for node, degree in degrees.items():
        if degree % 2 != 0:
            I.append(node)
    return I

def eulerian_circuit(Graph):
    """Calcula o circuito euleriano de um grafo"""
    for edge in nx.eulerian_circuit(Graph):
        yield edge

def shortcutting(eulerian_circuit, max_node):
    """Cria um circuito hamiltoniano a partir de um circuito euleriano da seguinte maneira: Elimina vértices duplicados, substituindo subcaminhos u-w-v por arestas u-v. Ideia: Make the circuit found in previous step into a Hamiltonian circuit by skipping repeated vertices (shortcutting)."""
    
    visited = [False] * (max_node + 1)
    hamiltonian_circuit = []

    # Visita os vértices se e somente se não foram visitados previamente
    for u, v in eulerian_circuit:
        if not visited[u]:
            visited[u] = True
            hamiltonian_circuit.append(u)
        if not visited[v]:
            visited[v] = True
            hamiltonian_circuit.append(v)

    if hamiltonian_circuit[0] != hamiltonian_circuit[-1]:
        hamiltonian_circuit.append(hamiltonian_circuit[0])

    if len(hamiltonian_circuit) - 1 == max_node and len(set(hamiltonian_circuit[:-1])) == max_node:
        return hamiltonian_circuit
    else:
        return None
    
def remove_second_occurrences(H):
    """Remove repetições de vértices de H e adiciona o inicial no final para formar um circuito Hamiltoniano."""
    seen = set()
    circuit = []
    for vertex in H:
        if vertex not in seen:
            circuit.append(vertex)
            seen.add(vertex)

    circuit.append(circuit[0])
    return circuit
    
def cost_calculator(H, c):
    """Calcula o custo total para twice around the tree"""
    cost = 0
    for i in range(len(H)):
        u = H[i]
        v = H[(i + 1) % len(H)]
        
        if (u, v) in c:
            cost += c[(u, v)]
        elif (v, u) in c:
            cost += c[(v, u)]
            
    return cost

def cost_calculator_christophies(G, H):
    """Calcula o custo total para christophies"""
    cost = 0
    i = 0
    while i < len(H) - 1:
        cost += G[H[i]][H[i + 1]]['weight']
        i += 1
    return cost