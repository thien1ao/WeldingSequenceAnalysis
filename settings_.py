import matplotlib.pyplot as plt
from typing import NamedTuple

N_SAMPLES = 300

N_CLUSTERS = 3
MAX_NOISE = 0.2
N_BEST = 5
N_SEQ = 2
CHOSEN_CLUSTER = 0

palette = plt.get_cmap("tab10").colors
eps_list = [64, 70, 77, 84, 90, 97, 103, 110]
min_samples = [3, 5, 8, 15, 30, 45, 60, 80, 100]

ENVELOPE_SIZE = 100

class Styles(NamedTuple):
    cluster_colors: list
    chosen_color: str
    outlier_styles: list

STYLES = Styles(
    cluster_colors=["blue", "orange", "green"],
    chosen_color="black",
    outlier_styles=[("red", "--"), ("purple", "-.")],
)


