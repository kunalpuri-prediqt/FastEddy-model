***************************
Askervein (Option-B Setup)
***************************

This page documents a lightweight way to prepare an Askervein hill test while following the same preprocessing pattern used for real-world FastEddy cases:

1. Build a minimal GIS-style NetCDF from terrain ``h(y,x)``
2. Run ``GeoSpec.py``
3. Run ``SimGrid.py``
4. Use generated topography in ``topoFile``

Reference files are provided under:

.. code-block:: none

   examples/askervein_optionB/

Quick start
===========

1. Save terrain as ``askervein_h.npy`` with shape ``(Ny, Nx)`` and meters ASL.
2. Build GIS input:

.. code-block:: none

   python examples/askervein_optionB/build_minimal_gis_from_h.py \
     --h-npy examples/askervein_optionB/askervein_h.npy \
     --cellsize 10.0 \
     --out examples/askervein_optionB/inputs_gis.nc

3. Run GeoSpec:

.. code-block:: none

   python scripts/python_utilities/coupler/GeoSpec.py \
     -f examples/askervein_optionB/geospec.askervein.json

4. Edit ``examples/askervein_optionB/Askervein_OptionB.in`` domain/grid parameters.
5. Run SimGrid:

.. code-block:: none

   python scripts/python_utilities/coupler/SimGrid.py \
     -f examples/askervein_optionB/simgrid.askervein.json

6. Set ``topoFile`` in ``Askervein_OptionB.in`` to generated file:

.. code-block:: none

   ./examples/askervein_optionB/prep/Askervein_Topography_<Nx>x<Ny>.dat

Why this is useful
==================

- Keeps your workflow aligned with future real-case simulations.
- Lets you start with only terrain and constant roughness.
- Produces the same topography binary format expected by FastEddy.
