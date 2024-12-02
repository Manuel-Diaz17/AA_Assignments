from collections import defaultdict
import pickle
from algorithms import find_minimum_vertex_cover, greedy_vertex_cover
from utils import EDGE_DENSITIES, SEED, log


graphs = pickle.load(open(f"../results/all_graphs.pickle", "rb"))

def run(algorithm, name):
    results = defaultdict(dict)
    
    for max_edges in EDGE_DENSITIES:
        for size in range(4, 29): # 29 for exhaustive algorithm and 256 for greedy
            log.info(f"Running {name} algorithm for graph with size {size}, seed {SEED} and {max_edges} of the maximum number of edges.")
            results[max_edges][size] = algorithm(graphs[max_edges][size])
            log.info(f"Finished running {name} algorithm for graph with size {size}, seed {SEED} and {max_edges} of the maximum number of edges.")
        
    pickle.dump(results, open(f"../results/results_complete_{name}.pickle", "wb"))


if __name__ == "__main__":
    run(find_minimum_vertex_cover, "bruteforce")
    #run(greedy_vertex_cover, "greedy")