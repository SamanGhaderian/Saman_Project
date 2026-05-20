import os
import pandas as pd

# =========================
# CACHE DIRECTORY
# =========================
CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)


# =========================
# GENERATE CACHE PATH
# =========================
def get_cache_path(patient_id, mode):
    filename = f"{patient_id}_{mode}.pkl"
    return os.path.join(CACHE_DIR, filename)


# =========================
# CHECK CACHE EXISTS
# =========================
def cache_exists(patient_id, mode):
    path = get_cache_path(patient_id, mode)
    return os.path.exists(path)


# =========================
# SAVE DATAFRAME
# =========================
def save_to_disk(df, patient_id, mode):
    path = get_cache_path(patient_id, mode)
    df.to_pickle(path)
    print(f"Saved cache: {path}")


# =========================
# LOAD DATAFRAME (SAFE)
# =========================
def load_from_disk(patient_id, mode):
    path = get_cache_path(patient_id, mode)

    if not os.path.exists(path):
        print(f"Cache miss: {path}")
        return None

    print(f"Loading cache: {path}")
    return pd.read_pickle(path)


# =========================
# GET OR CREATE (RECOMMENDED)
# =========================
def get_or_create(patient_id, mode, builder_func):
    """
    If cache exists → load it
    If not → compute using builder_func and save it
    """

    path = get_cache_path(patient_id, mode)

    if os.path.exists(path):
        print(f"Loading cache: {path}")
        return pd.read_pickle(path)

    print(f"Cache miss. Building: {path}")
    data = builder_func()

    if not isinstance(data, pd.DataFrame):
        raise ValueError("Cache system currently supports only pandas DataFrame")

    data.to_pickle(path)
    print(f"Saved cache: {path}")

    return data