from pathlib import Path

import pandas as pd
import xarray as xr

from dashboard.cache import cache


@cache.memoize()
def get_consumption(file_name: str = "sample_data.csv") -> xr.DataArray:
    file_path = Path(__file__).parent / file_name

    df = pd.read_csv(file_path, sep=";", decimal=",")
    df["Fra_dato"] = pd.to_datetime(df["Fra_dato"], format="%d-%m-%Y %H:%M:%S")
    df["Til_dato"] = pd.to_datetime(df["Til_dato"], format="%d-%m-%Y %H:%M:%S")

    df["Mængde"] = -df["Mængde"] * 1000

    df = df.rename(columns={"Fra_dato": "time_utc", "Mængde": "consumption_W"})

    df = df.drop_duplicates(subset="time_utc", keep="first")

    s = df.set_index("time_utc")["consumption_W"]

    ds = xr.DataArray.from_series(s)

    return ds
