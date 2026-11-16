"""Helpers for reading and reducing the mass-spring position-vs-time data.

Each data file has a few title/date lines (2 or 3, it varies), then a
header line starting with "Time (s)", then three tab-separated columns:

    Time (s)    Distance (cm)    Dist Error (cm)
"""
from pathlib import Path

import numpy as np

DATA_DIR = Path(__file__).resolve().parent / "data"


def count_header_lines(path):
    """Number of lines up to and including the 'Time (s)' column-header line."""
    with open(path) as f:
        for i, line in enumerate(f):
            if line.startswith("Time"):
                return i + 1
    raise ValueError(f"No 'Time' header line found in {path}")


def read_run(path):
    """Read one file with np.loadtxt. Returns (time_s, dist_cm, dist_err_cm) arrays."""
    time, dist, dist_err = np.loadtxt(
        path, delimiter="\t", skiprows=count_header_lines(path), unpack=True
    )
    return time, dist, dist_err


def load_all(folder="equilibrium"):
    """Read every sample under data/<folder>/ into {name: {"time", "dist", "dist_err"}}."""
    runs = {}
    for f in sorted((DATA_DIR / folder).glob("*/positionvssample.txt")):
        time, dist, dist_err = read_run(f)
        runs[f.parent.name] = {"time": time, "dist": dist, "dist_err": dist_err}
    return runs


def equilibrium(dist, dist_err):
    """Mean equilibrium position and its uncertainty.

    std   = sample standard deviation of the readings (ddof=1)
    err   = mean of the per-point sensor error
    sigma = sqrt(std**2 + err**2)
    """
    mean = np.mean(dist)
    std = np.std(dist, ddof=1)
    err_mean = np.mean(dist_err)
    sigma = np.sqrt(std**2 + err_mean**2)
    return mean, std, err_mean, sigma
