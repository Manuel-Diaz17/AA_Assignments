import json
from collections import defaultdict

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from math import ceil

def plot_count_per_algorithm(results, title, n=5, show=False, save=False):
    n = str(n)  # Convert n to string for indexing results
    books = results.keys()
    num_books = len(books)
    algorithms = ["exact_counter", "approximate_counter", "lossy_counting"]

    num_cols = 3  # Number of columns in the grid
    num_rows = ceil(num_books / num_cols)  # Calculate rows based on number of books

    fig, axs = plt.subplots(num_rows, num_cols, figsize=(10 * num_cols, 5 * num_rows), constrained_layout=True)
    axs = axs.flatten()

    for i, book in enumerate(books):
        # Get the most frequent words from the exact counter
        words = results[book]["exact_counter"][n]["result"].keys()
        values = {
            algorithm: [results[book][algorithm][n]["result"].get(word, 0) for word in words]
            for algorithm in algorithms
        }

        x = np.arange(len(words))  # Positions for bars
        width = 0.25  # Width of each bar
        multiplier = 0  # Offset multiplier for side-by-side bars

        for attribute, measurement in values.items():
            axs[i].bar(x + multiplier * width, measurement, width, label=attribute)
            multiplier += 1

        axs[i].set_ylabel('Counts')
        axs[i].set_xlabel('Most frequent words')
        axs[i].set_title(book)
        axs[i].set_xticks(x + width / 2)
        axs[i].set_xticklabels(words, rotation=45, ha='right')  # Rotate labels for better visibility
        axs[i].legend(loc='upper right')

    # Remove unused subplots if the grid is larger than the number of books
    for i in range(num_books, num_rows * num_cols):
        fig.delaxes(axs[i])

    fig.suptitle(title, fontsize=16)

    if show:
        plt.show()

    if save:
        plt.savefig(f'../plots/{title}.png')

def main():
    results = json.load(open("../results/results.json", "r"))

    for n in [5, 10, 15, 20]:
        plot_count_per_algorithm(results, f"Most frequent words with n={n}", n=n, save=True)


if __name__ == "__main__":
    main()