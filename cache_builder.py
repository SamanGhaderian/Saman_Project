import os
import wfdb
import numpy as np
import pandas as pd

from disk_cache import save_to_disk, cache_exists


# =========================
# CONFIG
# =========================
WINDOWS = [5, 30]


# =========================
# GET PATIENTS
# =========================
def get_patients(dataset_path):
    return [
        p for p in os.listdir(dataset_path)
        if os.path.isdir(os.path.join(dataset_path, p))
    ]


# =========================
# GET WFDB RECORDS (CORRECT WAY)
# =========================
def get_records(patient_path):

    # WFDB standard: detect .hea files
    records = [
        f.replace(".hea", "")
        for f in os.listdir(patient_path)
        if f.endswith(".hea")
    ]

    return sorted(records)


# =========================
# LOAD PATIENT DATA (FIXED)
# =========================
def load_patient_data(patient_path):

    records = get_records(patient_path)

    all_data = []
    cumulative_time = 0

    if len(records) == 0:
        return pd.DataFrame()

    for record_name in records:

        record_path = os.path.join(patient_path, record_name)

        try:
            record = wfdb.rdrecord(record_path)

            fs = record.fs
            signals = np.array(record.p_signal)
            names = list(record.sig_name)

            if signals is None or len(signals) == 0:
                continue

            n_channels = min(signals.shape[1], len(names))
            signals = signals[:, :n_channels]
            names = names[:n_channels]

            # 🔥 CRITICAL FIX: force UNIQUE column names
            seen = {}
            clean_names = []

            for n in names:
                if n not in seen:
                    seen[n] = 0
                    clean_names.append(n)
                else:
                    seen[n] += 1
                    clean_names.append(f"{n}_{seen[n]}")

            local_time = np.arange(len(signals)) / fs
            global_time = local_time + cumulative_time

            df = pd.DataFrame(signals, columns=clean_names)

            # ensure time column is clean
            df.insert(0, "time", global_time)

            # extra safety: ensure NO duplicate columns
            df = df.loc[:, ~df.columns.duplicated()]

            all_data.append(df)

            cumulative_time += len(signals) / fs

        except Exception as e:
            print(f"Skipping {record_name}: {e}")

    if len(all_data) == 0:
        return pd.DataFrame()

    # 🔥 SAFE CONCAT (important)
    return pd.concat(all_data, ignore_index=True, sort=False, verify_integrity=False)

# =========================
# WINDOWING
# =========================
def create_windows(df, window_size):

    if df.empty:
        return df

    df = df.copy()

    df["window"] = (df["time"] // window_size).astype(int)

    grouped = df.groupby("window").mean(numeric_only=True)

    grouped["time"] = grouped.index * window_size

    return grouped.reset_index(drop=True)


# =========================
# BUILD CACHE
# =========================
def build_patient_cache(patient_id, patient_path):

    print(f"\nProcessing {patient_id}")

    df = load_patient_data(patient_path)

    if df.empty:
        print(f"EMPTY → {patient_id}")
        return

    for w in WINDOWS:

        mode = f"{w}s"

        if cache_exists(patient_id, mode):
            print(f"Exists → {patient_id} {mode}")
            continue

        window_df = create_windows(df, w)

        if window_df.empty:
            print(f"Empty window → {patient_id} {mode}")
            continue

        save_to_disk(window_df, patient_id, mode)

    print(f"Done → {patient_id}")


# =========================
# MAIN
# =========================
if __name__ == "__main__":

    DATASET_PATH = r"C:\Users\Saman\Desktop\sample"

    patients = get_patients(DATASET_PATH)

    print(f"Found patients: {len(patients)}")

    for p in patients:
        build_patient_cache(
            patient_id=p,
            patient_path=os.path.join(DATASET_PATH, p)
        )

    print("\nDONE")