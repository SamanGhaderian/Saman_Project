import os
import re
import wfdb
import numpy as np
import pandas as pd


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
# LOAD FULL PATIENT WITH
# CONTINUOUS TIME
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
            signals = record.p_signal
            names = record.sig_name

            # local segment time
            local_time = np.arange(len(signals)) / fs

            # global continuous time
            global_time = local_time + cumulative_time

            df = pd.DataFrame(signals, columns=names)
            df.insert(0, "time", global_time)

            all_data.append(df)

            # update cumulative offset
            segment_duration = len(signals) / fs
            cumulative_time += segment_duration

            print(f"Loaded {record_name} "
                  f"({segment_duration:.2f}s) "
                  f"→ total: {cumulative_time:.2f}s")

        except Exception as e:
            print(f"Skipping {record_name}: {e}")

    full_df = pd.concat(all_data, ignore_index=True)

    return full_df
def resample_windows(df, window_size):

    df = df.copy()

    # assign each row to a window index
    df["window"] = (df["time"] // window_size).astype(int)

    # group by window
    grouped = df.groupby("window").mean(numeric_only=True)

    # reconstruct time as window start
    grouped["time"] = grouped.index * window_size

    return grouped.reset_index(drop=True)