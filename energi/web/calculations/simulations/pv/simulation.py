from pathlib import Path

import pandas as pd
import xarray as xr

from calculations import data
from calculations.models import Coordinate, PVSystem
from calculations.simulations.pv import formulas
from dashboard.cache import cache


def ac_power_from_nwp(
    system: PVSystem,
    nwp: xr.Dataset,
) -> xr.DataArray:
    nwp = nwp.to_dataframe()

    ac_power = formulas.ac_power_from_nwp(system, nwp)

    ac_power = xr.DataArray.from_series(ac_power).rename("pv_generation_W")

    return ac_power


def interpolate_nwp_at_coordinate(
    nwp: xr.Dataset, coordinate: Coordinate
) -> xr.Dataset:
    nearest_neighbour = data.nwp.coord_kdtree.nearest_index(coordinate)

    nwp = nwp.sel(nearest_neighbour).compute()
    # nwp = nwp.sel(x=1225, y=825).compute()

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


@cache.memoize(ignore=[0])
def interpolate_nwp(nwp: xr.Dataset, coordinate: Coordinate):
    nwp = interpolate_nwp_at_coordinate(nwp, coordinate)

    nwp = nwp.bfill(dim="altitude_m").sel(altitude_m=0)

    nwp = interpolate_nwp_on_time(nwp)
    return nwp


@cache.memoize()
def simulate_pv_generation(system: PVSystem) -> xr.DataArray:
    print("Recalculating pv generation")
    nwp = data.nwp.get_nwp(system.coordinate)

    ac_power = ac_power_from_nwp(system, nwp)

    return ac_power
