from utils import util
import random
from timeout_decorator import timeout # type: ignore
import time
import tracemalloc

"""
APPROX-TSP-TOUR (G, c)
    Step 1) select a vertex r ∈ G.V to be a "root" vertex
    Step 2) compute a minimum spanning tree T for G from root r using MST-PRIM(G, c, r)
    Step 3) let H be a list of vertices, ordered according to when they are first visited in a preorder tree walk of T
    Step 4) return the hamiltonian cycle H
"""

@timeout(1800)
def approx_twice_around_the_tree_tour(G, c):
    start = time.time()
    tracemalloc.start()
    
    """Aproximação do problema do Caixeiro Viajante usando Twice Around The Tree."""
    root = random.choice(list(G.nodes))  # Step 1)
    MST_T = util.MST(G)  # Step 2)
    H = util.VertexListPreOrder(MST_T, root)  # Step 3)
    
    hamiltonian_circuit = util.remove_second_occurrences(H)
    cost = util.cost_calculator(hamiltonian_circuit, c)
    
    # Captura o uso de memória
    peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()  # Para o monitoramento de memória

    end = time.time()
    total_time = end - start
    
    return cost, total_time, peak_memory