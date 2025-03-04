from time import time
import networkx as nx
import matplotlib.pyplot as plt
from collections import namedtuple
import logging, pickle, json

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)

EDGE_DENSITIES = [0.125, 0.25, 0.5, 0.75]

SEED = 103645

SIZES = 256

Result = namedtuple('Result', ['function', 'result', 'operations', 'time', 'solutions'])

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