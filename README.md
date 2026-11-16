# Springmass

Mass–spring equilibrium data and its reduction.

- `data/equilibrium/<sample>/positionvssample.txt` — raw motion-sensor exports (time, distance, distance error) for the unstretched length and the 100 g, 201 g and 301 g masses.
- `springmass.py` — helpers to read the files and average each run (using `np.loadtxt`), with the error combined in quadrature: `np.sqrt(std**2 + err_mean**2)`.
- `data_reduction.ipynb` — the JupyterLab notebook that does the reduction.

```bash
pip install -r requirements.txt
jupyter lab
```
