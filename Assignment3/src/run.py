import json
import os
from collections import OrderedDict
from math import floor

from tqdm import tqdm
from algorithms import count_exactly, approximate_counter, lossy_frequency_counter
from utils import log, Stats, CounterResult

FILE_PATH = "../books/processed_books"
RESULTS_FILE = "../results/results.json"

# Retrieve all books from the specified directory
books = [book for book in os.listdir(FILE_PATH) if book.endswith(".txt")]
algorithms = [count_exactly, approximate_counter, lossy_frequency_counter]

def sort_result(result, time):
    # Sort results by frequency and return top-n results for specific values of n
    sorted_result = sorted(result.items(), key=lambda x: x[1], reverse=True)
    n_values = [5, 10, 15, 20]  # Define the top-n values
    sorted_results = {n: {"result": OrderedDict(sorted_result[:n]), "time": time} for n in n_values}
    sorted_results[0] = {"result": OrderedDict(sorted_result), "time": time}  # Full result
    return sorted_results

def run_exact_counter(text):
    # Run the exact counter and sort results
    result, time = count_exactly(text)
    return sort_result(result, time)

def run_approximate_counter(text, runs=500):
    # Run the approximate counter multiple times and compute average results
    results = []
    average_result = {}
    average_time = 0

    for _ in tqdm(range(runs)):
        result, time = approximate_counter(text)
        results.append(result)
        average_time += time

    for word in results[0]:
        average_result[word] = floor(sum(result[word] for result in results) / len(results))

    return sort_result(average_result, average_time / runs)

def run_lossy_counting(text):
    # Run the lossy counting algorithm for specified n values
    top_n_values = [5, 10, 15, 20]
    lossy_results = {}
    for n in top_n_values:
        log.info(f"Running lossy counting with n={n}")
        result, time = lossy_frequency_counter(text, n)
        sorted_result = sorted(result.items(), key=lambda x: x[1], reverse=True)
        lossy_results[n] = {"result": OrderedDict(sorted_result), "time": time}

    return lossy_results

def marathon():
    # Run all algorithms on all books and save results
    results = {}
    for book in books:
        results[book] = {}
        with open(os.path.join(FILE_PATH, book), "r") as f:
            book_text = f.read()
            log.info(f"Running exact counter on {book}")
            results[book]["exact_counter"] = run_exact_counter(book_text)
            log.info(f"Running approximate counter on {book}")
            results[book]["approximate_counter"] = run_approximate_counter(book_text)
            log.info(f"Running lossy counting on {book}")
            results[book]["lossy_counting"] = run_lossy_counting(book_text)

    # Save all results to a JSON file
    json.dump(results, open(RESULTS_FILE, "w"), indent=4, ensure_ascii=False)

def run_stats_lossy(results):
    # Compute and save statistics for lossy counting
    for book in books:
        for n in ["5", "10", "15", "20"]:
            exact_result = CounterResult(
                results[book]["exact_counter"]["0"]["result"],
                results[book]["exact_counter"]["0"]["time"]
            )
            lossy_result = CounterResult(
                results[book]["lossy_counting"][n]["result"],
                results[book]["lossy_counting"][n]["time"]
            )
            stats = Stats(exact_result, lossy_result)
            stats.save_results(f"../results/statistics/statistics_{book}_lossy_counting_{n}.json", _type="json")


def run_stats_probability(results):
    # Compute and save statistics for approximate counters
    for book in books:
        exact_result = CounterResult(
            results[book]["exact_counter"]["0"]["result"],
            results[book]["exact_counter"]["0"]["time"]
        )
        approx_result = CounterResult(
            results[book]["approximate_counter"]["0"]["result"],
            results[book]["approximate_counter"]["0"]["time"]
        )
        stats = Stats(exact_result, approx_result)
        stats.save_results(f"../results/statistics/statistics_{book}_approximate_counter.json", _type="json")


if __name__ == "__main__":
    # Ensure results directory exists
    if not os.path.exists("../results"):
        os.mkdir("../results")

    # If results file doesn't exist, run all algorithms
    if not os.path.exists(RESULTS_FILE):
        marathon()

    # Load results and compute statistics
    results = json.load(open(RESULTS_FILE, "r"))
    run_stats_lossy(results)
    run_stats_probability(results)