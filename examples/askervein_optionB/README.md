# Askervein Option-B preprocessing example

This folder demonstrates how to **simulate the real-case preprocessing workflow** (`GeoSpec.py` + `SimGrid.py`) while only providing a terrain field `h(y,x)`.

## What this example contains

- `build_minimal_gis_from_h.py`: creates a minimal GIS-like NetCDF (`inputs_gis.nc`) from `h(y,x)`.
- `LandCoverMetadata_Askervein.csv`: constant roughness lookup table (`z0=0.03 m`).
- `geospec.askervein.json`: GeoSpec config.
- `simgrid.askervein.json`: SimGrid config.
- `Askervein_OptionB.in`: starter FastEddy input file (copied from `Example01_NBL.in`).

## End-to-end steps

1. Save your terrain array as `examples/askervein_optionB/askervein_h.npy` with shape `(Ny, Nx)` and units of meters ASL.

2. Build a minimal GIS input file:

```bash
python examples/askervein_optionB/build_minimal_gis_from_h.py \
  --h-npy examples/askervein_optionB/askervein_h.npy \
  --cellsize 10.0 \
  --out examples/askervein_optionB/inputs_gis.nc \
  --land-class 71 \
  --center-lat 57.18 \
  --center-lon -7.37
```

3. Run GeoSpec:

```bash
python scripts/python_utilities/coupler/GeoSpec.py \
  -f examples/askervein_optionB/geospec.askervein.json
```

4. Edit `examples/askervein_optionB/Askervein_OptionB.in` to set your target `Nx`, `Ny`, `Nz`, `d_xi`, `d_eta`, and `d_zeta`.

5. Run SimGrid:

```bash
python scripts/python_utilities/coupler/SimGrid.py \
  -f examples/askervein_optionB/simgrid.askervein.json
```

6. Update `topoFile` in `Askervein_OptionB.in` to the generated path:

```text
topoFile = ./examples/askervein_optionB/prep/Askervein_Topography_<Nx>x<Ny>.dat
```

7. Run FastEddy with the updated `.in` file.

## Notes

- This is a practical bridge to real-case workflows: only terrain is real, roughness is constant.
- `GeoSpec.py` expects `elevation`, `LandCover`, `lat`, `lon`, and scalar `cellsize` for `gis_opt=0`.
- `SimGrid.py` writes the binary topography file consumed by `topoFile`.
