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

def prepare_pie_chart_data(df, column):
    """
    Returns counts for categorical data.
    e.g., {"Male": 10, "Female": 15}
    """
    counts = df[column].value_counts().head(10) # Limit to top 10 to avoid messy pies
    return {
        "labels": counts.index.tolist(),
        "values": counts.values.tolist()
    }