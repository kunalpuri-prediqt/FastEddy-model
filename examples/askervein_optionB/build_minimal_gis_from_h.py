#!/usr/bin/env python3
"""Create a minimal GIS NetCDF file for FastEddy GeoSpec.py from a terrain array h(y,x).

This script is intended for Option-B style preprocessing:
1) build GIS-like NetCDF from h(y,x)
2) run GeoSpec.py
3) run SimGrid.py
"""

import argparse
from pathlib import Path

import numpy as np
import xarray as xr


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--h-npy", required=True, help="Path to terrain npy file with shape (Ny, Nx), meters ASL.")
    p.add_argument("--cellsize", type=float, required=True, help="Horizontal grid spacing (m).")
    p.add_argument("--out", default="inputs_gis.nc", help="Output NetCDF path.")
    p.add_argument("--land-class", type=int, default=71, help="Constant LandCover class id.")
    p.add_argument("--center-lat", type=float, default=57.18, help="Reference latitude (deg).")
    p.add_argument("--center-lon", type=float, default=-7.37, help="Reference longitude (deg).")
    p.add_argument("--dlat", type=float, default=0.0, help="Optional north-south increment per j index (deg).")
    p.add_argument("--dlon", type=float, default=0.0, help="Optional east-west increment per i index (deg).")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    h = np.load(args.h_npy).astype(np.float32)
    if h.ndim != 2:
        raise ValueError(f"Expected 2-D h array, got shape {h.shape}")

    ny, nx = h.shape
    land = np.full((ny, nx), args.land_class, dtype=np.int32)

    lat_1d = args.center_lat + (np.arange(ny) - 0.5 * (ny - 1)) * args.dlat
    lon_1d = args.center_lon + (np.arange(nx) - 0.5 * (nx - 1)) * args.dlon
    lon, lat = np.meshgrid(lon_1d, lat_1d)

    ds = xr.Dataset(
        {
            "elevation": (("y", "x"), h),
            "LandCover": (("y", "x"), land),
            "lat": (("y", "x"), lat.astype(np.float64)),
            "lon": (("y", "x"), lon.astype(np.float64)),
            "cellsize": ((), np.float32(args.cellsize)),
        }
    )

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    ds.to_netcdf(out)
    print(f"Wrote {out} with shape Ny={ny}, Nx={nx}")


if __name__ == "__main__":
    main()
