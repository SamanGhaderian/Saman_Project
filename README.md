# 🫀 ICU Multi-Patient Signal Dashboard (v7)

A scalable ICU time-series visualization system using WFDB signals, offline preprocessing, and Parquet-based caching.

---

## 🚀 Overview

This system converts raw ICU signals into a fast multi-patient dashboard by separating:

- Offline preprocessing (cache_builder.py)
- Online visualization (Dash dashboard)

---

## 🧠 Final Architecture


RAW WFDB DATA
↓
cache_builder.py
↓
Parquet Cache (5s / 30s)
↓
Dash Dashboard


---

# 🔄 System Evolution & Fixes

Each section shows:
👉 Problem → Cause → Fix → Code

---

## ❌ Issue 1: Pandas concat crash (InvalidIndexError)

### Problem

Reindexing only valid with uniquely valued Index objects


### Cause
Duplicate column names in WFDB signals.

---

### Fix
Force unique column names before concat.

---

### Code Fix

```python
# BEFORE (problematic)
df = pd.DataFrame(signals, columns=names)

# AFTER (fixed)
seen = {}
clean_names = []

for n in names:
    if n not in seen:
        seen[n] = 0
        clean_names.append(n)
    else:
        seen[n] += 1
        clean_names.append(f"{n}_{seen[n]}")

df = pd.DataFrame(signals, columns=clean_names)

# remove duplicates safety
df = df.loc[:, ~df.columns.duplicated()]
❌ Issue 2: Wrong WFDB record loading
Problem

Some patients failed to load.

Cause

Using .dat instead of WFDB record names.

Fix

Use .hea files as entry point.

Code Fix
# BEFORE
for f in os.listdir(patient_path):
    if f.endswith(".dat"):

# AFTER
for f in os.listdir(patient_path):
    if f.endswith(".hea"):
        record_name = f.replace(".hea", "")
Correct loading
record = wfdb.rdrecord(os.path.join(patient_path, record_name))
❌ Issue 3: Dashboard crash with multiple patients
Problem
Callback error updating signal-plot.figure
Cause
Missing cache files
Empty datasets
Missing channels
Fix

Add validation before plotting.

Code Fix
df = load_patient_windows(p, f"{mode}s")

if df is None or df.empty:
    continue

if channel not in df.columns:
    continue
❌ Issue 4: Time mismatch between patients
Problem

Each patient had different time ranges:

Patient 1 → 200k
Patient 2 → 400k
Cause

Cumulative time preserved from raw WFDB records.

Fix

Add normalization in dashboard.

Code Fix
Absolute time
df["time"] = df["time"] - df["time"].min()
Normalized time (0–1)
tmin = df["time"].min()
tmax = df["time"].max()

df["time"] = (df["time"] - tmin) / (tmax - tmin)
❌ Issue 5: Channel mismatch across patients
Problem

Some patients missing signals → crash or empty plot.

Fix

Compute intersection across all selected patients.

Code Fix
common = set(dfs[0].columns)

for df in dfs[1:]:
    common = common.intersection(set(df.columns))

common.discard("time")
❌ Issue 6: Manual patient input (bad UX)
Problem

User had to manually type paths.

Fix

Auto-load from cache directory.

Code Fix
CACHE_ROOT = "cache"

patients = [
    p for p in os.listdir(CACHE_ROOT)
    if os.path.isdir(os.path.join(CACHE_ROOT, p))
]
❌ Issue 7: No system transparency
Problem

No visibility into:

skipped patients
errors
loading status
Fix

Add status reporting panel.

Code Fix
status_lines.append(f"✅ {p}: loaded")
status_lines.append(f"❌ {p}: empty dataset")
status_lines.append(f"⚠️ {p}: missing channel")
📦 Final System Structure
project/
│
├── cache_builder.py   # offline preprocessing
├── dashboard.py       # visualization
├── data_loader.py     # cache loader
├── disk_cache.py      # parquet system
├── processor.py       # utilities
│
└── cache/
    ├── patient_01/
    │   ├── 5s.parquet
    │   └── 30s.parquet
🚀 How to Run
Step 1: Build cache
python cache_builder.py
Step 2: Run dashboard
python dashboard.py
🧠 Key Takeaways
Real ICU data is inconsistent → requires defensive design
Offline preprocessing improves scalability
Parquet significantly improves performance
Visualization must not assume clean data
Separation of concerns is critical in medical systems
👨‍💻 Author

Saman Ghaderian
Master’s Student – Software Technology
HFT Stuttgart
