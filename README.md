# Welding Sequence Analysis

This repository was developed as part of the **Data Science 2** course at **Hochschule Hannover (University of Applied Sciences and Arts)**.

## Overview

The dataset consists of **14** daily Parquet files containing **63** features. The objective of this project is to identify patterns and similarities between welding sequences using dimensionality reduction and unsupervised clustering.

Consecutive time intervals during which the `Schweißen EIN` (welding ON) signal is active are grouped into individual welding sequences, resulting in **383** sequences.

## Methodology

1. **Sequence extraction**: Identify welding sequences using the binary `Schweißen EIN`  signal. Consecutive active intervals are treated as one continuous welding sequence.
2. **Standardisation**: Apply z-score standardisation to all numerical features and remove constant features. 
3. **Common representation**: Resample each welding sequence using linear interpolation to obtain a fixed-length representation of (N = 300) equidistant time points.
4. **Dimensionality reduction**: Apply Principal Component Analysis (PCA) to the resulting data. Retain enough principal components to explain at least **95%** of the total variance, resulting in **160** components.
5. **Clustering**: K-Means on the reduced data. The elbow method estimates `k`, and `k = 2, 3, 4` are compared.
6. **Inspection**: Examine the original and interpolated signals of the nearest and farthest sequence pairs in PCA space, as well as a potential outlier.

## Results

