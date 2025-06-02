import datetime as dt

import pandas as pd
import xarray as xr

from calculations.data.integrations.dataset import Dataset
from calculations.models import Coordinate
from dashboard.cache import cache

from .kdtree import coord_kdtree


def get_raw_nwp():
    nwp = Dataset("latest_nwp_rechunked").read()

    start_time = dt.datetime(2024, 6, 1, 0, 0, 0)
    end_time = dt.datetime(2025, 5, 1, 0, 0, 0)

    nwp = nwp.sel(
        time_utc=slice(start_time, end_time),
    )

    return nwp


def interpolate_nwp_at_coordinate(
    nwp: xr.Dataset, coordinate: Coordinate
) -> xr.Dataset:
    nearest_neighbour = coord_kdtree.nearest_index(coordinate)

    nwp = nwp.sel(nearest_neighbour).compute()

    return nwp


def interpolate_nwp_on_time(nwp: xr.Dataset):
    freq = xr.infer_freq(nwp["time_utc"])

    start_freq = pd.Timedelta(f"1{freq}")

    end_freq = pd.Timedelta("PT5M")

    nwp = nwp.dropna(dim="time_utc")

    index = pd.date_range(
        start=nwp["time_utc"].values.min(),
        end=nwp["time_utc"].values.max(),
        freq=end_freq,
    )

    nwp = nwp.reindex(time_utc=index)

    nwp = nwp.interpolate_na(dim="time_utc", method="pchip")

    nwp["time_utc"] = nwp["time_utc"] - start_freq / 2

    return nwp


@cache.memoize()
def get_nwp(coordinate: Coordinate):
    print("Recalculating NWP")
    nwp = get_raw_nwp()

    nwp = interpolate_nwp_at_coordinate(nwp, coordinate)

    nwp = nwp.bfill(dim="altitude_m").sel(altitude_m=0)

    nwp = interpolate_nwp_on_time(nwp)

    return nwp
