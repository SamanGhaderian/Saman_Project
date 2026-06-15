import numpy as np
from data_loader import load_patient_windows
from dtw import dtw_distance
from preprocess import normalize_series


def build_similarity_matrix(patients, channel, mode="5s"):
    signals = {}

    # STEP 1: LOAD + PREPROCESS
    for p in patients:
        df = load_patient_windows(p, mode)

        if df is None or df.empty:
            continue

        if channel not in df.columns:
            continue

        series = df[channel].values

        # 🔥 CRITICAL FIX
        signals[p] = normalize_series(series, max_len=300)

    patient_list = list(signals.keys())
    n = len(patient_list)

    if n < 2:
        return patient_list, np.array([])

    matrix = np.zeros((n, n))

    # STEP 2: DTW
    for i in range(n):
        for j in range(n):

            if i == j:
                matrix[i][j] = 0

            elif j < i:
                matrix[i][j] = matrix[j][i]

            else:
                a = signals[patient_list[i]]
                b = signals[patient_list[j]]

                matrix[i][j] = dtw_distance(a, b)

    return patient_list, matrix