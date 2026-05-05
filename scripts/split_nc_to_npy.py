from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import xarray as xr

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Split a NetCDF file into one .npy file per time step. "
            "Each output file is named like 2026-01-01T00.npy."
        )
    )
    parser.add_argument(
        "nc_file",
        type=Path,
        help="Path to the source .nc file.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=(
            "Base output directory. The final directory always appends the nc file name "
            "without extension. Default: <project>/data"
        ),
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing .npy files.",
    )
    return parser


def validate_args(args: argparse.Namespace) -> None:
    if not args.nc_file.exists():
        raise SystemExit(f"NetCDF file does not exist: {args.nc_file}")
    if args.nc_file.suffix.lower() != ".nc":
        raise SystemExit(f"Input file must be a .nc file: {args.nc_file}")


def resolve_output_dir(nc_file: Path, base_output_dir: Path) -> Path:
    return base_output_dir.resolve() / nc_file.stem


def format_time_filename(value: np.datetime64) -> str:
    timestamp = np.datetime_as_string(value, unit="h")
    return f"{timestamp}.npy"


def variable_to_array(dataset: xr.Dataset, variable_name: str, time_index: int) -> np.ndarray:
    values = dataset[variable_name].isel(time=time_index).to_numpy()
    return values.astype(np.float32)


def split_nc_to_npy(nc_file: Path, output_dir: Path, overwrite: bool) -> int:
    output_dir.mkdir(parents=True, exist_ok=True)

    with xr.open_dataset(nc_file) as dataset:
        if "time" not in dataset.dims:
            raise SystemExit("The NetCDF file does not contain a 'time' dimension.")
        if not dataset.data_vars:
            raise SystemExit("The NetCDF file does not contain any data variables.")

        time_values = dataset["time"].to_numpy()
        written = 0

        for variable_name in dataset.data_vars:
            if "time" not in dataset[variable_name].dims:
                raise SystemExit(
                    f"Variable {variable_name!r} does not contain a 'time' dimension."
                )

            variable_output_dir = output_dir / variable_name
            variable_output_dir.mkdir(parents=True, exist_ok=True)

            for index, time_value in enumerate(time_values):
                output_file = variable_output_dir / format_time_filename(time_value)
                if output_file.exists() and not overwrite:
                    print(f"[SKIP] {output_file}")
                    continue

                array = variable_to_array(dataset, variable_name, index)
                np.save(output_file, array)
                print(f"[OK] {output_file}")
                written += 1

    return written


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    validate_args(args)

    output_dir = resolve_output_dir(args.nc_file, args.output_dir)
    print(f"Input nc file: {args.nc_file}")
    print(f"Output directory: {output_dir}")

    count = split_nc_to_npy(
        nc_file=args.nc_file,
        output_dir=output_dir,
        overwrite=args.overwrite,
    )
    print(f"Generated {count} npy files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
