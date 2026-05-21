import os
import pandas as pd

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)


def get_cache_path(patient_id, mode):
    folder = os.path.join(CACHE_DIR, patient_id)
    os.makedirs(folder, exist_ok=True)

    return os.path.join(folder, f"{mode}.parquet")


def cache_exists(patient_id, mode):
    return os.path.exists(get_cache_path(patient_id, mode))


def save_to_disk(df, patient_id, mode):
    path = get_cache_path(patient_id, mode)
    df.to_parquet(path, index=False)
    print(f"Saved: {path}")


def load_from_disk(patient_id, mode):
    path = get_cache_path(patient_id, mode)

    if not os.path.exists(path):
        print(f"Cache miss: {path}")
        return None

    return pd.read_parquet(path)


def get_or_create(patient_id, mode, builder_func):
    path = get_cache_path(patient_id, mode)

    if os.path.exists(path):
        return pd.read_parquet(path)

    df = builder_func()
    df.to_parquet(path, index=False)
    return df