import numpy as np
import xarray as xr
from numba import njit

from calculations import data, simulations
from calculations.models import Battery, PVSystem


def net_to_gross(
    battery: Battery,
    net: xr.DataArray,
) -> xr.DataArray:
    gross = net.copy()

    gross.loc[gross > 0] = gross.loc[gross > 0] / battery.discharge_efficiency
    gross.loc[gross < 0] = gross.loc[gross < 0] * battery.charge_efficiency

    return gross


def gross_to_net(
    battery: Battery,
    gross: xr.DataArray,
) -> xr.DataArray:
    net = gross.copy()

    net.loc[net > 0] = net.loc[net > 0] * battery.discharge_efficiency
    net.loc[net < 0] = net.loc[net < 0] / battery.charge_efficiency

    return net


@njit
def cumsum_clip(a, xmin=-np.inf, xmax=np.inf):
    res = np.empty_like(a)
    c = 0
    for i in range(len(a)):
        c = min(max(c + a[i], xmin), xmax)
        res[i] = c
    return res


def simulate_battery_power(
    battery: Battery,
    pv_system: PVSystem,
) -> xr.Dataset:
    print("Recalculating battery power")
    pv_generation = simulations.simulate_pv_generation(pv_system)

    load = data.get_consumption()

    net_target = -(load + pv_generation)

    gross_target = net_to_gross(battery, net_target)

    gross_target = gross_target.clip(
        min=-battery.max_charge_power,
        max=battery.max_discharge_power,
    )

    time = gross_target["time_utc"]
    periods = (time.shift(time_utc=-1) - time).ffill(dim="time_utc").dt.total_seconds()
    potential_energy_flow = -gross_target * periods

    min_allowed_energy = battery.max_energy * battery.min_state_of_charge
    max_allowed_energy = battery.max_energy * battery.max_state_of_charge

    energy_flow = xr.zeros_like(gross_target)

    # start_energy_level = min_allowed_energy # init
    # for t in range(n):
    #    # energy level at end of interval `t`
    #    end_energy_level = (start_energy_level + potential_energy_flow[t]).clip(min_allowed_energy, max_allowed_energy)
    #    energy_flow[t] = (end_energy_level - start_energy_level)
    #    start_energy_level = end_energy_level

    energy_level: xr.DataArray = xr.apply_ufunc(
        cumsum_clip,
        potential_energy_flow,
        kwargs={"xmin": min_allowed_energy, "xmax": max_allowed_energy},
    )

    energy_flow = energy_level.diff(dim="time_utc").fillna(0)

    gross_power = -energy_flow / periods

    net_power = gross_to_net(battery, gross_power)

    return net_power.rename("battery_power_W")
