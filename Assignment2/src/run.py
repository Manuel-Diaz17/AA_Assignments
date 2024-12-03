from collections import defaultdict
import pickle
from algorithms import find_minimum_vertex_cover, greedy_vertex_cover, randomized_vertex_cover, randomized_vertex_cover_min
from utils import EDGE_DENSITIES, ITERATIONS, SEED, log


graphs = pickle.load(open(f"../graphs/all_graphs.pickle", "rb"))

def run(algorithm, name):
    results = defaultdict(dict)
    
    for max_edges in EDGE_DENSITIES:
        for size in range(4, 29): # 29 for exhaustive algorithm and 256 for greedy
            log.info(f"Running {name} algorithm for graph with size {size}, seed {SEED} and {max_edges} of the maximum number of edges.")
            results[max_edges][size] = algorithm(graphs[max_edges][size])
            log.info(f"Finished running {name} algorithm for graph with size {size}, seed {SEED} and {max_edges} of the maximum number of edges.")
        
    pickle.dump(results, open(f"../results/results_complete_{name}.pickle", "wb"))


def run_other_graphs(algorithm, name, graph):
    log.info(f"Running {name} algorithm for graph with size {graph.number_of_nodes()}, maximum number of edges {graph.number_of_edges()}")
    result = algorithm(graph)
    log.info(f"Finished running {name} algorithm for graph with size {graph.number_of_nodes()}, seed {SEED} and maximum number of edges {graph.number_of_edges()}")

    pickle.dump(result, open(f"../results/results_{name}.pickle", "wb"))


def run_all():
    for algorithm, name in [(randomized_vertex_cover_min, "randomized_vertex_cover_min")]:
        for max_iterations in ITERATIONS:
            results = defaultdict(dict)
            for max_edges in EDGE_DENSITIES:
                for size in range(4, 256):
                    log.info(f"Running randomized algorithm for graph with size {size}, seed {SEED} and maximum number of edges {max_edges}")
                    results[max_edges][size] = algorithm(graphs[max_edges][size], max_iterations)
                    log.info(f"Finished running randomized algorithm for graph with size {size}, seed {SEED} and maximum number of edges {max_edges}")

            pickle.dump(results, open(f"../results/{name}/results_{name}_{max_iterations}.pickle", "wb"))

if __name__ == "__main__":
    #run(greedy_vertex_cover, "greedy")
    run_all()