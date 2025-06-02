import pandas as pd
import xarray as xr
from dash import Input, State, Output, callback

from calculations import simulations, utils
from dashboard.params import unpacking

from .sections import summary, time_series


def get_metrics(ds):
    metrics = dict()
    for var in [
        "pv_to_grid_J",
        "pv_to_battery_J",
        "pv_to_consumption_J",
        "grid_to_consumption_J",
        "battery_to_consumption_J",
        "consumption_J",
        "pv_generation_J",
    ]:
        total_energy = ds[var].sum()
        if var == "consumption_J":
            total_energy = -total_energy
        total_energy = utils.joule_to_kwh(total_energy)
        total_energy = f"{int(total_energy):,d} kWh".replace(",", ".")
        metrics[var] = total_energy
    return metrics


def get_ts(sim: xr.Dataset, resolution: str) -> xr.Dataset:
    """Convert time_utc to pandas datetime index and return the dataset."""

    sim = sim.resample(time_utc=resolution).sum()

    sim = sim.assign_attrs(freq=resolution)

    return sim


@callback(
    Output("consumption-chart", "children"),
    Output("pv-generation-chart", "children"),
    Output("cost-savings-chart", "children"),
    Output("metrics", "children"),
    Output("summary", "children"),
    #Input("run-simulation", "n_clicks"),
    Input("params", "data"),
)
def visualize(params: dict) -> list:
    price_area = params["price_area"]

    hybrid_system = unpacking.get_hybrid_system_model(params)

    sim = simulations.simulate_hybrid_system_with_costs(price_area, hybrid_system)

    start = pd.Timestamp(params["time_range"][0])
    end = pd.Timestamp(params["time_range"][1]) + pd.Timedelta(days=1, microseconds=-1)
    time_range = pd.Interval(start, end)

    sim = sim.sel(time_utc=slice(time_range.left, time_range.right))

    ts = get_ts(sim, params["resolution"])

    consumption_chart = time_series.make_consumption_time_series_chart(ts)

    pv_generation_chart = time_series.make_pv_generation_time_series_chart(ts)

    cost_saving_chart = time_series.make_cost_savings_time_series_chart(ts)

    metrics = get_metrics(sim)

    flow_diagram = summary.make_flow_diagram(metrics)

    balance_sheet = summary.make_balance_sheet(metrics)

    return (
        consumption_chart,
        pv_generation_chart,
        cost_saving_chart,
        flow_diagram,
        balance_sheet,
    )
