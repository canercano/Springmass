"""Helpers for reading and reducing the mass-spring position-vs-time data.

The data files are exported from the motion sensor software. Each one has a
few title/date lines (the number varies between files), then a tab-separated
header line starting with "Time (s)", then the data columns:

    Time (s)    Distance (cm)    Dist Error (cm)
"""
from pathlib import Path

import numpy as np
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent / "data"


def read_run(path):
    """Read one positionvssample.txt file into a DataFrame.

    Columns are renamed to: time_s, dist_cm, dist_err_cm.
    """
    path = Path(path)
    lines = path.read_text().splitlines()
    # Find the column-header line, since the number of title lines varies.
    header_row = next(i for i, line in enumerate(lines) if line.startswith("Time"))
    df = pd.read_csv(path, sep="\t", skiprows=header_row)
    df.columns = ["time_s", "dist_cm", "dist_err_cm"]
    return df


def load_all(folder="equilibrium"):
    """Read every sample folder under data/<folder>/ into a dict {name: DataFrame}."""
    runs = {}
    for f in sorted((DATA_DIR / folder).glob("*/positionvssample.txt")):
        runs[f.parent.name] = read_run(f)
    return runs


def average_run(df):
    """Average one run and propagate the error in quadrature.

    mean  = mean of the distance readings
    std   = sample standard deviation of the readings (ddof=1)
    err   = mean of the per-point sensor error
    total = sqrt(std**2 + err**2)
    """
    mean = df["dist_cm"].mean()
    std = df["dist_cm"].std(ddof=1)
    err_mean = df["dist_err_cm"].mean()
    total = np.sqrt(std**2 + err_mean**2)
    return {
        "n": len(df),
        "mean_cm": mean,
        "std_cm": std,
        "err_mean_cm": err_mean,
        "total_err_cm": total,
    }


def summarize(runs):
    """Return a summary table with one row per sample."""
    return pd.DataFrame({name: average_run(df) for name, df in runs.items()}).T
