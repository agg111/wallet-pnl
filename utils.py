import random

def pick_random_timestamps(start_timestamp, end_timestamp, num_values=4):
    if start_timestamp >= end_timestamp:
        raise ValueError("start_timestamp must be less than end_timestamp")

    random_timestamps = [random.randint(start_timestamp, end_timestamp) for _ in range(num_values)]
    return random_timestamps
