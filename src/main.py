import sys
from christofides import *
from twice_around_the_tree import *

def main():
    G, c, arg = util.starter()

    if arg == "TAT":
        cost = approx_twice_around_the_tree_tour(G, c)
    elif arg == "C":
        cost = approx_christofides_tour(G)
    elif arg == "BNB":
        print("Branch and Bound ainda não implementado.")
        return

    with open('results.txt', 'a') as f:
        f.write(f"{sys.argv[2]}: {cost}\n")

if __name__ == "__main__":
    main()