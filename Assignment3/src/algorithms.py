import random
from collections import defaultdict
from math import floor

from utils import count_time  # Changed the decorator name to something different


@count_time
def count_exactly(input_text):
    # Maps the exact frequency of each character
    frequency_map = defaultdict(int)

    for char in input_text:
        frequency_map[char] += 1

    return frequency_map


@count_time
def approximate_counter(input_text, sampling_rate=1 / 2):
    # Approximate counter using probabilistic sampling
    frequency_map = defaultdict(int)

    for char in input_text:
        if random.random() < sampling_rate:
            frequency_map[char] += 1

    # Scale the counts to estimate the actual frequencies
    scale_factor = int(1 / sampling_rate)
    for char in frequency_map:
        frequency_map[char] *= scale_factor

    return frequency_map


@count_time
def lossy_frequency_counter(input_text: str, segment_size: int = 10):
    # Lossy Counting Algorithm
    frequency_map = defaultdict(int)
    total_chars = 0
    current_threshold = 0

    for char in input_text:
        if char not in frequency_map:
            frequency_map[char] = current_threshold + 1
        else:
            frequency_map[char] += 1

        total_chars += 1
        new_threshold = floor(total_chars / segment_size)

        if new_threshold != current_threshold:
            current_threshold = new_threshold
            # Remove items with counts below the current threshold
            for key, value in list(frequency_map.items()):
                if value < current_threshold:
                    del frequency_map[key]

    return frequency_map
