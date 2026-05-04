import os
import wfdb

def get_sorted_records(patient_path):
    files = os.listdir(patient_path)

    records = sorted(set(
        f.replace(".dat", "")
        for f in files
        if f.endswith(".dat")
    ))

    records = [r for r in records if not r.endswith("n")]
    return sorted(records)


def load_record(patient_path, record_name):
    record_path = os.path.join(patient_path, record_name)
    record = wfdb.rdrecord(record_path)

    signal = record.p_signal
    fs = record.fs
    sig_names = record.sig_name

    return signal, fs, sig_names