# Welding Sequence Analysis: Clustering Multivariate Time Series

Unsupervised analysis of industrial resistance-welding data. Each welding cycle is extracted from raw machine signals, normalised to a common length, reduced with PCA and grouped with K-Means to find typical and atypical welds.

## Overview

A steel-strip line joins the end of one strip to the start of the next. The strips overlap and are clamped by hydraulic cylinders, while a welding tool on a C-carriage travels across the strip. Once the carriage reaches welding speed (137 mm/s), the current controller is enabled and the welding current is switched on.

The dataset contains **63 features** (about **1.08 billion rows**) in 14 daily Parquet files. Contiguous periods where the signal *Schweißen EIN* (welding ON) is active are treated as one welding sequence, which gives **383 sequences**.

| Feature group | Examples |
|---|---|
| Current / voltage | Welding current (setpoint and actual), voltage, mains supply L1–L3 |
| C-carriage | Position and velocity |
| Binary states | Welding ON, welding roller down |
| Strip data | Thickness, width, material, carbon content |
| Pressure / force | Welding roller, smoothing roller, hydraulic pressure at the overlap table |

## Method

1. **Sequence extraction**: detect welding sequences from the binary *Welding ON* signal.
2. **Standardisation**: z-score every numeric feature and drop constant features.
3. **Common representation**: linearly interpolate each sequence onto `N = 300` equidistant time points, giving one row per sequence.
4. **Dimensionality reduction**: PCA, keeping the components that explain at least 95 % of the variance (160 components).
5. **Clustering**: K-Means on the reduced data. The elbow method estimates `k`, and `k = 2, 3, 4` are compared.
6. **Inspection**: compare original and interpolated signals for the nearest pair, the farthest pair and a likely outlier in PCA space.

## Results

- Sequences that are close in PCA space show similar signal curves.
- The most distant pair differs clearly in signal height and duration.
- The detected outlier is hardly distinguishable in the inspected feature, so its position is probably driven by other features. Inspecting more features is future work.

![Example welding sequence](Images/seq2_cwagen_stromregelung.png)

*Sequence 2: the grey area marks the controller enable, during which current flows.*

## Project Structure

```
.
├── M1.ipynb             # Exploration of the data and the welding process
├── M1_Bericht.ipynb     # Report M1: process description and features
├── M2.ipynb             # Pipeline: interpolation, PCA, K-Means, inspection
├── M2_Bericht.ipynb     # Report M2: methodology and findings
├── plot_seq2.py         # Script for the example-sequence figure
├── data/                # Parquet files (git-ignored, see below)
├── Images/              # Figures used in the reports
└── note.txt             # Lecture notes (K-Means, elbow, silhouette)
```

## Getting Started

### Prerequisites

- Python 3.10+
- Jupyter

### Installation

```bash
git clone <repo-url>
cd ds2
python -m venv .venv && source .venv/bin/activate
pip install polars numpy pandas scikit-learn matplotlib plotly jupyter
```

### Data

The raw files are not versioned (`*.parquet` is git-ignored). Place them in `data/` using the naming pattern `EV__<date>_..._de_compressed_without_label.parquet`.

### Usage

```bash
jupyter lab M2.ipynb
```

Run the cells top to bottom. The raw data is read lazily with Polars, so the full dataset never has to fit in memory. To regenerate the example figure:

```bash
python plot_seq2.py
```

## Reproducibility

K-Means uses `random_state=0`. Results can still vary slightly with library versions. Consider pinning them in a `requirements.txt`.

## Tech Stack

Polars · NumPy · pandas · scikit-learn · Matplotlib · Plotly

