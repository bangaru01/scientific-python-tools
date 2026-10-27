# Scientific Python Tools — review draft

Notebook collection for manipulating molecular geometries and preparing small computational-chemistry analyses. Organized from previously mixed Google Colab uploads. **Status: curated but not scientifically validated.**

## Gaussian file conversion

| Notebook | Intended task | Current limitation |
|---|---|---|
| `gaussian-file-conversion/input_orientation_log_to_xyz.ipynb` | Extract input-orientation geometries from Gaussian log files | Contains two related implementations; further consolidation needed |
| `gaussian-file-conversion/log_to_xyz_with_energy.ipynb` | Extract geometry from Gaussian logs, with energy-aware selection | Requires adapted Google Drive paths and a real-log regression test |
| `gaussian-file-conversion/xyz_or_log_to_gjf.ipynb` | Produce Gaussian input from XYZ or log structures | Multiple cells specify distinct modes; method/charge/multiplicity must be checked |

## Molecular steric descriptors

| Notebook | Task | Warning |
|---|---|---|
| `molecular-sterics/steric_descriptors.py` | Rewritten stand-alone buried-volume and cone-angle calculator from XYZ | Requires explicit 1-based ligand indices, Morfeus runtime and scientific validation; includes mock unit tests |

## Reaction preparation

- `reaction-preparation/reagent_calculator_pubchem.ipynb`: example PubChem-based molar-mass lookup and reagent-quantity spreadsheet; uses network lookups and example inputs. Not a validated synthesis instruction.

## Typical requirements
- Python 3 / Jupyter or Google Colab
- `numpy`, `pandas`, `openpyxl`, `morfeus-ml`, `pubchempy` depending on notebook
- Input XYZ/Gaussian files, atom numbering and working directories appropriate to each script

## Before reuse

1. Read the first Markdown cell, then inspect original code for Colab (`/content/drive/MyDrive`) paths.
2. Use your own **authorized** data and compatible dependency versions.
3. Verify atom numbering, units, parse behavior, charges/spins and numerical outputs against known references.
4. No general claim of reliability or validated reproducibility is made yet. Do not execute notebooks blind.

## Source

Each notebook records its source filename from the original `C_programing` Git repository. This collection does not include cycloetherification notebooks.

### Steric calculator (revised prototype)

```bash
python -m pip install morfeus-ml
python molecular-sterics/steric_descriptors.py --folder xyz_files --metal Pd --ligand-atoms 2,3,4 --output sterics.csv
```

**Do not copy these example atom indices onto your structures.** Provide the actual ligand atom indices (1-based) for the selected metal and the entire XYZ frame. The revised API calls follow the [Morfeus reference](https://digital-chemistry-laboratory.github.io/morfeus/). The mock tests check only code plumbing, not molecular correctness.
