import time
import random

def calculate_delay():
    random_hour = random.randint(4, 6) % 24
    random_minutes = random.randint(0, 59)
    random_seconds = random.randint(0, 59)

    delay = (random_hour * 3600) + (random_minutes * 60) + random_seconds

    return delay