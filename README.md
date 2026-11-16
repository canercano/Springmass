# Springmass

Mass–spring equilibrium data and its reduction.

- `data100.txt`, `data201.txt`, `data301.txt` — sensor data (time, distance, distance error) for the 100 g, 201 g and 301 g masses.
- `data_reduction.ipynb` — reads the files with `np.loadtxt`, averages them and propagates the error with `np.sqrt(std**2 + err_mean**2)`.

