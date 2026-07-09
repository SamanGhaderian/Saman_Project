# ICU Multi-Patient Similarity Analysis Dashboard

## Overview

This project is an interactive ICU analytics dashboard for analyzing physiological time-series data from multiple patients.

The main goal is to discover similarities between ICU patients based on their physiological signal behavior.

The current pipeline combines:

- WFDB ICU signal loading
- Data preprocessing
- Window-based signal representation
- Dynamic Time Warping (DTW) similarity calculation
- Patient clustering
- UMAP visualization

The clustering stage was improved during development by replacing a fixed-number clustering approach with DBSCAN, which allows the algorithm to discover the number of clusters automatically.

---

# Current Pipeline

The complete workflow is:


ICU WFDB Dataset
|
|
v
cache_builder.py
|
|
v
Patient Signal Cache
(Parquet files)
|
|
v
dashboard.py
|
|
v
Load Patient Windows
|
|
v
Signal Preprocessing
|
|
v
DTW Similarity Matrix
|
|
+----------------------+
| |
v v
Hierarchical DBSCAN
Clustering Clustering
| |
+----------------------+
|
|
v
UMAP
|
|
v
2D Patient Similarity Visualization


---

# Data Caching

## cache_builder.py

The raw ICU data is stored in WFDB format.

The cache building stage:

1. Finds all available patients.
2. Reads WFDB records.
3. Extracts physiological signals.
4. Creates fixed-size windows.
5. Stores processed patient data.

Current window sizes:

```python
WINDOWS = [5, 30]

Meaning:

5-second averaged windows
30-second averaged windows

The generated cache structure:

cache/

    patient001/
        5s.parquet
        30s.parquet

    patient002/
        5s.parquet
        30s.parquet

    ...

The dashboard does not directly read WFDB files anymore.
It works only with cached data.

Patient Similarity Calculation
DTW (Dynamic Time Warping)

After selecting:

Patients
Signal channel (example: HR)
Window size

the system creates a time-series representation for each patient.

Example:

Patient 1:
[80,81,82,80,79,...]

Patient 2:
[75,77,80,82,81,...]

Because ICU signals are not perfectly synchronized, Euclidean distance is not suitable.

DTW is used because it can compare signals that have similar patterns but different timing.

The output is a distance matrix:

             P1       P2       P3

P1            0      1200     4000

P2         1200        0      2500

P3         4000      2500       0

Interpretation:

Smaller value = more similar patients
Larger value = more different patients
Previous Clustering Approach
Hierarchical Clustering

The original implementation used:

AgglomerativeClustering(
    n_clusters=3,
    metric="precomputed",
    linkage="average"
)

The input was the DTW distance matrix.

The problem:

The number of clusters was predefined.

Example:

n_clusters=3

This forces the algorithm to always create exactly three groups.

However, ICU patient data may naturally contain:

two groups
five groups
one group
no clear grouping

Therefore, forcing the number of clusters may create artificial separation.

DBSCAN Implementation
Motivation

DBSCAN was introduced to remove the requirement of defining the number of clusters beforehand.

Instead of asking:

"How many clusters should exist?"

DBSCAN asks:

"Which patients form dense similarity regions?"

The algorithm determines:

cluster membership
number of clusters
outliers/noise patients
How DBSCAN Works

DBSCAN uses two main parameters:

DBSCAN(
    eps,
    min_samples
)
eps Parameter
Definition

eps defines the maximum distance between two samples to be considered neighbors.

In this project:

Distance = DTW distance
Smaller DTW = more similar physiological behavior

Example:

eps = 1500

means:

Two patients are neighbors if:

DTW distance <= 1500
Effect of eps
Small eps

Example:

eps = 500

The algorithm becomes strict.

Result:

Only very similar patients cluster together.
Many patients become noise (-1).

Example:

Cluster 0:
5 patients

Noise:
15 patients
Large eps

Example:

eps = 5000

The algorithm becomes relaxed.

Result:

More patients become connected.
Different groups may merge.

Example:

Cluster 0:
20 patients
Medium eps

A suitable value can produce:

Cluster 0:
8 patients

Noise:
12 patients

which means:

One dense patient group was discovered.
Remaining patients do not sufficiently match this pattern.
min_samples Parameter
Definition

min_samples defines how many neighboring patients are required before a patient can be considered part of a cluster.

Example:

min_samples = 3

A patient needs at least three nearby patients within the eps radius.

Effect of min_samples
Low min_samples

Example:

min_samples = 2

Advantages:

More clusters can appear.

Disadvantages:

Small accidental groups may be detected.
High min_samples

Example:

min_samples = 10

Advantages:

Only strong patterns become clusters.

Disadvantages:

More patients become noise.
Current DBSCAN Experiment

Using:

Signal:

HR

Window:

5 seconds

Patients:

20 patients

DTW statistics:

Minimum distance: 919
Maximum distance: 18532
Mean distance: 5070
Median distance: 3670

Testing:

eps = 100

Result:

All patients classified as noise (-1)

Reason:

The eps value was too small compared with the DTW distance scale.

Testing:

eps = 3000

Result:

One large cluster

Reason:

The eps value was too large and connected most patients.

Testing:

eps = 1500
min_samples = 3

Result:

Cluster 0:
8 patients

Noise (-1):
12 patients

This represents a more meaningful DBSCAN behavior.

Automatic Parameter Selection Using K-Distance
Problem

Although DBSCAN removes the predefined number of clusters, it still requires:

eps
min_samples

Choosing these manually is not ideal.

A better approach is using a k-distance graph.

K-Distance Concept

For every patient:

Find the distance to the kth nearest patient.
Collect these distances.
Sort them.
Plot them.

The kth value is usually:

k = min_samples

Example:

If:

min_samples = 5

then:

For every patient:

Find distance to the 5th closest patient.

Example

After calculation:

Patient       5-distance

P1              1200
P2              1400
P3              1600
P4              1800
P5              7000
P6              8500
P7             10000

Sorted graph:

distance

10000 |                  *
      |
8000  |              *
      |
6000  |          *
      |
2000  |  * * * *
      |
      +--------------------
          patients

The sudden increase is the "elbow".

The elbow value is selected as:

eps
Why K-Distance Helps

Without k-distance:

Try eps values manually
       |
       |
       v
Choose a value that looks good

This is subjective.

With k-distance:

DTW Distance Matrix
        |
        |
        v
K-distance calculation
        |
        |
        v
Find elbow point
        |
        |
        v
Automatically select eps

The parameter selection becomes data-driven.

Future Improvements

Current version solved:

✅ Fixed number of clusters problem

because DBSCAN automatically determines the number of clusters.

Remaining improvements:

Implement automatic eps selection using k-distance.
Evaluate clustering quality.
Run experiments on full dataset (90 patients).
Compare:
Hierarchical clustering
DBSCAN
Analyze cluster stability.
Investigate clinical meaning of discovered groups.
Final Methodology Goal

The final pipeline should be:

ICU Signals

      |
      v

Windowing + Preprocessing

      |
      v

DTW Similarity Matrix

      |
      v

K-distance Analysis

      |
      v

DBSCAN

      |
      v

Patient Groups + Outliers

      |
      v

UMAP Visualization

This approach avoids forcing artificial clusters and allows the patient population structure to emerge from the physiological data itself.
