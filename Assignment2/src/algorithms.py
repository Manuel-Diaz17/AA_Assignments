from itertools import combinations
import random
from math import ceil

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

@count_time
def randomized_vertex_cover(graph, iterations=1000):
    """
    Randomized algorithm for finding an approximate Minimum Vertex Cover, starting with greater subsets.
    """
    best_cover = None
    operations_count = 0
    solution_counter = 0
    total_vertices = len(graph.nodes())
    checked_subsets = set()  # Tracks evaluated subsets

    for i in range(iterations):
        # Dynamically decrease the size of subsets over iterations
        subset_size = max(1, ceil(total_vertices * (1 - i / iterations)))
        random_subset = random.sample(graph.nodes(), subset_size)
        operations_count += 1

        # Avoid re-evaluating subsets already tested
        subset_key = frozenset(random_subset)
        if subset_key not in checked_subsets:
            solution_counter += 1
            checked_subsets.add(subset_key)
            operations_count += 1

            # Check if the subset is a valid vertex cover
            is_cover, additional_ops = is_vertex_cover(graph, random_subset)
            operations_count += additional_ops

            # Update the best solution found so far
            if is_cover and (best_cover is None or len(random_subset) < len(best_cover)):
                best_cover = set(random_subset)
                operations_count += 1

    return best_cover, operations_count, solution_counter


@count_time
def randomized_vertex_cover_min(graph, iterations=1000):
    """
    Randomized algorithm for finding an approximate Minimum Vertex Cover, starting with smaller subsets.
    """
    best_cover = None
    operations_count = 0
    solution_counter = 0
    total_vertices = len(graph.nodes())
    checked_subsets = set()  # Tracks evaluated subsets

    for i in range(iterations):
        # Dynamically increase the size of subsets over iterations
        subset_size = min(total_vertices, ceil((i + 1) / iterations * total_vertices))
        random_subset = random.sample(graph.nodes(), subset_size)
        operations_count += 1

        # Avoid re-evaluating subsets already tested
        subset_key = frozenset(random_subset)
        if subset_key not in checked_subsets:
            solution_counter += 1
            checked_subsets.add(subset_key)
            operations_count += 1

            # Check if the subset is a valid vertex cover
            is_cover, additional_ops = is_vertex_cover(graph, random_subset)
            operations_count += additional_ops

            # Update the best solution found so far
            if is_cover and (best_cover is None or len(random_subset) < len(best_cover)):
                best_cover = set(random_subset)
                operations_count += 1

    return best_cover, operations_count, solution_counter
