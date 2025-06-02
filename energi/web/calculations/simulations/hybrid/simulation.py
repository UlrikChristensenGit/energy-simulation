import pandas as pd
import xarray as xr

from calculations import data, simulations
from calculations.models import Battery, HybridSystem, PVSystem
from dashboard.cache import cache


@cache.memoize()
def simulate_hybrid_system(
    pv_system: PVSystem,
    battery: Battery,
) -> xr.Dataset:
    """Current implementation assumes the following:
    - Excessive PV generation is used to first cover the load, then charge the battery
    - Excessive load is covered first by the battery, then by the grid
    """
    pv_generation = simulations.simulate_pv_generation(pv_system)

    load = data.get_consumption()

    battery_power = simulations.simulate_battery_power(battery, pv_system)

    flow = xr.merge(
        objects=[
            pv_generation,
            load,
            battery_power,
        ],
        join="inner",
    )

    flow["pv_to_battery_W"] = -flow["battery_power_W"].clip(max=0)
    flow["battery_to_consumption_W"] = flow["battery_power_W"].clip(min=0)

    flow["pv_to_consumption_W"] = flow["pv_generation_W"].clip(
        max=-flow["consumption_W"]
    )
    flow["pv_to_grid_W"] = (
        flow["pv_generation_W"] - flow["pv_to_consumption_W"] - flow["pv_to_battery_W"]
    )
    flow["grid_to_consumption_W"] = (
        -flow["consumption_W"]
        - flow["pv_to_consumption_W"]
        - flow["battery_to_consumption_W"]
    )

    return flow


#@cache.memoize()
def simulate_hybrid_system_with_costs(
    price_area: str,
    hybrid_system: HybridSystem,
):
    print("Recalculating hybrid system with costs")
    spot_prices = data.get_spot_prices(price_area)

    spot_prices = (spot_prices * 1e9) / (1e6 * 3600)

    flow = simulate_hybrid_system(hybrid_system.pv_system, hybrid_system.battery)

    flow = flow.merge(spot_prices, join="left")

    time = flow["time_utc"]
    periods = (time.shift(time_utc=-1) - time).ffill(dim="time_utc").dt.total_seconds()

    flow["consumption_J"] = flow["consumption_W"] * periods
    flow["pv_generation_J"] = flow["pv_generation_W"] * periods
    flow["battery_power_J"] = simulations.net_to_gross(hybrid_system.battery, flow["battery_power_W"]) * periods
    flow["battery_state_of_charge"] = -flow["battery_power_J"].cumsum(dim="time_utc") / hybrid_system.battery.max_energy
    flow["pv_to_battery_J"] = flow["pv_to_battery_W"] * periods
    flow["battery_to_consumption_J"] = flow["battery_to_consumption_W"] * periods
    flow["pv_to_consumption_J"] = flow["pv_to_consumption_W"] * periods
    flow["pv_to_grid_J"] = flow["pv_to_grid_W"] * periods
    flow["grid_to_consumption_J"] = flow["grid_to_consumption_W"] * periods

    flow["grid_cost_DKK"] = -flow["grid_to_consumption_J"] * flow["spot_price_DKK_J"]
    flow["pv_saved_costs_DKK"] = flow["pv_to_consumption_J"] * flow["spot_price_DKK_J"]
    flow["battery_saved_costs_DKK"] = (
        flow["battery_to_consumption_J"] * flow["spot_price_DKK_J"]
    )

    flow["saved_costs_DKK"] = flow["pv_saved_costs_DKK"] + flow["battery_saved_costs_DKK"]

    return flow
