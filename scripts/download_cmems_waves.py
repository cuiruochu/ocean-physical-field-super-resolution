from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable

import copernicusmarine

VARIABLES = ["VMDR", "VTM10", "VHM0"]


@dataclass(frozen=True)
class ProductConfig:
    dataset_id: str
    file_tag: str


PRODUCTS: dict[str, ProductConfig] = {
    "GLOBAL_ANALYSISFORECAST_WAV_001_027": ProductConfig(
        dataset_id="cmems_mod_glo_wav_anfc_0.083deg_PT3H-i",
        file_tag="analysisforecast",
    ),
    "GLOBAL_MULTIYEAR_WAV_001_032": ProductConfig(
        dataset_id="cmems_mod_glo_wav_my_0.2deg_PT3H-i",
        file_tag="multiyear",
    ),
}


def parse_datetime(value: str) -> datetime:
    normalized = value.strip()

    if not (
        normalized.endswith("Z")
        or normalized.endswith("+00:00")
        or normalized.endswith("+0000")
    ):
        raise argparse.ArgumentTypeError(
            f"Invalid datetime: {value!r}. Use explicit UTC time with a trailing 'Z', "
            "for example 2026-01-01T00:00:00Z."
        )

    if normalized.endswith("Z"):
        normalized = f"{normalized[:-1]}+00:00"

    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"Invalid datetime: {value!r}. Use ISO 8601 UTC time, "
            "for example 2026-01-01T00:00:00Z."
        ) from exc

    if parsed.tzinfo is None:
        raise argparse.ArgumentTypeError(
            f"Invalid datetime: {value!r}. Timezone information is required. "
            "Use UTC time with a trailing 'Z'."
        )

    return parsed.astimezone(UTC)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Download CMEMS wave subsets for "
            "GLOBAL_ANALYSISFORECAST_WAV_001_027 and GLOBAL_MULTIYEAR_WAV_001_032."
        )
    )
    parser.add_argument(
        "--products",
        nargs="+",
        choices=sorted(PRODUCTS),
        default=list(PRODUCTS),
        help="Products to download. Default: both products.",
    )
    parser.add_argument("--min-lon", type=float, required=True, help="Minimum longitude in degrees east.")
    parser.add_argument("--max-lon", type=float, required=True, help="Maximum longitude in degrees east.")
    parser.add_argument("--min-lat", type=float, required=True, help="Minimum latitude in degrees north.")
    parser.add_argument("--max-lat", type=float, required=True, help="Maximum latitude in degrees north.")
    parser.add_argument(
        "--start",
        type=parse_datetime,
        required=True,
        help="Start time in ISO 8601 UTC format, for example 2026-01-01T00:00:00Z.",
    )
    parser.add_argument(
        "--end",
        type=parse_datetime,
        required=True,
        help="End time in ISO 8601 UTC format, for example 2026-05-01T00:00:00Z.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("downloads"),
        help="Directory where downloaded NetCDF files are written. Default: downloads",
    )
    parser.add_argument(
        "--username",
        default=os.getenv("CMEMS_USERNAME"),
        help="CMEMS username. Defaults to environment variable CMEMS_USERNAME.",
    )
    parser.add_argument(
        "--password",
        default=os.getenv("CMEMS_PASSWORD"),
        help="CMEMS password. Defaults to environment variable CMEMS_PASSWORD.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing output files.",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Skip download when the target file already exists.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the request without downloading the file.",
    )
    parser.add_argument(
        "--no-progress",
        action="store_true",
        help="Disable the Copernicus Marine progress bar.",
    )
    return parser


def validate_args(args: argparse.Namespace) -> None:
    if args.min_lon >= args.max_lon:
        raise SystemExit("--min-lon must be smaller than --max-lon.")
    if args.min_lat >= args.max_lat:
        raise SystemExit("--min-lat must be smaller than --max-lat.")
    if args.start > args.end:
        raise SystemExit("--start must be earlier than or equal to --end.")
    if args.overwrite and args.skip_existing:
        raise SystemExit("--overwrite and --skip-existing cannot be used together.")
    if bool(args.username) != bool(args.password):
        raise SystemExit("--username and --password must be provided together.")
    if not args.username or not args.password:
        raise SystemExit(
            "CMEMS credentials are required. Pass --username/--password or set "
            "CMEMS_USERNAME and CMEMS_PASSWORD."
        )


def compact_datetime(value: datetime) -> str:
    return value.strftime("%Y%m%dT%H%M%S")


def compact_coord(value: float) -> str:
    text = f"{value:.3f}".rstrip("0").rstrip(".")
    return text.replace("-", "m").replace(".", "p")


def build_filename(product_id: str, start: datetime, end: datetime, args: argparse.Namespace) -> str:
    product = PRODUCTS[product_id]
    return (
        f"{product.file_tag}_"
        f"{compact_datetime(start)}_{compact_datetime(end)}_"
        f"lon{compact_coord(args.min_lon)}_{compact_coord(args.max_lon)}_"
        f"lat{compact_coord(args.min_lat)}_{compact_coord(args.max_lat)}.nc"
    )


def build_subset_kwargs(
    product_id: str,
    start: datetime,
    end: datetime,
    args: argparse.Namespace,
) -> dict[str, object]:
    filename = build_filename(product_id, start, end, args)
    config = PRODUCTS[product_id]
    kwargs: dict[str, object] = {
        "dataset_id": config.dataset_id,
        "variables": VARIABLES,
        "minimum_longitude": args.min_lon,
        "maximum_longitude": args.max_lon,
        "minimum_latitude": args.min_lat,
        "maximum_latitude": args.max_lat,
        "start_datetime": start,
        "end_datetime": end,
        "output_directory": args.output_dir,
        "output_filename": filename,
        "file_format": "netcdf",
        "overwrite": args.overwrite,
        "skip_existing": args.skip_existing,
        "dry_run": args.dry_run,
        "disable_progress_bar": args.no_progress,
    }

    if args.username:
        kwargs["username"] = args.username
    if args.password:
        kwargs["password"] = args.password
    return kwargs


def download_products(product_ids: Iterable[str], args: argparse.Namespace) -> int:
    args.output_dir.mkdir(parents=True, exist_ok=True)

    failures = 0
    for product_id in product_ids:
        print(f"Downloading {product_id} with variables {', '.join(VARIABLES)}")
        try:
            response = copernicusmarine.subset(
                **build_subset_kwargs(product_id, args.start, args.end, args)
            )
        except Exception as exc:
            failures += 1
            print(f"[ERROR] {product_id}: {exc}")
            continue

        print(f"[OK] {product_id}: {response.file_path}")

    return 1 if failures else 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    validate_args(args)
    return download_products(args.products, args)


if __name__ == "__main__":
    raise SystemExit(main())
