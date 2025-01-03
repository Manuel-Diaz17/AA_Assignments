import json
import os
from collections import defaultdict

from utils import calculate_total_and_unique_words

FILE_PATH = "../books/processed_books"
books = [book for book in os.listdir(FILE_PATH) if book.endswith(".txt")]

def calculate_total_and_unique_words_main():
    # Calculate total and unique words for each book
    results = {}
    for book in books:
        with open(os.path.join(FILE_PATH, book), "r") as f:
            book_text = f.read()
            total_words, unique_words = calculate_total_and_unique_words(book_text)
            results[book] = {
                "total_words": total_words,
                "total_unique_words": len(unique_words),
                "unique_words": list(unique_words)
            }

    # Save results to a JSON file
    with open("../results/word_counts.json", "w") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)


def calculate_times_main():
    # Save in a JSON file the time it takes to run each algorithm for each book
    results = {}
    with open("../results/results.json", "r") as f:
        results = json.load(f)
        new_results = defaultdict(dict)
        for book in results:
            for algorithm in results[book]:
                if algorithm == "lossy_counting":
                    new_results[f"{book}"][algorithm] = defaultdict(dict)
                    for n in ["5", "10", "15", "20"]:
                        new_results[f"{book}"][algorithm][f"{n}"] = results[book]["lossy_counting"][n]["time"]
                else:
                    new_results[f"{book}"][algorithm] = results[book][algorithm]["0"]["time"]

    # Save times to a JSON file
    json.dump(new_results, open("../results/times.json", "w"), indent=4, ensure_ascii=False)


def main():
    # Generate a list of the top 10 most frequent words for each book of each algorithm
    with open("../results/results.json", "r") as f:
        results = json.load(f)
        new_results = defaultdict(dict)

        for book in results:
            for algorithm in results[book]:
                if algorithm == "lossy_counting":
                    new_results[f"{book}"][algorithm] = defaultdict(dict)
                    for n in ["5", "10", "15", "20"]:
                        new_results[f"{book}"][algorithm][f"{n}"] = list(results[book]["lossy_counting"][n]["result"].keys())
                else:
                    new_results[f"{book}"][algorithm] = list(results[book][algorithm]["10"]["result"].keys())

    # Save the top words to a JSON file
    json.dump(new_results, open("../results/top_words.json", "w"), indent=4, ensure_ascii=False)


if __name__ == '__main__':
    # Uncomment the function you want to run
    calculate_total_and_unique_words_main()
    calculate_times_main()
    main()