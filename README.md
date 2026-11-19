# Civil Data Toolkit
### High-Performance Computational & Analytics Utilities for Civil & Structural Engineering

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A modular Python library bridging classical civil engineering mathematics (Matrix Structural Analysis, Geotechnical Statistics, and Earned Value Management) with modern vectorized scientific computing using NumPy, SciPy, and Pandas.

```mermaid
flowchart LR
    A["Civil Data Inputs (CAD/BIM, Schedules, Lab Tests)"] --> B["civil-data-toolkit Core"]
    B --> C["structural_matrix.py (Direct Stiffness Formulation)"]
    B --> D["schedule_timeseries.py (EVM & S-Curve Interpolation)"]
    B --> E["geotech_stats.py (Material Reliability & Weibull)"]
    C --> F["Validated Engineering Outputs & DataFrames"]
    D --> F
    E --> F
```

## Key Features
- **Vectorized Matrix Stiffness Solver:** Global stiffness matrix assembly and boundary condition elimination for 2D trusses and frames with $O(N)$ sparse optimization.
- **Earned Value Management (EVM) Analytics:** Automated computation of SPI, CPI, EAC, and cubic spline interpolation of S-curves from project schedules.
- **Geotechnical & Material Reliability:** Continuous distribution modeling (Log-Normal, Weibull) for soil mechanics and concrete compressive strength datasets.

## Quickstart

```bash
git clone https://github.com/master-dev0000/civil-data-toolkit.git
cd civil-data-toolkit
pip install -r requirements.txt
pytest tests/
```

### Example: Matrix Stiffness Calculation
```python
from src.structural_matrix import Truss2D

truss = Truss2D()
truss.add_node(0, 0.0, 0.0, fix_x=True, fix_y=True)
truss.add_node(1, 4.0, 0.0, fix_x=False, fix_y=True)
truss.add_node(2, 2.0, 3.0, fix_x=False, fix_y=False)

# E = 200 GPa, Area = 0.0025 m2
truss.add_member(0, 1, E=200e9, A=0.0025)
truss.add_member(1, 2, E=200e9, A=0.0025)
truss.add_member(0, 2, E=200e9, A=0.0025)

truss.add_load(node_id=2, fx=0.0, fy=-50000.0)
results = truss.solve()
print(results['displacements'])
```

## License
MIT License. Developed by André Belarmino Alves.
