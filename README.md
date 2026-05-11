# 🧠 ICU Dashboard – Continuous Signal Processing System

---

## 🚀 Version

**v0.4.0 — Time Continuity & Windowed Aggregation**

---

## 🎯 Key Features

### 🧩 Data Pipeline
- Loads multi-file WFDB ICU patient data
- Automatically filters invalid record files
- Extracts physiological signals (ECG, ABP, RESP, etc.)

---

### ⏱️ Continuous Time Reconstruction
- Converts segmented ICU recordings into a **single continuous timeline**
- Applies cumulative time offsets across all records
- Ensures correct temporal alignment of patient data

---

### 📊 Multi-Resolution Analysis
- Full signal visualization
- Windowed aggregation:
  - 5-second averages
  - 30-second averages
- Efficient vectorized computation (no loop-based filtering)

---

### ⚡ Performance Optimization
- Replaced slow filtering loops with `groupby` aggregation
- Added caching layer for faster reloading
- Optimized for large ICU datasets

---

### 🖥️ Interactive Dashboard (Dash + Plotly)
- Patient-based signal exploration
- Channel selection (physiological signals)
- Visualization modes:
  - Full signal
  - 5-second window
  - 30-second window
  - Average value

---

## 🧱 System Architecture

```text
WFDB ICU Files
      ↓
Data Loader (data_loader.py)
      ↓
Continuous Timeline Builder
      ↓
Pandas DataFrame (time + signals)
      ↓
Windowed Processor (5s / 30s aggregation)
      ↓
Dash Visualization Layer
📁 Project Structure
icu-dashboard/
│
├── data_loader.py     # WFDB loading + time continuity engine
├── processor.py       # signal processing & window aggregation
├── cache.py           # in-memory caching system
├── dashboard.py       # Dash UI application
│
├── sample/            # ICU patient WFDB datasets
├── requirements.txt
└── README.md
⚙️ Data Processing Flow
1. Load ICU Data
Reads WFDB .dat and .hea files per patient
Filters invalid or auxiliary files
2. Build Continuous Timeline
Applies cumulative time offsets across segments
Produces a unified patient timeline
3. Signal Extraction
Extracts physiological channels
Aligns all signals on shared time axis
4. Windowed Aggregation
Converts raw signals into:
5-second windows
30-second windows
Uses vectorized groupby operations
5. Visualization
Interactive Dash plots
Real-time signal switching
📊 Example Data Format
Raw Continuous Data
time   | ABP   | ECG   | RESP
0.00   | ...   | ...   | ...
0.01   | ...   | ...   | ...
Windowed Data (5s)
time | ABP_mean | ECG_mean | RESP_mean
0    | ...
5    | ...
10   | ...
⚠️ Design Decisions
🔹 Continuous Time Model

Segmented ICU files are merged into a single timeline using cumulative offsets.

🔹 Window-Based Aggregation

Signal analysis is performed over the full timeline, not partial slices.

🔹 Performance Optimization

Replaced O(n²) filtering with O(n) grouped aggregation.

🚀 Future Work (v0.5.0+)
Multi-panel ICU monitor layout
Real-time patient status detection (normal / warning / critical)
Persistent caching (disk-based)
Improved visualization UX (medical-grade layout)
Performance benchmarking for large datasets
🧠 Tech Stack
Python
WFDB (PhysioNet dataset format)
Pandas / NumPy
Plotly Dash
Git (version-controlled architecture)
Pandas / NumPy
Plotly Dash
Git (version-controlled architecture)
