from time import time
import networkx as nx
import matplotlib.pyplot as plt
from collections import namedtuple
import logging, pickle, json
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)

EDGE_DENSITIES = [0.125, 0.25, 0.5, 0.75]

ITERATIONS = [100, 500, 1000, 5000, 10000]

SEED = 103645

SIZES = 256

Result = namedtuple('Result', ['function', 'result', 'operations', 'time', 'solutions'])
HitMiss = namedtuple('HitMiss', ['hit', 'miss', 'ratio'])

def generate_random_graph(seed, size=10, maximum_number_edges=0.8):
    return nx.fast_gnp_random_graph(size, maximum_number_edges, seed=seed)


def generate_all_graphs():
    all_graphs = {}
    for maximum_number_edges in EDGE_DENSITIES:
        all_graphs[maximum_number_edges] = {}
        for size in range(1, SIZES):
            G = generate_random_graph(SEED, size, maximum_number_edges)
            all_graphs[maximum_number_edges][size] = G
    return all_graphs


def save_graphs():
    graphs = generate_all_graphs()
    pickle.dump(graphs, open(f"../results/all_graphs.pickle", "wb"))


def count_time(func):
    def wrapper(*args, **kwargs):
        start = time()
        result, operations, solutions = func(*args, **kwargs)
        end = time()

        return Result(func.__name__, result, operations, end - start, solutions)
    
    return wrapper


def import_data(file):
    return pickle.load(open(f"{file}", "rb"))


def convert_to_json(data, path):
    new_data = {}
    for size in data.keys():
        new_data[size] = {}
        for max_edges in data[size].keys():
            new_data[size][max_edges] = {}
            new_data[size][max_edges]["operations"] = data[size][max_edges].operations
            new_data[size][max_edges]["time"] = data[size][max_edges].time
            new_data[size][max_edges]["result"] = list(data[size][max_edges].result)
            new_data[size][max_edges]["solutions"] = data[size][max_edges].solutions

    json.dump(new_data, open(path, "w"), indent=4)


def convert_all_pickle_to_json():
    files = [f for f in os.listdir("../results/randomized_vertex_cover") if f.startswith("results_") and f.endswith(".pickle")]
    for file in files:
        print(f"Converting {file} to json")
        data = import_data(f"../results/randomized_vertex_cover/{file}")
        convert_to_json(data, f"../results/randomized_vertex_cover/json/{file.replace('.pickle', '.json')}")


def read_graph_from_txt(filename):
    G = nx.Graph()

    with open(filename, 'r') as file:
        lines = file.readlines()

        # Skip the first three lines (headers/metadata)
        for line in lines[:4]:
            u, v = map(int, line.strip().split()[:2])
            G.add_edge(u, v)

    return G


def compare_solutions_with_optimal_solution(results, bruteforce_results):
    hit = 0
    miss = 0

    for max_edges in EDGE_DENSITIES:
        for size in range(4, 29):
            if results[max_edges][size].result == bruteforce_results[max_edges][size].result:
                hit += 1
            else:
                miss += 1

    return hit, miss, hit / (hit + miss)


if __name__ == "__main__":
    files = [f for f in os.listdir("../results/randomized_vertex_cover") if f.startswith("results_") and f.endswith(".pickle")]
    # # Load all the files
    results = [import_data(f"../results/randomized_vertex_cover/{file}") for file in files]
    # # Load all the graphs
    # graphs = pickle.load(open("../graphs/all_graphs.pickle", "rb"))
    # # Load the brute force results
    brute_force_results = import_data("../results/bruteforce/results_complete_bruteforce.pickle")
    # # Compare the solutions

    hitMiss = {}
    for result, file in zip(results, files):
        hit, miss, ratio = compare_solutions_with_optimal_solution(result, brute_force_results)
        hitMiss[file] = HitMiss(hit, miss, ratio)

    json.dump(hitMiss, open("../results/comparisons_with_optimal_solution/hit_miss_randomized_vertex_cover.json", "w"), indent=4)