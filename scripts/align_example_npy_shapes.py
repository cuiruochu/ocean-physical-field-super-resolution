from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "tmp"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Align example ERA5, CMEMS multiyear, and CMEMS analysisforecast npy files "
            "into shape-compatible outputs."
        )
    )
    parser.add_argument("era5_npy", type=Path, help="Path to the ERA5 .npy file.")
    parser.add_argument(
        "cmems_multiyear_npy",
        type=Path,
        help="Path to the CMEMS multiyear .npy file.",
    )
    parser.add_argument(
        "cmems_analysisforecast_npy",
        type=Path,
        help="Path to the CMEMS analysisforecast .npy file.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Output directory. Default: ./tmp",
    )
    return parser


def load_array(path: Path) -> np.ndarray:
    if not path.exists():
        raise SystemExit(f"File does not exist: {path}")
    array = np.load(path)
    if array.ndim != 2:
        raise SystemExit(f"Expected a 2D array in {path}, but got shape {array.shape}")
    return array.astype(np.float32)


def transform_era5(values: np.ndarray) -> np.ndarray:
    # 1. Flip vertically so the latitude direction matches CMEMS.
    flipped = np.flipud(values)
    # 2. Remove the maximum-latitude row and maximum-longitude column.
    return flipped[:-1, :-1]


def transform_cmems_multiyear(values: np.ndarray) -> np.ndarray:
    # Remove the minimum-longitude column.
    return values[:, 1:]


def transform_cmems_analysisforecast(values: np.ndarray) -> np.ndarray:
    # Remove the minimum-latitude row and minimum-longitude column.
    return values[1:, 1:]


def build_output_path(output_dir: Path, source_path: Path, source_tag: str, suffix: str) -> Path:
    return output_dir / f"{source_tag}_{source_path.stem}_{suffix}.npy"


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    era5 = load_array(args.era5_npy)
    cmems_multiyear = load_array(args.cmems_multiyear_npy)
    cmems_analysisforecast = load_array(args.cmems_analysisforecast_npy)

    era5_aligned = transform_era5(era5)
    cmems_multiyear_aligned = transform_cmems_multiyear(cmems_multiyear)
    cmems_analysisforecast_aligned = transform_cmems_analysisforecast(cmems_analysisforecast)

    era5_output = build_output_path(output_dir, args.era5_npy, "era5", "aligned")
    multiyear_output = build_output_path(
        output_dir, args.cmems_multiyear_npy, "cmems_multiyear", "aligned"
    )
    analysisforecast_output = build_output_path(
        output_dir, args.cmems_analysisforecast_npy, "cmems_analysisforecast", "aligned"
    )

    np.save(era5_output, era5_aligned)
    np.save(multiyear_output, cmems_multiyear_aligned)
    np.save(analysisforecast_output, cmems_analysisforecast_aligned)

    print(f"ERA5 input shape: {era5.shape}")
    print(f"ERA5 aligned shape: {era5_aligned.shape}")
    print(f"ERA5 output: {era5_output}")
    print()
    print(f"CMEMS multiyear input shape: {cmems_multiyear.shape}")
    print(f"CMEMS multiyear aligned shape: {cmems_multiyear_aligned.shape}")
    print(f"CMEMS multiyear output: {multiyear_output}")
    print()
    print(f"CMEMS analysisforecast input shape: {cmems_analysisforecast.shape}")
    print(f"CMEMS analysisforecast aligned shape: {cmems_analysisforecast_aligned.shape}")
    print(f"CMEMS analysisforecast output: {analysisforecast_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
