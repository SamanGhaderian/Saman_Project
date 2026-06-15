# 🏥 ICU Multi-Patient Similarity & Clustering Dashboard

## 📌 Overview

This project is an interactive ICU analytics dashboard for analyzing multi-patient physiological time-series data.  
It combines **signal processing, Dynamic Time Warping (DTW), clustering, and UMAP visualization** to discover hidden patterns in ICU patients.

The system enables:
- Multi-patient signal visualization
- Patient similarity computation
- Unsupervised clustering of patients
- 2D ICU population mapping

---

## 🎯 Goal

Transform raw ICU time-series data into:

> A structured, visual representation of patient similarity and group behavior.

---

## 🧠 Methods Used

### 1. Signal Preprocessing
- WFDB records loaded per patient
- Multiple records concatenated
- Windowing applied (5s / 30s)
- Signals normalized to fixed length (300 points)

---

### 2. Dynamic Time Warping (DTW)
DTW is used to compute similarity between time-series by aligning them in time.

- Handles time shifts in physiological signals
- Produces a pairwise distance between patients

Output:
- `N × N` similarity matrix

---

### 3. Similarity Matrix
A full matrix is built:


D[i][j] = DTW(patient_i, patient_j)


Represents ICU patient-to-patient distances.

---

### 4. Hierarchical Clustering
Using:

```python
AgglomerativeClustering(metric="precomputed")
Groups patients based on DTW distance
Produces cluster labels

Output:

Patient clusters (groups)
5. UMAP Embedding

UMAP is applied on the DTW matrix:

Reduces high-dimensional similarity space to 2D
Preserves local structure

Output:

ICU 2D patient map
⚙️ System Architecture
Raw WFDB Data
      ↓
Preprocessing (windowing + normalization)
      ↓
Fixed-length time series (300 points)
      ↓
DTW pairwise computation
      ↓
Similarity matrix
      ↓
├── Hierarchical clustering
└── UMAP projection
      ↓
Dash visualization layer
🚀 Features
Multi-patient selection
Signal plotting (ABP, HR, etc.)
Time mode selection (absolute / normalized)
DTW-based similarity computation
Hierarchical clustering
UMAP ICU map visualization
Cluster-based coloring
📦 Installation
pip install numpy pandas wfdb dash plotly scikit-learn umap-learn
▶️ How to Run
python Dashboard.py

Then open the local Dash server link.

📊 Workflow
Select patients
Select signal (e.g., ABP)

Click:

Run DTW + Clustering + UMAP
View:
Cluster results
ICU similarity map
📈 Outputs
1. Clusters

Groups of similar patients based on physiological behavior.

2. UMAP Map

2D visualization of ICU population structure.

Each point represents a patient:

Distance ≈ similarity
Color = cluster membership
⚠️ Limitations
DTW is still computationally expensive
UMAP is stochastic (small variations per run)
Only unsupervised learning (no clinical labels)
🔮 Future Improvements
FastDTW / Soft-DTW optimization
Feature-based modeling (instead of raw signals)
Real-time ICU streaming support
Risk prediction layer
Clinical validation
👨‍💻 Author

Saman Ghaderian
Master’s in Software Technology
HFT Stuttgart
