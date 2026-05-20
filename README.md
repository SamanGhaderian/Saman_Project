# 🧠 ICU Dashboard – Multi-Patient Signal Comparison System

## 🚀 Version
**v0.6.1 — Multi-Patient Comparison + Window-Level Caching Only (No Full Data Cache)**

---

## 🎯 Overview

This project is an ICU signal analysis and visualization system built with:

- **Dash (Plotly)** for interactive UI  
- **WFDB (PhysioNet)** for ICU physiological data  
- **Pandas / NumPy** for signal processing  
- **Disk-based caching (window-level only)**  

It enables **comparison of two ICU patients** using synchronized window-based signal analysis.

---

## ✨ Key Features

### 👥 Multi-Patient Comparison
- Load and compare **two ICU patients simultaneously**
- Overlay signals on a single graph
- Color-coded patient visualization
- Automatic detection of shared signal channels

---

### 💾 Lightweight Caching Strategy (IMPORTANT)
- ❌ No full-patient cache (avoids large 100MB–500MB files)
- ✔ Only caches processed windowed outputs:
  - 5-second aggregated signals
  - 30-second aggregated signals
- ✔ Cache is reusable across sessions

---

### ⏱ Continuous Time Reconstruction
- Merges segmented WFDB recordings
- Builds continuous patient timeline
- Ensures correct signal alignment across records

---

### 📊 Window-Based Signal Analysis
- 5-second mean aggregation
- 30-second mean aggregation
- Efficient vectorized Pandas groupby operations
- Cached per patient + window size

---

### 🖥 Interactive Dashboard (Dash + Plotly)
- Two patient input fields
- Signal selection dropdown
- Window mode switch (5s / 30s)
- Real-time comparative visualization

---

## 🧱 System Architecture


WFDB ICU Files
↓
data_loader.py
├── Continuous Time Builder
├── Signal Alignment
├── Window Aggregation (5s / 30s)
└── Disk Cache (window-level only)
↓
disk_cache.py
└── Stores ONLY aggregated window results
↓
dashboard.py
└── Multi-patient visualization layer


---

## 📁 Project Structure


icu-dashboard/
│
├── dashboard.py # Multi-patient Dash UI
├── data_loader.py # WFDB loading + processing logic
├── disk_cache.py # Window-level caching system
├── processor.py # Optional signal utilities
│
├── cache/ # Cached windowed .pkl files
├── sample/ # ICU WFDB datasets
├── requirements.txt
└── README.md


---

## ⚙️ Data Processing Flow

### 1. Patient Selection
- User enters paths for two ICU patients
- System extracts patient IDs for cache keys

---

### 2. Data Loading (No Full Cache)
- WFDB files are parsed every session if needed
- Continuous time is reconstructed per patient
- No large full-patient files are stored

---

### 3. Signal Extraction
- Extracts physiological signals such as:
  - ECG (e.g., III)
  - ABP
  - RESP
  - PLETH
- Aligns signals on a unified time axis

---

### 4. Windowed Aggregation + Cache
- 5-second and 30-second mean signals
- Cached per:
  - patient_id
  - window_size
- Avoids recomputation of expensive aggregations

---

### 5. Multi-Patient Visualization
- Two independent patient timelines
- Overlayed signal comparison
- Shared channel selection across both patients

---

## 📊 Example Visualization

### Raw Signal Concept

Patient 1: ECG ────▁▂▃▅▆▇
Patient 2: ECG ──▂▃▅▆▇█


---

### Windowed Comparison (5s / 30s)

Time → 0 5 10 15

P1: ▄▆█ ▅▆█ ▆▇█
P2: ▃▅█ ▅▇█ ▇█▇


---

## ⚠️ Design Decisions

### 🔹 No Full Patient Cache
- Avoids large storage usage
- Keeps system lightweight and portable
- Ensures reproducibility from raw WFDB data

---

### 🔹 Window-Level Cache Only
- Stores only computed analysis results
- Optimized for repeated visualization
- Small file footprint

---

### 🔹 Multi-Patient Model
- Patients are processed independently
- Comparison happens only at visualization layer
- No merging of raw datasets

---

## 🚀 Performance Characteristics

| Operation | Speed |
|------------|------|
| First load (WFDB) | Medium |
| Window generation | Fast (cached after first run) |
| Switching signals | Fast |
| Multi-patient overlay | Efficient |

---

## 🚀 Future Work (v0.7.0+)

- Add 3+ patient comparison
- Normalize signals for fair comparison
- Add patient alignment (time synchronization)
- Add difference mode (P1 − P2)
- Add anomaly detection (ML-based)
- Improve ICU-style UI layout

---

## 🧠 Tech Stack

- Python
- WFDB (PhysioNet ICU format)
- Pandas / NumPy
- Plotly Dash
- Disk-based caching (window-level only)
- Git feature-branch workflow

---

## ▶️ Run Project

```bash
python dashboard.py

Then open:

http://127.0.0.1:8050/
