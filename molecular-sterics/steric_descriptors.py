"""Ligand-specific steric descriptors from XYZ using morfeus-ml.

Corrected standalone replacement for the original Buried_Vol_Cone_Angle Colab notebook.
Scientific validation against known ligand benchmarks is still needed.
Requires explicit ligand atom indices (1-indexed) to prevent attributing all
of a multi-ligand complex to a single ligand.

Usage:
 python steric_descriptors.py --folder xyz_files --metal Pd --ligand-atoms 2,3,4,5

Ligand atom mapping must be consistent across every XYZ file in a batch.
"""
import argparse
import csv
from pathlib import Path
import sys


def parse_indices(raw):
    """Parse a comma-separated set of 1-indexed atom numbers."""
    try:
        numbers = [int(s.strip()) for s in raw.split(",") if s.strip()]
    except ValueError as exc:
        raise ValueError("ligand atoms must be positive integers") from exc
    if not numbers or any(n < 1 for n in numbers) or len(numbers) != len(set(numbers)):
        raise ValueError("supply unique, positive, 1-indexed ligand atom numbers")
    return numbers


def find_metal_index(elements, symbol):
    """Return unique metal index, 1-indexed; error for missing/ambiguous metals."""
    found = [i for i, el in enumerate(elements, 1) if str(el).lower() == symbol.lower()]
    if len(found) != 1:
        raise ValueError(f"Expected one {symbol} atom; found {len(found)}")
    return found[0]


def compute_descriptors(elements, coordinates, metal, ligand_indices, radius, buried_cls, cone_cls):
    """Compute whole-ligand %Vbur and exact cone angle after selecting ligand atoms.

    All other atom indices are excluded from buried volume. For cone angle,
    construct a subset with metal first, ligand atoms next.
    """
    n = len(elements)
    if len(coordinates) != n:
        raise ValueError("XYZ element and coordinate counts differ")
    metal_idx = find_metal_index(elements, metal)
    ligand = parse_indices(ligand_indices)
    if any(i > n for i in ligand) or metal_idx in ligand:
        raise ValueError("ligand atoms must exist and must exclude the metal atom")
    included = set(ligand) | {metal_idx}
    excluded = [i for i in range(1, n + 1) if i not in included]
    buried = buried_cls(elements, coordinates, metal_idx, excluded_atoms=excluded, radius=radius)
    # ConeAngle index 1 is the central metal in the selected subset.
    selected = [metal_idx] + ligand
    selected_elements = [elements[i - 1] for i in selected]
    selected_coordinates = [coordinates[i - 1] for i in selected]
    cone = cone_cls(selected_elements, selected_coordinates, 1)
    return {
        "metal_index_1based": metal_idx,
        "ligand_atoms_1based": ",".join(map(str, ligand)),
        "buried_volume_percent": 100.0 * float(buried.fraction_buried_volume),
        "cone_angle_degrees": float(cone.cone_angle),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--folder", required=True, type=Path, help="XYZ input folder")
    parser.add_argument("--metal", default="Pd", help="Unique central metal symbol (default Pd)")
    parser.add_argument("--ligand-atoms", required=True, help="1-indexed ligand atom numbers, e.g. 2,3,4")
    parser.add_argument("--radius", type=float, default=3.5, help="Buried-volume sphere radius in Å")
    parser.add_argument("--output", type=Path, default=Path("steric_descriptors.csv"))
    args = parser.parse_args(argv)
    if args.radius <= 0:
        parser.error("radius must be positive")
    files = sorted(args.folder.glob("*.xyz"))
    if not files:
        parser.error(f"No .xyz files found in {args.folder}")
    try:
        from morfeus import BuriedVolume, ConeAngle, read_xyz
    except ImportError:
        parser.error("Install morfeus-ml first: python -m pip install morfeus-ml")
    results = []
    for fname in files:
        try:
            elements, coordinates = read_xyz(str(fname))
            result = compute_descriptors(elements, coordinates, args.metal,
                                         args.ligand_atoms, args.radius, BuriedVolume, ConeAngle)
            result["file"] = fname.name
            results.append(result)
        except (ValueError, IndexError, TypeError, RuntimeError) as exc:
            print(f"SKIP {fname.name}: {exc}", file=sys.stderr)
    if not results:
        parser.error("No valid descriptors calculated; inspect atom mapping and files")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["file", "metal_index_1based", "ligand_atoms_1based", "buried_volume_percent", "cone_angle_degrees"])
        writer.writeheader()
        writer.writerows(results)
    print(f"Wrote {len(results)} structures to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
