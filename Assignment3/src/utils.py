from time import time
import logging, pickle, json
from dataclasses import dataclass
from functools import wraps
from math import sqrt

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)

def count_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        end = time()
        return result, end - start

    return wrapper

def calculate_total_and_unique_words(text):
    words = text.split()
    unique_words = set(words)
    return len(words), unique_words


@dataclass
class CounterResult:
    result: dict[str, int]
    time: float

    def __str__(self):
        return f'Time: {self.time}, Result: {self.result}'


class Stats:
    def __init__(self, exact_result: CounterResult, approx_result: CounterResult):
        # Initialize with exact and approximate word counts
        self.exact_counts = exact_result.result
        self.approx_counts = approx_result.result
        self.words = set(self.exact_counts.keys()).union(set(self.approx_counts.keys()))

    def mean_absolute_error(self):
        # Calculate the mean absolute error between exact and approximate counts
        total_error = sum(
            abs(self.exact_counts.get(word, 0) - self.approx_counts.get(word, 0)) for word in self.words
        )
        return total_error / len(self.words)

    def mean_relative_error(self):
        # Calculate the mean relative error
        total_relative_error = sum(
            abs(self.exact_counts.get(word, 0) - self.approx_counts.get(word, 0)) / self.exact_counts.get(word, 1)
            for word in self.words if self.exact_counts.get(word, 0) != 0
        )
        return total_relative_error / len(self.words)

    def mean_accuracy_ratio(self):
        # Calculate the mean accuracy ratio
        total_accuracy_ratio = sum(
            self.approx_counts.get(word, 0) / self.exact_counts.get(word, 1) for word in self.words
            if self.exact_counts.get(word, 0) != 0
        )
        return total_accuracy_ratio / len(self.words)

    def smallest_value(self):
        # Get the smallest word count in approximate results
        return min(self.approx_counts.values())

    def largest_value(self):
        # Get the largest word count in approximate results
        return max(self.approx_counts.values())

    def mean(self):
        # Calculate the mean of approximate counts
        return sum(self.approx_counts.values()) / len(self.approx_counts)

    def mean_absolute_deviation(self):
        # Calculate the mean absolute deviation
        mean = self.mean()
        total_deviation = sum(abs(count - mean) for count in self.approx_counts.values())
        return total_deviation / len(self.approx_counts)

    def standard_deviation(self):
        # Calculate the standard deviation
        mean = self.mean()
        total_squared_deviation = sum((count - mean) ** 2 for count in self.approx_counts.values())
        return sqrt(total_squared_deviation / len(self.approx_counts))

    def maximum_deviation(self):
        # Calculate the maximum deviation
        mean = self.mean()
        return max(abs(count - mean) for count in self.approx_counts.values())

    def variance(self):
        # Calculate the variance
        mean = self.mean()
        total_squared_deviation = sum((count - mean) ** 2 for count in self.approx_counts.values())
        return total_squared_deviation / len(self.approx_counts)

    def __save_pickle(self, filename, results):
        # Save results in pickle format
        with open(filename, 'wb') as file:
            pickle.dump(results, file)

    def __save_json(self, filename, results):
        # Save results in JSON format
        with open(filename, 'w') as file:
            json.dump(results, file, indent=4, ensure_ascii=False)

    def save_results(self, filename, _type='pickle'):
        # Prepare results and save to file in specified format
        results = {
            'mean_absolute_error': self.mean_absolute_error(),
            'mean_relative_error': self.mean_relative_error(),
            'mean_accuracy_ratio': self.mean_accuracy_ratio(),
            'smallest_value': self.smallest_value(),
            'largest_value': self.largest_value(),
            'mean': self.mean(),
            'mean_absolute_deviation': self.mean_absolute_deviation(),
            'standard_deviation': self.standard_deviation(),
            'maximum_deviation': self.maximum_deviation(),
            'variance': self.variance(),
        }

        if _type == 'pickle':
            self.__save_pickle(filename, results)
        if _type == 'json':
            self.__save_json(filename, results)
        else:
                raise ValueError(f'Invalid file type: {_type}')