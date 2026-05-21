from disk_cache import load_from_disk


def load_patient_windows(patient_id, mode):
    return load_from_disk(patient_id, mode)