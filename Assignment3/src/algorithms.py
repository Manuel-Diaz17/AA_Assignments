import random
from collections import defaultdict
from math import floor

from utils import count_time  # Changed the decorator name to something different


@count_time
def count_exactly(input_text):
    # Maps the exact frequency of each word
    frequency_map = defaultdict(int)

    # Split the input text into words
    words = input_text.split()

    for word in words:
        frequency_map[word] += 1
                                                                                                                                                                                                                                                                                                                               
    return frequency_map


@count_time
def approximate_counter(input_text, sampling_rate = 1 / 2):
    # Approximate counter using probabilistic sampling
    frequency_map = defaultdict(int)

    # Split the input text into words
    words = input_text.split()

    for word in words:
        if random.random() < sampling_rate:
            frequency_map[word] += 1

    # Scale the counts to estimate the actual frequencies
    scale_factor = int(1 / sampling_rate)
    for word in frequency_map:
        frequency_map[word] *= scale_factor

    return frequency_map


@count_time
def lossy_frequency_counter(input_text: str, segment_size: int = 10):
    # Lossy Counting Algorithm for words
    frequency_map = defaultdict(int)
    total_words = 0
    current_threshold = 0

    # Split the input text into words
    words = input_text.split()

    for word in words:
        if word not in frequency_map:
            frequency_map[word] = current_threshold + 1
        else:
            frequency_map[word] += 1

        total_words += 1
        new_threshold = floor(total_words / segment_size)

        if new_threshold != current_threshold:
            current_threshold = new_threshold
            # Remove items with counts below the current threshold
            for key, value in list(frequency_map.items()):
                if value < current_threshold:
                    del frequency_map[key]

    return frequency_map