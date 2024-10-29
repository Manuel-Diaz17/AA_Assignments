from time import time
import networkx as nx
import matplotlib.pyplot as plt

def generate_random_graph(seed, size):
    return nx.fast_gnp_random_graph(size, 0.8, seed=seed)