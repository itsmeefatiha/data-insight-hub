import pandas as pd
import numpy as np
import os

def prepare_histogram_data(df, column):
    """
    Returns data for a Bar Chart / Histogram.
    Bins the data into ranges (e.g., 0-10, 10-20).
    """
    # Drop empty values to avoid errors
    data = df[column].dropna()
    
    # Numpy automatically calculates the best bins
    counts, bin_edges = np.histogram(data, bins='auto')
    
    return {
        "labels": [f"{int(bin_edges[i])}-{int(bin_edges[i+1])}" for i in range(len(counts))],
        "values": counts.tolist()
    }