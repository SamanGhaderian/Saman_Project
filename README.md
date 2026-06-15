🏥 ICU Multi-Patient Similarity & Clustering Dashboard
Overview

This project is an interactive ICU analytics dashboard that enables multi-patient physiological similarity analysis using time-series methods. It combines:

Signal preprocessing
Dynamic Time Warping (DTW)
Hierarchical clustering
UMAP dimensionality reduction
Interactive visualization (Dash + Plotly)

The system allows exploration of ICU patient cohorts and discovery of hidden physiological patterns and clusters.

🎯 Project Goal

To transform raw ICU time-series data into:

A structured, visual representation of patient similarity and group behavior.

This enables:

Patient similarity comparison
Cluster discovery (phenotype-like grouping)
Visual ICU population mapping
Exploratory medical data analysis
🧠 Methods Used
1. Signal Preprocessing

Each patient time-series is:

Loaded from WFDB records
Concatenated across multiple records
Converted into continuous time-series
Windowed into fixed intervals (5s / 30s)
Normalized and resampled to fixed length (300 points)
Purpose:

Ensure uniform input size for all downstream algorithms.

2. Dynamic Time Warping (DTW)

DTW is used to measure similarity between two time-series.

Key idea:

It aligns signals by allowing non-linear time shifts.

Example:

Patient A heart rate may rise earlier than Patient B
DTW aligns them before measuring distance
Output:

A pairwise distance matrix between all patients.

3. Similarity Matrix Construction

For N patients:

Compute DTW distance for every pair
Build an N × N symmetric matrix
Output:

A full ICU patient-to-patient similarity graph

4. Hierarchical Clustering

We apply:

AgglomerativeClustering(metric="precomputed")
Method:
Uses DTW distance matrix
Merges closest patients iteratively
Forms hierarchical groups
Output:
Patient cluster labels
Grouped patient cohorts
5. UMAP Dimensionality Reduction

We use:

UMAP(metric="precomputed")
Purpose:

Project high-dimensional DTW space into 2D.

Output:
2D patient embeddings
Preserves neighborhood structure
6. Visualization Layer

Built using Plotly + Dash

Features:
Multi-patient signal visualization
Interactive selection of channels
ICU similarity map (UMAP)
Cluster-based coloring
Real-time analysis button
⚙️ System Architecture
Raw WFDB Data
      ↓
Patient Loader
      ↓
Windowing (5s / 30s)
      ↓
Normalization (fixed-length 300)
      ↓
DTW Pairwise Distance Computation
      ↓
Similarity Matrix
      ↓
├── Hierarchical Clustering
└── UMAP Projection
      ↓
Interactive Dashboard (Dash + Plotly)
🚀 Key Improvements Implemented
🔴 1. Performance Fix (Critical)

Before:

Full-length raw signals used in DTW
Extremely slow computation (minutes per run)

After:

Fixed-length signals (300 points)
Downsampling + interpolation
Stable and fast execution
🔴 2. Stable DTW Pipeline

Before:

Uncontrolled computation cost
Risk of freezing UI

After:

Deterministic runtime per comparison
Safe bounded computation
🔴 3. Scalable Similarity Matrix

Before:

No controlled preprocessing

After:

Centralized similarity matrix builder
Reusable DTW results
🔴 4. Clustering Integration

Before:

No grouping logic

After:

Hierarchical clustering using DTW distances
Automatic patient grouping
🔴 5. ICU Embedding Visualization (UMAP)

Before:

Only raw signal plots

After:

2D ICU patient map
Cluster-based spatial structure
Visual interpretation of similarity
🔴 6. Full Analytical Pipeline

The system evolved from:

Visualization tool → Analytical ICU intelligence system

Now supports:

Signal analysis
Similarity computation
Group discovery
Visual embedding
📊 Current Features
✔ Multi-patient signal visualization
✔ Channel selection
✔ Time-window selection (5s / 30s)
✔ DTW similarity computation
✔ Hierarchical clustering
✔ UMAP ICU map visualization
✔ Cluster-colored patient embedding
📦 Dependencies
pip install numpy pandas wfdb dash plotly scikit-learn umap-learn
🧪 Example Use Case
Select ICU patients
Choose signal (e.g., ABP)
Click Run DTW + Clustering + UMAP
System outputs:
Patient clusters
ICU similarity map
Visual grouping of physiological patterns
📌 Scientific Contribution

This project demonstrates:

Application of time-series similarity (DTW) in ICU data
Use of unsupervised clustering for patient grouping
Dimensionality reduction for medical population visualization
Integration into an interactive clinical decision-support dashboard
⚠️ Limitations (Current Stage)
DTW still computationally expensive for large datasets
No real-time streaming support yet
No clinical labeling (unsupervised only)
UMAP embedding is stochastic (minor variation possible)
🚀 Future Work
FastDTW or Soft-DTW integration
Feature-based hybrid modeling
Real-time ICU streaming support
Predictive risk scoring layer
Model validation against clinical outcomes
👨‍💻 Author

Saman Ghaderian
Master’s Student — Software Technology
HFT Stuttgart
