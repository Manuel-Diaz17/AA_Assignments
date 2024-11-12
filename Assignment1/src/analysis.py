from matplotlib import pyplot as plt
from utils import EDGE_DENSITIES, import_data

def plot_y_number_of_solutions_tested_x_number_of_vertices(results, name, log=False, save=False, show=False):
    for max_edges in EDGE_DENSITIES:
        x = []
        y = []
        for size in range(4, 29): # 29 for exhaustive algorithm and 256 for greedy
            x.append(size)
            y.append(results[max_edges][size].solutions)
        if log:
            plt.semilogy(x, y, label=f"edges ratio: {max_edges}")
        else:
            plt.plot(x, y, label=f"edges ratio: {max_edges}")
        plt.xlabel("Number of vertices")
        plt.ylabel("Number of solutions tested")
        plt.title(f"Number of solutions tested vs number of vertices for {name} algorithm")
        plt.legend()
    if save:
        plt.savefig(f"../charts/{name}_number_of_solutions_tested_vs_number_of_vertices.png")
    if show:
        plt.show()
    plt.close()


def plot_y_number_operations_x_number_of_vertices(results, name, log=False, save=False, show=False):
    for max_edges in EDGE_DENSITIES:
        x = []
        y = []
        for size in range(4, 29): # 29 for exhaustive algorithm and 256 for greedy
            x.append(size)
            y.append(results[max_edges][size].operations)
        if log:
            plt.semilogy(x, y, label=f"Maximum number of edges: {max_edges}")
        else:
            plt.plot(x, y, label=f"Maximum number of edges: {max_edges}")
        plt.xlabel("Number of vertices")
        plt.ylabel("Number of operations")
        plt.title(f"Number of operations vs number of vertices for {name} algorithm")
        plt.legend()
    if save:
        plt.savefig(f"../charts/{name}_number_operations_vs_number_of_vertices.png")
    if show:
        plt.show()
    plt.close()


def plot_y_time_x_number_of_vertices(results, name, log=False, save=False, show=False):
    for max_edges in EDGE_DENSITIES:
        x = []
        y = []
        for size in range(4, 29): # 29 for exhaustive algorithm and 256 for greedy
            x.append(size)
            y.append(results[max_edges][size].time)
        if log:
            plt.semilogy(x, y, label=f"Maximum number of edges: {max_edges}")
        else:
            plt.plot(x, y, label=f"Maximum number of edges: {max_edges}")
        plt.xlabel("Number of vertices")
        plt.ylabel("Time (s)")
        plt.title(f"Time vs number of vertices for {name} algorithm")
        plt.legend()
    if save:
        plt.savefig(f"../charts/{name}_time_vs_number_of_vertices.png")
    if show:
        plt.show()
    plt.close()


def main():
    
    bruteforce_results = import_data("../results/results_complete_bruteforce.pickle")
    #greedy_results = import_data("../results/results_complete_greedy.pickle")

    plot_y_number_of_solutions_tested_x_number_of_vertices(bruteforce_results, "bruteforce", log=True, save=True)
    plot_y_number_operations_x_number_of_vertices(bruteforce_results, "bruteforce", log=True, save=True)
    plot_y_time_x_number_of_vertices(bruteforce_results, "bruteforce", log=True, save=True)

    #plot_y_number_of_solutions_tested_x_number_of_vertices(greedy_results, "greedy", log=True, save=True)
    #plot_y_number_operations_x_number_of_vertices(greedy_results, "greedy", log=True, save=True)
    #plot_y_time_x_number_of_vertices(greedy_results, "greedy", log=True, save=True)
    

if __name__ == "__main__":
    main()