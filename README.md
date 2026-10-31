# Welding Sequence Analysis

This repository was developed as part of the **Data Science 2** course at **Hochschule Hannover (University of Applied Sciences and Arts)**.

## Overview

The dataset contains **63 features** in 14 daily Parquet files. Contiguous periods where the signal *Schweißen EIN* (welding ON) is active are treated as one welding sequence, which gives **383 sequences**.

## What was done

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

### Installation

```bash
git clone <repo-url>
cd WeldingSequenceAnalysis
python -m venv .venv && source .venv/bin/activate
pip install polars numpy pandas scikit-learn matplotlib plotly jupyter
```

### Data

The raw files are not versioned (`data/` is git-ignored). Place them in `data/` using the naming pattern `EV__<date>_..._de_compressed_without_label.parquet`.

### Usage

```bash
jupyter lab main.ipynb
```

Run the cells top to bottom. The raw data is read lazily with Polars, so the full dataset never has to fit in memory.
## Reproducibility

K-Means uses `random_state=0`. Results can still vary slightly with library versions. Consider pinning them in a `requirements.txt`.

## Tech Stack

Polars · NumPy · pandas · scikit-learn · Matplotlib · Plotly

