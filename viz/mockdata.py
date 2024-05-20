import random
import numpy as np
from datetime import datetime, timedelta

# Get the current date and time
current_date = datetime.now()

# Calculate the date from one month ago
one_month_ago = current_date - timedelta(days=30)

# Generate an array of timestamps for the past month
timestamps = []
for _ in range(5000):
    # Generate a random timestamp between one month ago and now
    timestamp = one_month_ago + timedelta(
        seconds=random.randint(0, int((current_date - one_month_ago).total_seconds()))
    )
    timestamps.append(timestamp)

# Sort the timestamps
timestamps.sort()


# Define the size of the array
def biased_random():
    return random.random() ** 2 * 25


# Generate the array
array = [biased_random() for _ in range(5000)]

data = {
    "_id": [i for i in range(5000)],
    "user_id": [str(random.randint(1, 5000)) for _ in range(5000)],
    "created": timestamps,
    "user_latency": array,
}
