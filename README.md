# ICU Dashboard Project — Version 0.0.1: Multi-Resolution Pipeline

## Project Overview

This project is an ICU patient monitoring dashboard built using WFDB physiological signal data and Python.

The goal of the system is to:

* Load and process multi-patient ICU waveform data
* Visualize physiological signals interactively
* Build a scalable monitoring dashboard using Plotly Dash
* Support future patient metrics and status monitoring

The dataset contains segmented ICU recordings with multiple physiological signals such as ECG, ABP, PLETH, and RESP.

---

# Current Project Status

Current Version:

```text
v0.0.1-multi-resolution
```

Completed phases:

* ✅ Data understanding
* ✅ Dataset verification
* ✅ WFDB loading pipeline
* ✅ Multi-record patient merging
* ✅ Multi-resolution preprocessing pipeline

Pending phases:

* ⏳ Time continuity correction
* ⏳ Dash UI integration
* ⏳ Interactive visualization
* ⏳ Metrics panel
* ⏳ Patient status indicators

---

# Dataset Structure

The dataset is organized as:

```text
sample/
│
├── 252/
│   ├── 25200001.dat
│   ├── 25200001.hea
│   ├── 25200002.dat
│   ├── 25200002.hea
│   └── ...
│
├── 256/
└── ...
```

Each patient folder contains multiple segmented WFDB records.

Special files such as:

```text
252n.dat
252n.hea
```

were detected and excluded from processing because their signal structure differs from normal ICU segments.

---

# Dataset Verification Results

The following checks were completed:

## File Integrity

* Verified `.dat` and `.hea` file structure
* Verified segmented patient organization
* Detected known special-case records (`*n`)

## Signal Consistency

Most segmented records contain the same signal set:

```text
MCL1
II
V
ABP
PLETH
RESP
```

## Sampling Frequency

Verified sampling rate:

```text
125 Hz
```

Equivalent sampling interval:

```text
0.008 seconds
```

## Segment Duration

Typical segment structure:

```text
75000 samples
125 Hz
600 seconds (10 minutes)
```

## Record Ordering

Verified correct sequential ordering:

```text
25200001
25200002
25200003
...
```

---

# Current Data Pipeline

The project currently implements a multi-resolution signal pipeline.

## Pipeline Architecture

```text
WFDB Records
      ↓
RAW Layer (125 Hz)
      ↓
5-Second Layer
      ↓
30-Second Summary Layer
```

---

# RAW Layer

Purpose:

* Preserve full physiological signal detail
* Maintain original ICU waveform resolution
* Support future detailed analysis and zooming

Characteristics:

* Full 125 Hz sampling rate
* Millions of samples per patient
* Stored as Pandas DataFrame

Example structure:

```text
time | MCL1 | II | V | ABP | PLETH | RESP
```

---

# 5-Second Layer

Purpose:

* Lightweight visualization
* Faster dashboard rendering
* Reduced plotting overhead

Method:

* Resampling every 5 seconds
* Mean aggregation

Benefits:

* Much smaller dataset
* Dash-friendly plotting
* Preserves general trends

---

# 30-Second Summary Layer

Purpose:

* Dashboard metrics
* Trend monitoring
* Future patient condition indicators

Method:

* Resampling every 30 seconds
* Statistical aggregation:

  * mean
  * min
  * max

Example output:

```text
ABP_mean
ABP_min
ABP_max
```

---

# Current Python Components

## Record Discovery

Implemented:

* Automatic record scanning
* Exclusion of invalid/noisy records
* Sequential sorting

## WFDB Loader

Implemented:

* WFDB record reading using `wfdb.rdrecord`
* Signal extraction
* Sampling frequency extraction
* Time vector generation

## Multi-Record Patient Loader

Implemented:

* Sequential loading of all valid records
* DataFrame conversion
* Concatenation into full patient dataset

## Resampling System

Implemented:

* 5-second aggregation layer
* 30-second summary layer
* Pandas time-based resampling

---

# Current Limitations

The following items are intentionally postponed for the next version.

## Time Continuity Correction

Current issue:

Each segmented record starts its internal time axis from zero.

Next version will:

* Apply cumulative time offsets
* Create one fully continuous patient timeline

---

## Performance Optimization

Current limitation:

Data is reloaded from WFDB files every execution.

Planned improvements:

* Caching
* Pickle storage
* Faster patient loading

---

## Dashboard UI

Not implemented yet.

Planned features:

* Plotly Dash integration
* Patient selection
* Interactive graphs
* Zooming and panning
* Multi-signal display

---

# Planned Next Phase

Next branch/version:

```text
v0.0.2-time-continuity
```

Goals:

* Fix segmented timeline continuity
* Add cumulative time offsets
* Validate merged patient duration
* Prepare final backend for Dash integration

---

# Technologies Used

## Python Libraries

* Python
* Pandas
* NumPy
* WFDB
* Plotly Dash (planned)

---

# Project Vision

Final system goals:

1. Select ICU patient
2. Visualize synchronized physiological signals
3. Navigate long recordings efficiently
4. Display patient metrics
5. Indicate patient condition state

---

# Repository Workflow

Development strategy:

* One Git branch per major milestone
* README updates per version
* Structured incremental development

Current branch:

```text
v0.0.1-multi-resolution
```

---

# Author

Saman Ghaderian

Master's Student — Software Technology
HFT Stuttgart
