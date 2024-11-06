from matplotlib import pyplot as plt
from utils import MAXIMUM_NUMBER_EDGES, import_data


def plot_y_number_operations_x_number_of_vertices(results, name, log=False, save=False, show=False):
    for max_edges in MAXIMUM_NUMBER_EDGES:
        x = []
        y = []
        for size in range(1, 50):
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
        plt.savefig(f"charts/{name}_number_operations_vs_number_of_vertices.png")
    if show:
        plt.show()


def plot_y_time_x_number_of_vertices(results, name, log=False, save=False, show=False):
    for max_edges in MAXIMUM_NUMBER_EDGES:
        x = []
        y = []
        for size in range(1, 50):
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
        plt.savefig(f"charts/{name}_time_vs_number_of_vertices.png")
    if show:
        plt.show() 


def plot_y_number_of_solutions_tested_x_number_of_vertices(results, name, log=False, save=False, show=False):
    for max_edges in MAXIMUM_NUMBER_EDGES:
        x = []
        y = []
        for size in range(4, 50):
            x.append(size)
            y.append(results[max_edges][size].solution_counter)
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


def main():
    
    bruteforce_results = import_data("../results/results_complete_find_bruteforce.pickle")
    greedy_results = import_data("../results/results_complete_greedy.pickle")

    # plot_y_number_operations_x_number_of_vertices(bruteforce_results, "bruteforce", log=True, show=True)
    # plot_y_time_x_number_of_vertices(bruteforce_results, "bruteforce", log=True, show=True)
    # plot_y_number_of_solutions_tested_x_number_of_vertices(bruteforce_data, "bruteforce", log=True, save=True)

    # plot_y_number_operations_x_number_of_vertices(greedy_results, "greedy", log=True, show=True)
    # plot_y_time_x_number_of_vertices(greedy_results, "greedy", log=True, show=True)
    # plot_y_number_of_solutions_tested_x_number_of_vertices(greedy_results, "greedy", log=True, save=True)

    

if __name__ == "__main__":
    main()