# 🧠 ICU Dashboard – Continuous Signal Processing System

## 🚀 Version
**v0.5.0 — Clean Architecture + Window-Level Caching + Simplified Dashboard**

---

## 🎯 Overview

This project is an interactive ICU signal visualization system built with **Dash (Plotly)** and **WFDB (PhysioNet datasets)**.

It processes multi-segment ICU recordings into a continuous timeline and provides efficient window-based signal analysis (5s / 30s) with a lightweight disk caching system.

---

## ✨ Key Features

### 🧹 Simplified Dashboard
- Removed full-signal and average modes
- Focused visualization:
  - 5-second window aggregation
  - 30-second window aggregation

---

### 💾 Efficient Caching System
- Disk-based caching using pickle files
- Only caches **windowed data (5s / 30s)**
- Removes large full-patient cache (~450MB eliminated)
- Faster repeated analysis without recomputation

---

### ⏱️ Continuous Time Reconstruction
- Merges segmented WFDB recordings into a single timeline
- Applies cumulative time offsets across records
- Ensures correct temporal alignment

---

### 📊 Multi-Resolution Analysis
- Window-based aggregation:
  - 5-second mean signals
  - 30-second mean signals
- Vectorized Pandas operations (groupby-based)

---

### 🖥️ Interactive Dashboard (Dash + Plotly)
- Patient folder input
- Dynamic signal channel selection
- Interactive plotting
- Window mode switching (5s / 30s)

---

## 🧱 System Architecture


WFDB ICU Files
↓
data_loader.py
├── Continuous Time Builder
├── Signal Alignment
├── Window Aggregation (5s / 30s)
└── Cache Integration (disk_cache)
↓
disk_cache.py
└── Stores only windowed DataFrames
↓
dashboard.py
└── UI Layer (Dash + Plotly)


---

## 📁 Project Structure


icu-dashboard/
│
├── dashboard.py # Dash UI (simplified interface)
├── data_loader.py # WFDB loading + processing + caching logic
├── disk_cache.py # disk-based cache system (window-level only)
├── processor.py # signal utilities (optional helpers)
│
├── cache/ # generated .pkl cache files
├── sample/ # ICU WFDB datasets
├── requirements.txt
└── README.md


---

## ⚙️ Data Processing Flow

### 1. Load ICU Data
- Reads WFDB `.dat` and `.hea` files
- Filters invalid or auxiliary records

### 2. Build Continuous Timeline
- Merges segmented recordings
- Applies cumulative time offsets

### 3. Extract Signals
- Extracts physiological channels (e.g., ABP, ECG, RESP, PLETH)
- Aligns all signals on unified timeline

### 4. Windowed Aggregation
- 5-second and 30-second signal summarization
- Uses vectorized Pandas groupby operations

### 5. Caching Layer
- Stores only processed windowed outputs
- Avoids recomputation on repeated access

### 6. Visualization
- Interactive Dash dashboard
- Channel selection
- Window-based signal exploration

---

## 📊 Example Data Format

### Raw Continuous Data

time | ABP | ECG | RESP
0.00 | ... | ... | ...
0.01 | ... | ... | ...


### Windowed Data (5s / 30s)

time | ABP_mean | ECG_mean | RESP_mean
0 | ...
5 | ...
10 | ...


---

## ⚠️ Design Decisions

### 🔹 Removed Full-Patient Caching
- Eliminated ~450MB cache files
- Reduced storage overhead
- Avoided redundant preprocessing storage

---

### 🔹 Window-Centric Architecture
- System focuses on analysis-level outputs
- Not raw data persistence

---

### 🔹 Clean Layer Separation
- UI (dashboard.py)
- Processing (data_loader.py)
- Storage (disk_cache.py)

---

## 🚀 Future Work (v0.6.0+)

- Multi-patient comparison dashboard
- Memory caching layer (optional performance boost)
- Real-time ICU monitoring simulation
- Signal anomaly detection (ML integration)
- Medical-grade visualization UI redesign
- Performance benchmarking for large datasets

---

## 🧠 Tech Stack

- Python
- WFDB (PhysioNet format)
- Pandas / NumPy
- Plotly Dash
- Disk-based caching (pickle)
- Git (feature-branch workflow)

---

## ▶️ Run the Project

```bash
python dashboard.py

Then open:

http://127.0.0.1:8050/
