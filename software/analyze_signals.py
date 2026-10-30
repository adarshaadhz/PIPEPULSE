import argparse
import csv
from pathlib import Path

import numpy as np
from scipy.signal import butter, sosfiltfilt, correlate, correlation_lags


def load_signals(filename):
    """Load two synchronized sensor channels from a CSV file."""
    time_values = []
    sensor_a = []
    sensor_b = []

    with open(filename, newline="") as file:
        reader = csv.DictReader(file)

        required = {"sensor_a", "sensor_b"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(
                "CSV must contain sensor_a and sensor_b columns"
            )

        for row in reader:
            sensor_a.append(float(row["sensor_a"]))
            sensor_b.append(float(row["sensor_b"]))

            if "time_s" in row and row["time_s"]:
                time_values.append(float(row["time_s"]))

    if len(sensor_a) < 100:
        raise ValueError("Recording is too short for analysis")

    return np.asarray(sensor_a), np.asarray(sensor_b), time_values


def bandpass_filter(signal, sample_rate, low=20, high=2000):
    """Remove frequencies outside the selected analysis band."""
    if high >= sample_rate / 2:
        raise ValueError("High cutoff must be below Nyquist frequency")

    sos = butter(
        4,
        [low, high],
        btype="bandpass",
        fs=sample_rate,
        output="sos"
    )

    return sosfiltfilt(sos, signal)


def calculate_rms(signal):
    """Calculate root mean square signal amplitude."""
    return float(np.sqrt(np.mean(signal ** 2)))


def calculate_correlation(signal_a, signal_b):
    """Estimate relative time delay using cross-correlation."""
    a = signal_a - np.mean(signal_a)
    b = signal_b - np.mean(signal_b)

    correlation = correlate(a, b, mode="full", method="fft")
    lags = correlation_lags(len(a), len(b), mode="full")

    best_lag = int(lags[np.argmax(np.abs(correlation))])

    return best_lag, float(best_lag)


def analyse_file(filename, sample_rate, output):
    sensor_a, sensor_b, _ = load_signals(filename)

    filtered_a = bandpass_filter(sensor_a, sample_rate)
    filtered_b = bandpass_filter(sensor_b, sample_rate)

    rms_a = calculate_rms(filtered_a)
    rms_b = calculate_rms(filtered_b)

    lag_samples, _ = calculate_correlation(
        filtered_a, filtered_b
    )

    lag_seconds = lag_samples / sample_rate

    results = {
        "samples": len(sensor_a),
        "sample_rate_hz": sample_rate,
        "rms_sensor_a": rms_a,
        "rms_sensor_b": rms_b,
        "lag_samples": lag_samples,
        "lag_seconds": lag_seconds,
    }

    with open(output, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=results.keys())
        writer.writeheader()
        writer.writerow(results)

    print("PIPEPULSE signal analysis complete")
    for key, value in results.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyse two-channel PIPEPULSE recordings"
    )

    parser.add_argument("input", help="Input sensor CSV file")
    parser.add_argument(
        "--sample-rate",
        type=float,
        default=8000,
        help="Sampling rate in Hz (default: 8000)"
    )
    parser.add_argument(
        "--output",
        default="analysis_results.csv",
        help="Output results CSV"
    )

    args = parser.parse_args()

    analyse_file(args.input, args.sample_rate, args.output)
