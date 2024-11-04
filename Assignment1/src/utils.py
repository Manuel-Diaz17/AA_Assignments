from time import time
import networkx as nx
import matplotlib.pyplot as plt
from collections import namedtuple
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)

MAXIMUM_NUMBER_EDGES = [0.125, 0.25, 0.5, 0.75]

GRAPH_SIZES = [10,50,100,200,300,400,500,600,700,800,900,1000]

SEED = 103645

Result = namedtuple('Result', ['function','result','operations', 'time'])

def generate_random_graph(seed, size):
    return nx.fast_gnp_random_graph(size, 0.8, seed=seed)

def draw_graph(graph):
    nx.draw(graph, with_labels=True)
    plt.show()




def count_time(func):
    def wrapper(*args, **kwargs):
        start = time()
        result, operations = func(*args, **kwargs)
        end = time()

        return Result(func.__name__, result, operations, end - start)
    
    return wrapper