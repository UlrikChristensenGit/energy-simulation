import xarray as xr
import pandas as pd


def transform(df: pd.DataFrame) -> xr.DataArray:
    # convert from MWh to Wh
    df["SpotPriceDKK"] = df["SpotPriceDKK"] / 1e9

    df = df.rename(
        columns={
            "HourUTC": "time_utc",
            "PriceArea": "price_area",
            "SpotPriceDKK": "spot_price_DKK_J",
        }
    )

    df = df.filter(
        [
            "time_utc",
            "price_area",
            "spot_price_DKK_J",
        ]
    )

    df["time_utc"] = df["time_utc"].astype("datetime64[ns]")

    df = df.set_index(["price_area", "time_utc"])

    ds = xr.Dataset.from_dataframe(df)

    return ds
