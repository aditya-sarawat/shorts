import random

def get_random(input_list):
    if not input_list:
        raise ValueError("Input list is empty")

    return random.choice(input_list)
