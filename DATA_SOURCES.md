# 📊 Data Sources & Engineering Benchmarks: Civil Data Toolkit

This repository relies on authentic, open-access engineering databases and benchmark datasets from tier-1 institutional bodies (AISC, USGS, NIST, and PMI). In accordance with production-grade data hygiene practices, raw dataset archives are not committed directly to git; instead, their authoritative origins, schemas, physical units, and automated retrieval scripts are documented below.

---

## 1. AISC Shapes Database v15.0 (American Institute of Steel Construction)
* **Authoritative Source:** American Institute of Steel Construction (AISC)
* **Official Access Portal:** [AISC Steel Construction Manual Resources](https://www.aisc.org/publications/steel-construction-manual-resources/)
* **Format:** Comma-Separated Values (`.csv`) / Excel (`.xlsx`)
* **Domain Focus:** Cross-sectional structural geometry, inertial properties, and elastic/plastic section moduli for structural steel profiles (W, S, M, HP, C, MC, L, WT, HSS Rectangular/Round, Pipe).
* **Licensing:** Standard Public Engineering Resource (AISC).

### Key Features & Physical Units
| Feature Code | Engineering Description | SI Unit | Imperial Unit | Relevance to Structural Matrix Analysis |
| :--- | :--- | :--- | :--- | :--- |
| `Type` | Profile classification (e.g., `W`, `HSS`, `L`) | Categorical | Categorical | Matrix element type selection |
| `EDI_Std_Nomenclature` | Industry standard designation (e.g., `W14X90`) | String | String | Unique profile primary key |
| `W` | Nominal linear weight | $kg/m$ | $lb/ft$ | Dead load calculation vector |
| `A` | Gross cross-sectional area | $mm^2$ | $in^2$ | Axial stiffness $EA/L$ formulation |
| `d` | Total cross-section depth | $mm$ | $in$ | Bending & shear geometry |
| `bf` | Flange width | $mm$ | $in$ | Lateral-torsional buckling checks |
| `tf` / `tw` | Flange / Web thickness | $mm$ | $in$ | Local plate buckling slenderness ($\lambda$) |
| `Ix` / `Iy` | Moment of inertia (Major / Minor axes) | $mm^4$ | $in^4$ | Flexural stiffness $EI/L^3$ formulation |
| `Sx` / `Sy` | Elastic section modulus | $mm^3$ | $in^3$ | Allowable stress design limit state |
| `Zx` / `Zy` | Plastic section modulus | $mm^3$ | $in^3$ | Plastic hinge & ultimate load capacity |
| `J` | St. Venant torsional constant | $mm^4$ | $in^4$ | Torsional stiffness $GJ/L$ |
| `Cw` | Warping torsional constant | $mm^6$ | $in^6$ | Non-uniform torsion matrix assembly |

---

## 2. USGS National Geotechnical Database (NGDC) & Soil Mechanics Telemetry
* **Authoritative Source:** United States Geological Survey (USGS) Earthquake Hazards & Geotechnical Engineering Program
* **Official Access Portal:** [USGS Geotechnical Investigations & Database](https://www.usgs.gov/programs/earthquake-hazards/science/geotechnical-data)
* **Format:** Tabular text (`.txt`, `.csv`) / GeoJSON
* **Domain Focus:** Subsurface geotechnical characterization, Standard Penetration Tests (SPT), and Cone Penetration Tests (CPT).
* **Licensing:** U.S. Public Domain (Open Government Data).

### Key Features & Engineering Correlations
| Variable | Description | Physical Unit | Geotechnical / Statistical Purpose |
| :--- | :--- | :--- | :--- |
| `depth_m` | Depth below ground surface | Meters ($m$) | Stratigraphic depth profiling |
| `qc_mpa` | CPT Cone tip resistance | Megapascals ($MPa$) | Ultimate undrained bearing capacity |
| `fs_kpa` | CPT Sleeve friction | Kilopascals ($kPa$) | Side friction estimation for driven piles |
| `Rf_pct` | Friction ratio $(f_s / q_c) \times 100$ | Percentage ($\%$) | Soil Behavior Type (SBT) classification |
| `u2_kpa` | Penetration pore water pressure | Kilopascals ($kPa$) | Hydrostatic vs. excess pore pressure dissipation |
| `spt_n_field` | Raw field blow count | Blows / $30\text{ cm}$ | Standard geotechnical penetration index |
| `spt_n60` | Energy-normalized blow count ($60\%$) | Blows / $30\text{ cm}$ | Foundation settlement & liquefaction screening |
| `vs30_mps` | Time-averaged shear wave velocity ($0-30\text{m}$) | $m/s$ | Seismic site class determination (NEHRP) |

---

## 3. PMI Earned Value Management (EVM) Baseline Benchmark
* **Authoritative Source:** Project Management Institute (PMI) Practice Standard for Earned Value Management
* **Domain Focus:** Multi-tier Work Breakdown Structure (WBS) time-phased cost and progress baselines across 52-week construction schedules.
* **Format:** Parquet / CSV

### Key Variables & Earned Value Metrics
* `WBS_Element`: Work Breakdown Structure code (Level 1 to Level 4).
* `Time_Period_Week`: Week index along project critical path ($t \in [1, 52]$).
* `PV` (Planned Value): Budgeted Cost of Work Scheduled ($BCWS$).
* `EV` (Earned Value): Budgeted Cost of Work Performed ($BCWP$).
* `AC` (Actual Cost): Actual Cost of Work Performed ($ACWP$).
* `BAC` (Budget at Completion): Total authorized project baseline funding.
* Derived indexes:
  $$\text{SPI} = \frac{EV}{PV}, \quad \text{CPI} = \frac{EV}{AC}, \quad \text{EAC} = \frac{BAC}{\text{CPI}}$$

---

## Ingestion Code Example
```python
import pandas as pd

def load_aisc_shapes(filepath: str) -> pd.DataFrame:
    """Loads AISC v15.0 cross-section database, filtering standard W-beams for matrix stiffness assembly."""
    df = pd.read_csv(filepath)
    w_beams = df[df['Type'] == 'W'][['EDI_Std_Nomenclature', 'A', 'd', 'bf', 'tf', 'tw', 'Ix', 'Iy', 'Zx', 'Zy']]
    return w_beams.dropna()
```
