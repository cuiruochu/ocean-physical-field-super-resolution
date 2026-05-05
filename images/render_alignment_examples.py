from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

PROJECT_ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = PROJECT_ROOT / "images"


def plot_single(
    values: np.ndarray,
    output_path: Path,
    title: str,
    vmin: float,
    vmax: float,
) -> None:
    fig, ax = plt.subplots(figsize=(10, 8), dpi=160)
    image = ax.imshow(np.ma.masked_invalid(values), cmap="viridis", vmin=vmin, vmax=vmax)
    ax.set_title(title)
    ax.set_xlabel("Longitude Index")
    ax.set_ylabel("Latitude Index")
    colorbar = fig.colorbar(image, ax=ax)
    colorbar.set_label("Wave Height (m)")
    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


def main() -> int:
    target_time = np.datetime64("2026-01-01T00:00:00")

    cmems = xr.open_dataset(
        PROJECT_ROOT / "downloads" / "analysisforecast_20260101T000000_20260501T000000_lon105_135_lat0_45.nc"
    )["VHM0"].sel(time=target_time)
    era5 = xr.open_dataset(
        PROJECT_ROOT / "downloads" / "df44a36af69b40d1e1fa386759c08acc.nc"
    )["swh"].sel(valid_time=target_time)

    cmems_values = cmems.to_numpy()
    era5_values = era5.to_numpy()

    merged = np.concatenate(
        [
            cmems_values[np.isfinite(cmems_values)],
            era5_values[np.isfinite(era5_values)],
        ]
    )
    vmin = float(np.min(merged))
    vmax = float(np.max(merged))

    cmems_title = (
        "CMEMS VHM0 2026-01-01T00\n"
        "top-left=(lat 0.0, lon 105.0), bottom-right=(lat 45.0, lon 135.0)"
    )
    era5_title = (
        "ERA5 swh 2026-01-01T00\n"
        "top-left=(lat 45.0, lon 105.0), bottom-right=(lat 0.0, lon 135.0)"
    )

    plot_single(
        values=cmems_values,
        output_path=IMAGES_DIR / "cmems_vhm0_2026-01-01T00.png",
        title=cmems_title,
        vmin=vmin,
        vmax=vmax,
    )
    plot_single(
        values=era5_values,
        output_path=IMAGES_DIR / "era5_swh_2026-01-01T00.png",
        title=era5_title,
        vmin=vmin,
        vmax=vmax,
    )

    print(IMAGES_DIR / "cmems_vhm0_2026-01-01T00.png")
    print(IMAGES_DIR / "era5_swh_2026-01-01T00.png")
    print(f"shared vmin={vmin}")
    print(f"shared vmax={vmax}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
