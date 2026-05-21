# 🫀 ICU Multi-Patient Signal Dashboard (v7)

A scalable ICU time-series visualization system for multi-patient comparison using WFDB signals, offline preprocessing, and Parquet-based caching.

---

## 🚀 Overview

This project processes raw ICU physiological data and transforms it into a fast, interactive multi-patient dashboard.

It separates:

- **Offline preprocessing (cache building)**
- **Online visualization (Dash dashboard)**

This design removes runtime computation and enables scalable multi-patient analysis.

---

## 🧠 Final Architecture


RAW WFDB DATA
↓
cache_builder.py (offline preprocessing)
↓
Parquet Cache (5s / 30s windows per patient)
↓
Dash Dashboard (visualization only)


---

## 📦 Features

- Multi-patient comparison (2–10+ patients)
- Window-based signal aggregation (5s / 30s)
- Parquet-based caching for fast loading
- Time normalization (absolute & normalized modes)
- Automatic patient validation system
- Skip/error reporting panel
- Loading status per patient
- Channel intersection across patients
- Fully scalable architecture

---

## ⚙️ Tech Stack

- Python
- Dash (Plotly)
- Pandas
- NumPy
- WFDB
- PyArrow (Parquet engine)
- Plotly Graph Objects

---

## 🔄 System Evolution

### 🟡 v5 – Initial Pipeline
- WFDB loading
- Basic DataFrame processing
- Simple visualization

❌ Issues:
- Slow runtime processing
- No caching
- Dashboard recomputed everything

---

### 🟠 v6 – Runtime Cache System
- Introduced caching (pickle-based)
- Window aggregation (5s / 30s)
- Faster dashboard performance

❌ Issues:
- Cache generated inside dashboard
- No separation between preprocessing and UI
- Not scalable

---

### 🔵 v7 – Final Architecture (CURRENT)

✔ Offline preprocessing introduced  
✔ Parquet-based storage  
✔ Multi-patient scalability  
✔ Robust validation system  
✔ Fault-tolerant pipeline  

---

## 🧩 Major Issues & Fixes

### ❌ Pandas concat crash (InvalidIndexError)

**Cause:**
- Duplicate column names from WFDB signals

**Fix:**
- Forced unique column names
- Removed duplicate columns before concat

---

### ❌ Wrong WFDB record loading

**Cause:**
- Using `.dat` instead of WFDB record names

**Fix:**
- Switched to `.hea`-based record discovery

---

### ❌ Dashboard crash with multiple patients

**Cause:**
- Missing cache files or empty datasets

**Fix:**
- Added validation layer
- Safe skipping of invalid patients

---

### ❌ Time mismatch between patients

**Cause:**
- Different cumulative time ranges per patient

**Fix:**
- Added time normalization:
  - Absolute mode
  - Normalized (0–1) mode

---

### ❌ Channel mismatch across patients

**Cause:**
- Different signal sets per patient

**Fix:**
- Dynamic intersection across selected patients

---

### ❌ Poor UI usability

**Fix:**
- Removed manual patient input
- Added automatic patient detection from cache
- Added validation + skip report panel

---

## 📁 Project Structure


project/
│
├── cache_builder.py # Offline preprocessing
├── dashboard.py # Visualization layer
├── data_loader.py # Cache loader
├── disk_cache.py # Parquet storage system
├── processor.py # Signal utilities
│
└── cache/
├── patient_01/
│ ├── 5s.parquet
│ └── 30s.parquet
└── patient_02/


---

## 🚀 How to Run

### Step 1: Build cache (one-time)

```bash
python cache_builder.py
Step 2: Run dashboard
python dashboard.py
🧠 Key Takeaways
Offline preprocessing is essential for scalability
Real ICU data is noisy and inconsistent
Fault tolerance is required for medical datasets
Parquet significantly improves performance
Separation of compute and visualization is critical
📌 Future Improvements
Cohort-level statistics (mean/variance bands)
Anomaly detection overlay
Real-time streaming support
Dataset quality scoring system
👨‍💻 Author

Saman Ghaderian
Master’s Student – Software Technology
HFT Stuttgart
