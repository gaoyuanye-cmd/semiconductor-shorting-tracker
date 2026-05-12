import numpy as np

def rolling_zscore(series, window=60):
    if len(series) < window:
        return 0
    mean = series[-window:].mean()
    std = series[-window:].std()
    if std == 0:
        return 0
    return (series.iloc[-1] - mean) / std
