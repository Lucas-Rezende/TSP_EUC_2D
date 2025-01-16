import sys
from christofides import *
from twice_around_the_tree import *
from BaB_TSP import *

def main():
    G, c, arg = util.starter()

    if arg == "TAT":
        cost, time = approx_twice_around_the_tree_tour(G, c)
    elif arg == "C":
        cost, time = approx_christofides_tour(G)
    elif arg == "BNB":
        path, cost = BaB_TSP(G)
        return

    with open('results.txt', 'a') as f:
        f.write(f"{sys.argv[2]} | Custo: {cost} | Tempo: {time}s\n")

if __name__ == "__main__":
    main()
