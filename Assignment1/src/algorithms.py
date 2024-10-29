from itertools import combinations

def is_vertex_cover(graph, vertex_set):
    for u, v in graph.edges():
        if u not in vertex_set and v not in vertex_set:
            return False
    return True

def find_minimum_vertex_cover(graph):
    """
    Finds minimum vertex coverage using exhaustive search
    """
    vertices = list(graph.nodes())
    n = len(vertices)

    for r in range(1, n + 1):
        for subset in combinations(vertices, r):
            if is_vertex_cover(graph, subset):
                return set(subset)
            
def greedy_vertex_cover(graph):
    """
    Finds an approximate solution for the vertex cover using a greedy heuristic.
    """
    # Initialize the vertex cover as an empty set
    cover = set()

    # As long as there are edges in the graph
    while graph.number_of_edges() > 0:
        # Select the vertex with the highest degree
        v = max(graph.degree, key=lambda x: x[1])[0]

        # Add the vertex to the cover and remove it from the graph
        cover.add(v)
        graph.remove_node(v)
    
    return cover