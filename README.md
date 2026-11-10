# Welding Sequence Analysis

This repository was developed as part of the **Data Science 2** course at **Hochschule Hannover (University of Applied Sciences and Arts)**.

## Overview

The dataset consists of **14** daily Parquet files containing **63** features. The objective of this project is to identify patterns and similarities between welding sequences using dimensionality reduction and unsupervised clustering.

Consecutive time intervals during which the `Schweißen EIN` (welding ON) signal is active are grouped into individual welding sequences, resulting in **383** sequences.

First 10 rows of `lf.head(10).collect()`:

| Time                    |   L1 Strom |   L1 Spannung |   Schweißstrom |   Schweißspannung |   Schweißkraft Soll |   Geschw. Soll |   C-Wagen V-Ist | Schweißen EIN   |
|:------------------------|-----------:|--------------:|---------------:|------------------:|--------------------:|---------------:|----------------:|:----------------|
| 2026-08-31 00:06:30.906 |      -0.11 |       -591.06 |           0.02 |            699.98 |                  22 |             40 |               0 | False           |
| 2026-08-31 00:06:30.907 |       0.02 |       -704.71 |           0.02 |            580.71 |                  22 |             40 |               0 | False           |
| 2026-08-31 00:06:30.908 |      -0.11 |       -751.09 |           0.02 |            404.32 |                  22 |             40 |               0 | False           |
| 2026-08-31 00:06:30.909 |       0.02 |       -720.58 |           0.02 |            184.1  |                  22 |             40 |               0 | False           |
| 2026-08-31 00:06:30.910 |       0.02 |       -624.87 |           0.02 |            -47.35 |                  22 |             40 |               0 | False           |
| 2026-08-31 00:06:30.911 |       0.02 |       -464.1  |           0.02 |           -277.82 |                  22 |             40 |               0 | False           |
| 2026-08-31 00:06:30.912 |       0.02 |       -260.85 |           0.02 |           -479.12 |                  22 |             40 |               0 | False           |
| 2026-08-31 00:06:30.913 |       0.02 |        -29.53 |           0.02 |           -638.79 |                  22 |             40 |               0 | False           |
| 2026-08-31 00:06:30.914 |       0.02 |        201.68 |           0.02 |           -729.61 |                  22 |             40 |               0 | False           |
| 2026-08-31 00:06:30.915 |       0.02 |        410.67 |           0.01 |           -752.56 |                  22 |             40 |               0 | False           |

## Methodology

1. **Sequence extraction**: Identify welding sequences using the binary `Schweißen EIN`  signal. Consecutive active intervals are treated as one continuous welding sequence.
2. **Standardisation**: Apply z-score standardisation to all numerical features and remove constant features.
3. **Common representation**: Resample each welding sequence using linear interpolation to obtain a fixed-length representation of (N = 300) equidistant time points.
4. **Dimensionality reduction**: Apply Principal Component Analysis (PCA) to the resulting data. Retain enough principal components to explain at least **95%** of the total variance, resulting in **160** components.
5. **Clustering**: K-Means on the reduced data. The elbow method estimates `k`, and `k = 2, 3, 4` are compared.
6. **Non-linear embedding**: Apply t-SNE (`perplexity = 30`) and UMAP (`n_neighbors = 15`, `min_dist = 0.1`) to the PCA-reduced data and colour the points with the K-Means clusters (`k = 3`) for comparison with the PCA projection.
7. **Comparison of clustering methods**: Hierarchical clustering (Ward linkage) and DBSCAN (`eps` from the k-distance plot) are compared with K-Means using the adjusted Rand index and silhouette score.
8. **Inspection**: Examine the original and interpolated signals of the nearest and farthest sequence pairs in PCA space, as well as a potential outlier.
