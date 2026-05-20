import os
import re
import wfdb
import numpy as np
import pandas as pd

from disk_cache import get_or_create


# =========================
# CLEAN RECORD LIST
# =========================
def get_patient_records(patient_path):
    files = os.listdir(patient_path)

    records = sorted(set(
        f.replace(".dat", "")
        for f in files
        if f.endswith(".dat")
    ))

    return [r for r in records if not re.match(r".*n$", r)]


# =========================
# LOAD PATIENT (NO CACHE)
# =========================
def load_patient_data(patient_path):

    records = get_patient_records(patient_path)

    all_data = []
    cumulative_time = 0

    for record_name in records:

        record_path = os.path.join(patient_path, record_name)

        try:
            record = wfdb.rdrecord(record_path)

            fs = record.fs
            signals = np.array(record.p_signal)
            names = list(record.sig_name)

            # safety alignment
            n_channels = min(signals.shape[1], len(names))
            signals = signals[:, :n_channels]
            names = names[:n_channels]

            local_time = np.arange(len(signals)) / fs
            global_time = local_time + cumulative_time

            df = pd.DataFrame(signals, columns=names)
            df.insert(0, "time", global_time)

            all_data.append(df)

            cumulative_time += len(signals) / fs

        except Exception as e:
            print(f"Skipping {record_name}: {e}")

    return pd.concat(all_data, ignore_index=True)


# =========================
# WINDOW CACHE ONLY
# =========================
def get_resampled_windows(patient_id, df, window_size):

    mode = f"resample_{window_size}s"

    return get_or_create(
        patient_id=patient_id,
        mode=mode,
        builder_func=lambda: resample_windows(df, window_size)
    )


# =========================
# RESAMPLING
# =========================
def resample_windows(df, window_size):

    df = df.copy()

    df["window"] = (df["time"] // window_size).astype(int)

    grouped = df.groupby("window").mean(numeric_only=True)

    grouped["time"] = grouped.index * window_size

    return grouped.reset_index(drop=True)