import numpy as np

def normalize_series(series, max_len=300):
    """
    Safe preprocessing for ICU signals:
    - removes NaN
    - resamples to fixed length
    """

    series = np.array(series)
    series = series[~np.isnan(series)]

    if len(series) == 0:
        return np.zeros(max_len)

    if len(series) > max_len:
        # smooth downsampling (IMPORTANT)
        x_old = np.linspace(0, 1, len(series))
        x_new = np.linspace(0, 1, max_len)
        series = np.interp(x_new, x_old, series)

    return series[:max_len]