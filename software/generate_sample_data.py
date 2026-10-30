import csv
import numpy as np

sample_rate = 8000
duration = 5
samples = sample_rate * duration

rng = np.random.default_rng(42)
time = np.arange(samples) / sample_rate

# Synthetic vibration signal — not real leak data
source = rng.normal(0, 1, samples)

sensor_a = source + 0.15 * rng.normal(size=samples)

delay = 12
sensor_b = np.roll(source, delay)
sensor_b += 0.15 * rng.normal(size=samples)

with open("sample_recording.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["time_s", "sensor_a", "sensor_b"])

    for t, a, b in zip(time, sensor_a, sensor_b):
        writer.writerow([t, a, b])

print("Synthetic test recording created.")