from pathlib import Path

import xarray as xr

from calculations.utils.kdtree import CoordinateKDTree


def get_coord_kdtree() -> CoordinateKDTree:
    """Get the NWP coordinate KDTree."""
    file_path = Path(__file__).parent / "nwp_coordinates.nc"
    coords = xr.open_dataset(file_path, engine="h5netcdf")

    kd_tree = CoordinateKDTree()
    kd_tree.fit(coords.coords)

    return kd_tree


coord_kdtree = get_coord_kdtree()
