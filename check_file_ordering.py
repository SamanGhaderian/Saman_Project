import os
import wfdb
import numpy as np

def get_sorted_records(patient_path):
    files = os.listdir(patient_path)

    records = sorted(set(
        f.replace(".dat", "")
        for f in files
        if f.endswith(".dat")
    ))

    # remove noise like 252n
    records = [r for r in records if not r.endswith("n")]

    return sorted(records)
def check_segment_time(patient_path, record_name):
    record_path = f"{patient_path}\\{record_name}"
    record = wfdb.rdrecord(record_path)

    fs = record.fs
    length = len(record.p_signal)

    duration = length / fs

    print(f"{record_name}:")
    print(f"  samples: {length}")
    print(f"  fs: {fs}")
    print(f"  duration (sec): {duration:.2f}")
patient_path = r"c:\users\saman\desktop\sample\252"
records = get_sorted_records(patient_path)
check_segment_time(patient_path, records[0])
check_segment_time(patient_path, records[1])
print("First 10 records:")
print(records[:10])