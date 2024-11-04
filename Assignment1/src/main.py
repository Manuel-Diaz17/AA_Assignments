from utils import generate_random_graph
from algorithms import find_minimum_vertex_cover, greedy_vertex_cover

SEED = 103645

def main():

    G = generate_random_graph(SEED, 10)

    algorithms = [find_minimum_vertex_cover, greedy_vertex_cover]

    for algorithm in algorithms:
        algorithm(G)



if __name__ == "__main__":
    main()