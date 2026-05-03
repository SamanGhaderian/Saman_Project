import os
import re
import wfdb
import numpy as np
import pandas as pd


# =========================
# 1. CLEAN RECORD LIST
# =========================
def get_clean_records(patient_path):
    files = os.listdir(patient_path)

    records = sorted(set(
        f.replace(".dat", "")
        for f in files
        if f.endswith(".dat")
    ))

    # ignore noisy files like 252n
    clean_records = [r for r in records if not re.match(r".*n$", r)]

    return clean_records


# =========================
# 2. LOAD ONE RECORD (RAW)
# =========================
def load_record_raw(patient_path, record_name):
    record_path = os.path.join(patient_path, record_name)

    record = wfdb.rdrecord(record_path)

    fs = record.fs
    signals = record.p_signal
    names = record.sig_name

    time = np.arange(len(signals)) / fs

    df = pd.DataFrame(signals, columns=names)
    df.insert(0, "time", time)

    return df


# =========================
# 3. LOAD FULL PATIENT (RAW)
# =========================
def load_patient_raw(patient_path):
    records = get_clean_records(patient_path)

    dfs = []

    for r in records:
        try:
            df = load_record_raw(patient_path, r)
            dfs.append(df)
        except Exception as e:
            print(f"Skipping {r}: {e}")

    return pd.concat(dfs, ignore_index=True)


# =========================
# 4. MEDIUM LAYER (5 sec)
# =========================
def create_medium_layer(df):
    df = df.copy()

    df["time"] = pd.to_timedelta(df["time"], unit="s")
    df = df.set_index("time")

    df_5s = df.resample("5s").mean()

    df_5s = df_5s.reset_index()
    df_5s["time"] = df_5s["time"].dt.total_seconds()

    return df_5s


# =========================
# 5. SUMMARY LAYER (30 sec)
# =========================
def create_summary_layer(df):
    df = df.copy()

    df["time"] = pd.to_timedelta(df["time"], unit="s")
    df = df.set_index("time")

    df_30s = df.resample("30s").agg(["mean", "min", "max"])

    df_30s.columns = ["_".join(col) for col in df_30s.columns]
    df_30s = df_30s.reset_index()
    df_30s["time"] = df_30s["time"].dt.total_seconds()

    return df_30s


# =========================
# 6. MASTER FUNCTION
# =========================
def load_patient_all_layers(patient_path):
    raw = load_patient_raw(patient_path)

    medium = create_medium_layer(raw)

    summary = create_summary_layer(raw)

    return raw, medium, summary


# =========================
# 7. TEST RUN
# =========================
if __name__ == "__main__":
    patient_path = r"c:\users\saman\desktop\sample\252"

    raw, medium, summary = load_patient_all_layers(patient_path)

    print("\n===== SHAPES =====")
    print("RAW:", raw.shape)
    print("5s :", medium.shape)
    print("30s:", summary.shape)

    print("\n===== RAW PREVIEW =====")
    print(raw.head())