# Welding Sequence Analysis

This repository was developed as part of the **Data Science 2** course at **Hochschule Hannover (University of Applied Sciences and Arts)**.

## Overview

The dataset consists of **14** daily Parquet files containing **63** features. The objective of this project is to identify patterns and similarities between welding sequences using dimensionality reduction and unsupervised clustering.

Consecutive time intervals during which the `Schweißen EIN` (welding ON) signal is active are grouped into individual welding sequences, resulting in **383** sequences.

## Data overview

Each Parquet file holds one day of machine data (timestamp resolution: milliseconds). Column names follow the pattern `[<PLC id>:<index>] <German description> (<PLC address>)`. The columns are grouped below with English translations. `Schweißen EIN` is the signal used to cut the recording into sequences. It is not used as a feature.

| Group | Columns | Type | Examples (German → English) |
|---|---|---|---|
| Time | 1 | timestamp | `Time` → timestamp |
| Supply / welding electrical | 8 | float | `Einspeisung L1 Strom Istwert` → supply L1 current (actual) |
| Welding current control | ~20 | float | `Schweißstromregelung: Reglerausgang` → welding current control: controller output |
| Smoothing pressure control | ~7 | float | `Glättdruckregelung: Druckistwert Glättrollen` → smoothing pressure control: actual pressure of smoothing rollers |
| Table adjustment | ~10 | float | `Tischverstellung Überlapptisch Überlappung Istwert` → overlap table adjustment: overlap (actual) |
| Strip / material data | 8 | float | `Dicke Band Einlauf` → strip thickness (inlet) |
| Pressure / hydraulics | ~6 | float | `Istwert Luftdruck am Schweißrollenzylinder` → actual air pressure at the welding roller cylinder |
| Setpoints (HMI) | 4 | float | `MP377: Schweißkraft Sollwert` → HMI: welding force setpoint |
| Drive | 2 | float | `Antrieb C-Wagen Istposition in mm` → C-carriage drive actual position (mm) |
| Binary signals | 7 | bool | `Schweißen EIN` → welding ON |

The group sizes marked `~` are approximate. The exact list is available in the notebook via `schema`.

### German–English glossary

| German | English |
|---|---|
| Schweißen / Schweißmaschine | welding / welding machine |
| Schweißen EIN | welding ON |
| Schweißstrom | welding current |
| Schweißspannung | welding voltage |
| Schweißkraft | welding force |
| Schweißgeschwindigkeit | welding speed |
| Schweißrolle(n) / Schweißrollendruck | welding roller(s) / welding roller pressure |
| Einspeisung | supply (mains feed) |
| Strom / Spannung | current / voltage |
| Istwert | actual value |
| Sollwert | setpoint (target value) |
| Grundsollwert | base setpoint |
| skaliert / normiert | scaled / normalised |
| Regler / Reglerausgang | controller / controller output |
| Reglerdifferenz | control error (setpoint minus actual) |
| Reglerfreigabe | controller enable |
| I-Anteil / P-Anteil | integral / proportional component |
| Schweißstromregelung | welding current control |
| Glättrolle / Glättkraft | smoothing roller / smoothing force |
| Glättdruckregelung | smoothing pressure control |
| Druck / Luftdruck | pressure / air pressure |
| Druckregelventil / Prop_-Ventil | pressure control valve / proportional valve |
| Netz | (air) supply network |
| Stromschiene oben | busbar, top |
| Temperatur Start Schweißen | temperature at start of welding |
| Shunt / HKS | shunt / HKS (measurement point of the secondary circuit, as labelled in the data) |
| Zuführung / Rückführung | feed / return |
| Differenz | difference |
| Antrieb | drive |
| C-Wagen | C-carriage |
| Istposition | actual position |
| V-Ist | actual velocity |
| Tischverstellung | table adjustment |
| Überlapptisch / Kipptisch | overlap table / tilting table |
| Ausspannlänge | free clamping length (stick-out) |
| Überlappung | overlap |
| Schränkung | offset (lateral misalignment of strip edges) |
| Hydraulikzylinder Kolbenseite / Flächenseite | hydraulic cylinder, piston side / cap side |
| Druckmessung | pressure measurement |
| Band Einlauf / Auslauf | strip inlet / outlet |
| Dicke / Breite | thickness / width |
| Materialnummer | material number |
| Kohlenstoffgehalt | carbon content |
| ist unten / ist auf / ist ab | is down / is on / is off |
| Softwareschalter | software switch |
| Geschweißt Relais | "welded" relay |
| Glaettrolle ist auf SBE / ab SE | smoothing roller is at strip start (SBE) / at strip end (SE) |

Some translations (`HKS`, `Schränkung`, `SBE`/`SE`) are my best interpretation and should be checked against the machine documentation.

## Methodology

1. **Sequence extraction**: Identify welding sequences using the binary `Schweißen EIN`  signal. Consecutive active intervals are treated as one continuous welding sequence.
2. **Standardisation**: Apply z-score standardisation to all numerical features and remove constant features. 
3. **Common representation**: Resample each welding sequence using linear interpolation to obtain a fixed-length representation of (N = 300) equidistant time points.
4. **Dimensionality reduction**: Apply Principal Component Analysis (PCA) to the resulting data. Retain enough principal components to explain at least **95%** of the total variance, resulting in **160** components.
5. **Clustering**: K-Means on the reduced data. The elbow method estimates `k`, and `k = 2, 3, 4` are compared.
6. **Non-linear embedding**: Apply t-SNE (`perplexity = 30`) and UMAP (`n_neighbors = 15`, `min_dist = 0.1`) to the PCA-reduced data and colour the points with the K-Means clusters (`k = 3`) for comparison with the PCA projection.
7. **Inspection**: Examine the original and interpolated signals of the nearest and farthest sequence pairs in PCA space, as well as a potential outlier.

## Results

### Dimensionality reduction

160 principal components are needed to explain at least 95% of the total variance of the 383 resampled sequences, so the variance is spread over many components. Projected onto PC1 and PC2, the sequences form two well-separated groups (PC1 < 0 and PC1 > 0). The right-hand group has more internal structure and splits into an upper and a lower part along PC2.

| Cumulative explained variance | Sequences in PC1 / PC2 |
|---|---|
| ![Cumulative explained variance](assets/pca_cumulative_variance.png) | ![PCA 2D projection](assets/pca_2d.png) |

### Clustering

K-Means (`n_init = 50`) was fitted on the 160 principal components. The plots below show the clusters in the PC1 / PC2 plane.

**Elbow method.** The inertia drops sharply from k = 1 to k = 2 (to about 66% of the k = 1 value) and flattens out after k = 3 (about 58%). There is no pronounced elbow beyond k = 2, so the data does not indicate a single clearly correct `k`.

![Elbow plot](assets/elbow.png)

**Comparison of k = 2, 3, 4.**

| k | What the clusters capture |
|---|---|
| 2 | Separates the left group (PC1 < 0) from the right group (PC1 > 0). This matches the main structure in the PCA plot. |
| 3 | Splits the right group into an upper and a lower cluster along PC2. The left group stays intact. |
| 4 | Additionally splits the left group into two clusters. These are less clearly separated than the other splits. |

![K-Means clusters for k = 2, 3, 4](assets/kmeans_clusters.png)

`k = 2` is the most clearly supported split. `k = 3` adds a split that is also visible in the PCA plot. `k = 4` mainly divides a group that looks continuous.

### Inspection of selected sequences

Sequences were selected in the PC1 / PC2 plane:

- **Nearest pair**: the two sequences with the smallest distance.
- **Farthest pair**: the two sequences with the largest distance.
- **Outlier**: the sequence with the largest mean distance to its four nearest neighbours.

![Selected sequences in PCA space](assets/pca_nearest_farthest_outlier.png)

| Case | Observation |
|------|-------------|
| Nearest pair | Very similar signal shapes, so proximity in PCA space matches similarity in the raw time series. |
| Farthest pair | Clearly different signal height and duration. |
| Outlier | Hardly any difference in the inspected feature. Its position is probably driven by other features, which would have to be examined to confirm this. |

Nearest pair:

![Nearest pair](assets/seq_nearest.png)

Farthest pair:

![Farthest pair](assets/seq_farthest.png)

Outlier:

![Outlier](assets/seq_outlier.png)

### Conclusions

- The welding sequences fall into two main groups in PCA space. A third cluster, splitting the right group, is also supported by the plot.
- The elbow plot shows no sharp elbow beyond k = 2, so the choice of `k` is partly a judgement call.
- Distances in PCA space reflect real differences in the original signals, as the nearest and farthest pairs show.
- The outlier is not explained by the single feature inspected, so a multi-feature comparison is needed.

### Limitations and next steps

- Only one feature was plotted for the inspected pairs. The clusters are not yet interpreted in terms of welding parameters.
- Cluster quality was judged visually and with the elbow method. Silhouette or Davies-Bouldin scores would give a more objective comparison of `k`.
- Possible extensions: cluster-mean signal profiles, PCA loadings to find the features that drive PC1 and PC2, and a check of the clusters against the recording day.
