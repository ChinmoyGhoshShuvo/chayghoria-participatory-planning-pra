"""
Charts rebuilt from the report's tables (data/*.csv).
Mean ranks and cost totals are recomputed from the listed values, which corrects two
arithmetic slips in the report (funding mean 3.00 -> 2.82; total cost, see README).
Run:  python make_figures.py   -> PNGs in ../images/
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).parent
DATA, OUT = HERE / "data", HERE.parent / "images"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9, "axes.titlesize": 10, "axes.titleweight": "bold",
    "axes.spines.top": False, "axes.spines.right": False, "savefig.dpi": 200,
    "savefig.bbox": "tight", "figure.facecolor": "white",
})


def ranking():
    d = pd.read_csv(DATA / "problem_ranking.csv", comment="#").set_index("respondent")
    means = d.mean().sort_values()  # lower = more problematic
    fig, ax = plt.subplots(figsize=(6.0, 2.8))
    rng = np.random.default_rng(1)
    for y, prob in enumerate(means.index):
        vals = d[prob].values
        ax.scatter(vals + rng.uniform(-0.08, 0.08, len(vals)), y + rng.uniform(-0.18, 0.18, len(vals)),
                   s=14, color="#999999", alpha=0.8, zorder=1, label="Individual rank" if y == 0 else None)
        ax.scatter(means[prob], y, marker="D", s=46, color="#D55E00", zorder=3,
                   label="Mean rank" if y == 0 else None)
        ax.text(means[prob], y + 0.3, f"{means[prob]:.2f}", ha="center", fontsize=7.5, color="#D55E00")
    ax.set_yticks(range(len(means)))
    ax.set_yticklabels(means.index)
    ax.invert_yaxis()
    ax.set_xticks([1, 2, 3, 4])
    ax.set_xticklabels(["1\nmost", "2", "3", "4\nnot a problem"])
    ax.set_xlim(0.6, 4.4)
    ax.set_xlabel("Rank given by residents (n = 11)")
    ax.set_title("Flooding ranked the most pressing problem", loc="left", pad=16)
    ax.legend(frameon=False, fontsize=7, loc="lower right", bbox_to_anchor=(1.0, 1.0), ncol=2)
    fig.text(0, -0.1, "Rebuilt from report Table 5; means recomputed from the 11 responses.", fontsize=7, color="#555")
    fig.savefig(OUT / "problem-ranking-by-residents.png")
    plt.close(fig)


def cost():
    d = pd.read_csv(DATA / "drainage_cost.csv", comment="#")
    g = d.groupby("group").cost_bdt.sum().sort_values()
    total = g.sum()
    fig, ax = plt.subplots(figsize=(5.8, 2.4))
    ax.barh(g.index, g.values / 1e5, color="#0072B2", height=0.6)
    for y, v in enumerate(g.values):
        ax.text(v / 1e5 + 0.4, y, f"{v / 1e5:.2f} lakh ({v / total * 100:.0f}%)", va="center", fontsize=7.5)
    ax.set_xlim(0, 42)
    ax.set_xlabel("Cost (lakh BDT)")
    ax.set_title(f"5.3 km drainage proposal: line items total {total / 1e5:.2f} lakh BDT", loc="left")
    fig.text(0, -0.12, "Rebuilt from report Tables 6-8 (equipment rent counted once, as listed).",
             fontsize=7, color="#555")
    fig.savefig(OUT / "drainage-proposal-cost-breakdown.png")
    plt.close(fig)


if __name__ == "__main__":
    ranking()
    cost()
    print("written to", OUT.resolve())
