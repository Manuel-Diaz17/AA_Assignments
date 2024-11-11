from itertools import combinations
from utils import count_time

def is_vertex_cover(graph, vertex_set):
    operation_count = 0 # Initialize operation counter
    for u, v in graph.edges():
        operation_count += 1
        if u not in vertex_set and v not in vertex_set:
            operation_count += 1
            return False, operation_count # Return early if not a vertex cover
    return True, operation_count # All edges are covered


@count_time
def find_minimum_vertex_cover(graph):
    """
    Finds minimum vertex coverage using exhaustive search.
    """
    vertices = list(graph.nodes())
    n = len(vertices)

    operation_count = 0 # Initialize operation counter
    solution_count = 0 # Initialize solution counter

    # Iterate over all possible subsets of vertices
    for r in range(1, n + 1):
        for subset in combinations(vertices, r):
            operation_count += 1 # Increment operation counter for each combination
            is_cover, op_count = is_vertex_cover(graph, subset)
            operation_count += op_count
            if is_cover:
                solution_count += 1  # Increment solution counter for each valid cover
                operation_count += 1 # Increment operation counter for each check
                vertices_set = set(subset)

    return vertices_set, operation_count, solution_count # Return all counts


@count_time
def greedy_vertex_cover(graph):
    """
    Finds an approximate solution for the vertex cover using a greedy heuristic.
    """
    # Initialize the vertex cover as an empty set
    cover = set()

    operation_count = 0  # Initialize operation counter
    solutions_count = 0 # Initialize solutions tested counter 

    # As long as there are edges in the graph
    while graph.number_of_edges() > 0:
        solutions_count += 1 # Increase the solutions tested count

        # Select the vertex with the highest degree
        v = max(graph.degree, key=lambda x: x[1])[0]
        operation_count += graph.degree[v] # Increment operation count by the degree of the chosen node

        # Add the vertex to the cover and remove it and all its edges from the graph
        cover.add(v)
        graph.remove_node(v)

    return cover, operation_count, solutions_count