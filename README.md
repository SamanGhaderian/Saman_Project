🫀 ICU Multi-Patient Signal Dashboard (v7)

A scalable ICU time-series visualization system designed for multi-patient comparison using WFDB data, Parquet-based caching, and a Dash web interface.

🚀 Project Overview

This project transforms raw ICU physiological signals into a high-performance multi-patient analytics dashboard.

It includes:

Offline preprocessing pipeline
Parquet-based caching system
Multi-patient visualization dashboard
Fault-tolerant data handling
Time normalization for cross-patient comparison
🧠 Final Architecture
RAW WFDB DATA
     ↓
cache_builder.py (offline preprocessing)
     ↓
Parquet Cache (5s / 30s windows per patient)
     ↓
Dash Dashboard (visualization only)
📦 Key Features
✔ Multi-patient comparison (2–10+ patients)
✔ Window-based signal aggregation (5s / 30s)
✔ Parquet storage for fast loading
✔ Time normalization (absolute vs normalized 0–1)
✔ Automatic patient validation
✔ Skip/error reporting panel
✔ Loading status tracking per patient
✔ Channel intersection across patients
⚙️ Technologies Used
Python
Dash (Plotly)
Pandas
NumPy
WFDB (physiological signal loading)
PyArrow (Parquet engine)
Plotly Graph Objects
🔄 System Evolution (Development Progress)

This project went through multiple important iterations:

🟡 v5 – Initial Data Pipeline
✔ Features:
WFDB signal loading
DataFrame-based processing
Basic visualization
❌ Issues:
Slow runtime processing
No caching system
Dashboard recomputed everything on load
🟠 v6 – Runtime Cache System
✔ Improvements:
Introduced disk caching using pickle
Window-based aggregation (5s / 30s)
Faster dashboard loading
❌ Problems discovered:
Cache generated at runtime inside dashboard
Not scalable for multiple patients
Mixed preprocessing and visualization layers
🔵 v7 – Architecture Refactor (CURRENT)
✔ Major Improvements:
1. Offline preprocessing introduced
cache_builder.py created
All patients processed once
Eliminates runtime computation overhead
2. Parquet migration
Replaced pickle with Parquet storage
Improved read performance and scalability
3. Multi-patient scalability
Supports 10+ patients simultaneously
Dynamic patient loading from cache folder
🧩 Critical Bugs Encountered & Fixes
❌ Issue 1: Pandas concat crash (InvalidIndexError)
Error:
Reindexing only valid with uniquely valued Index objects
Cause:
Duplicate column names in WFDB signals
Inconsistent channel naming across records
Fix:
Forced unique column names
Removed duplicate columns before concat
names = pd.io.parsers.ParserBase({'names': names})._maybe_dedup_names(names)
df = df.loc[:, ~df.columns.duplicated()]
❌ Issue 2: WFDB record loading failure
Cause:
Incorrect assumption: .dat used as record identifier
Fix:
Switched to .hea based detection
Correct WFDB usage:
wfdb.rdrecord("patient/record_name")
❌ Issue 3: Dashboard crash with multiple patients
Cause:
Missing cache files for some patients
Empty or corrupted datasets
Missing signal channels
Fix:
Added validation layer:
skip empty datasets
skip missing channels
try/except per patient
❌ Issue 4: Time axis mismatch between patients
Cause:
Each patient had different cumulative time length
No normalization applied
Fix:

Added two modes:

✔ Absolute time:
time = time - min(time)
✔ Normalized time:
time = (t - t_min) / (t_max - t_min)
❌ Issue 5: UI scaling issue (5+ patients crash)
Cause:
Channel intersection based only on 2 patients
Missing validation for large groups
Fix:
Channel validation extended across all selected patients
Safe intersection logic added
❌ Issue 6: Poor UX (manual patient input)
Fix:
Removed manual path inputs
Added automatic patient discovery from cache folder
❌ Issue 7: No system transparency
Fix:

Added:

✔ Loading status panel per patient
✔ Skip/error reporting panel
✔ Automatic invalid patient filtering
✔ Tooltip labels in dropdown
📊 Final System Capabilities
🔹 Data Pipeline
WFDB → Pandas → Windowing → Parquet Cache
🔹 Visualization
Multi-patient signal comparison
Dynamic channel selection
Time normalization modes
🔹 Reliability
Fault-tolerant processing
Automatic skipping of corrupted data
Full logging system
📁 Project Structure
project/
│
├── cache_builder.py        # OFFLINE preprocessing
├── dashboard.py            # VISUALIZATION layer
├── data_loader.py          # cache loader
├── disk_cache.py           # Parquet storage engine
├── processor.py            # signal utilities
│
└── cache/
    ├── patient_01/
    │    ├── 5s.parquet
    │    └── 30s.parquet
    └── patient_02/
🚀 How to Run
Step 1 – Build cache (one-time)
python cache_builder.py
Step 2 – Start dashboard
python dashboard.py
🧠 Key Engineering Takeaways
Separation of preprocessing and visualization is critical for scalability
Real-world biomedical data is inconsistent → requires defensive design
Parquet significantly improves performance for time-series datasets
UI must reflect data quality (not assume clean data)
🎯 Future Improvements (optional)
Patient cohort statistics (mean/variance bands)
Real-time streaming support
Anomaly detection overlay
Dataset quality scoring system
👨‍💻 Author

Saman Ghaderian
Master’s Student – Software Technology
HFT Stuttgart
