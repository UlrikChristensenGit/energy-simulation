import pandas as pd
import xarray as xr
from calculations import utils

from dashboard import plotting

pd.options.plotting.backend = "plotly"


def make_pv_generation_time_series_chart(ds: xr.Dataset):
    ds["pv_to_consumption_kWh"] = utils.joule_to_kwh(ds["pv_to_consumption_J"])
    ds["pv_to_battery_kWh"] = utils.joule_to_kwh(ds["pv_to_battery_J"])
    ds["pv_to_grid_kWh"] = utils.joule_to_kwh(ds["pv_to_grid_J"])

    x = {"column": "time_utc", "label": "Tid"}
    y = [
        {"column": "pv_to_consumption_kWh", "label": "Til forbrug", "color": "yellow.6"},
        {
            "column": "pv_to_battery_kWh",
            "label": "Til battery (opladning)",
            "color": "pink.6",
        },
        {"column": "pv_to_grid_kWh", "label": "Til elnet", "color": "blue.6"},
    ]

    return plotting.area(
        ds, x, y, yaxis_label="kWh", curve_type="linear", type="stacked"
    )


def make_consumption_time_series_chart(ds: xr.Dataset):
    ds["pv_to_consumption_kWh"] = utils.joule_to_kwh(ds["pv_to_consumption_J"])
    ds["battery_to_consumption_kWh"] = utils.joule_to_kwh(ds["battery_to_consumption_J"])
    ds["grid_to_consumption_kWh"] = utils.joule_to_kwh(ds["grid_to_consumption_J"])

    x = {"column": "time_utc", "label": "Tid"}
    y = [
        {
            "column": "pv_to_consumption_kWh",
            "label": "Fra solceller",
            "color": "yellow.6",
        },
        {
            "column": "battery_to_consumption_kWh",
            "label": "Fra batteri (afladning)",
            "color": "pink.6",
        },
        {"column": "grid_to_consumption_kWh", "label": "Fra elnet", "color": "blue.6"},
    ]

    return plotting.area(
        ds, x, y, yaxis_label="kWh", curve_type="linear", type="stacked"
    )


def make_cost_savings_time_series_chart(ds: xr.Dataset):
    x = {"column": "time_utc", "label": "Tid"}
    y = [
        {"column": "saved_costs_DKK", "label": "Omkostningsbesparelse", "color": "gray.6"},
    ]

    return plotting.area(
        ds, x, y, yaxis_label="DKK", curve_type="linear", type="split"
    )
