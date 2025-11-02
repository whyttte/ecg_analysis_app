import pandas as pd
from scipy.signal import find_peaks

def analyze_ecg(signal, sampling_rate):
    """
    Analyzes ECG data to find heart rate and other metrics.
    """
    # Find R-peaks
    distance = (sampling_rate / 200) * 60 # Heuristic for distance between peaks
    peaks, _ = find_peaks(signal, height=signal.quantile(0.9), distance=distance)

    # Calculate heart rate
    if len(peaks) > 1:
        # Calculate the average distance between peaks
        avg_distance = pd.Series(peaks).diff().mean()
        heart_rate = (sampling_rate / avg_distance) * 60
    else:
        heart_rate = 0

    interpretation = f"Average Heart Rate: {heart_rate:.2f} bpm (at {sampling_rate} Hz)"

    return interpretation, peaks
