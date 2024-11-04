from itertools import combinations
from utils import count_time

def is_vertex_cover(graph, vertex_set):
    for u, v in graph.edges():
        if u not in vertex_set and v not in vertex_set:
            return False
    return True

@count_time
def find_minimum_vertex_cover(graph):
    """
    Finds minimum vertex coverage using exhaustive search
    """
    vertices = list(graph.nodes())
    n = len(vertices)

    operation_count = 0 # Initialize operation counter

    # Iterate over all possible subsets of vertices
    for r in range(1, n + 1):
        for subset in combinations(vertices, r):
            operation_count += 1
            if is_vertex_cover(graph, subset):
                operation_count += 1
                vertices_set = set(subset)

    return vertices_set, operation_count

@count_time
def greedy_vertex_cover(graph):
    """
    Finds an approximate solution for the vertex cover using a greedy heuristic.
    """
    # Initialize the vertex cover as an empty set
    cover = set()

    operation_count = 0 # Initialize operation counter

    # As long as there are edges in the graph
    while graph.number_of_edges() > 0:
        operation_count += 1
        # Select the vertex with the highest degree
        v = max(graph.degree, key=lambda x: x[1])[0]
        operation_count += 1

        # Add the vertex to the cover and remove it from the graph
        cover.add(v)
        graph.remove_node(v)
        operation_count += 2 # Increment operation counter for each additional and removal
    
    return cover, operation_count