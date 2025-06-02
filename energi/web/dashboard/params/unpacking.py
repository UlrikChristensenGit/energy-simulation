"""
Module for casting input and output values of callback functions.
This is used when defining our callbacks, because we want to automatically
deserialize inputs values and deserialize output values, due to Dash not being
able to store complex objects (but only JSON-serializable objects).
"""

import pandas as pd

from calculations.models import (
    Battery,
    Coordinate,
    Direction,
    HybridSystem,
    InverterParameters,
    ModuleParameters,
    PVSystem,
    PVSystemParameters,
    ThermalParameters,
)


def get_pv_system_model(params: dict) -> PVSystem:
    if params["no_pv"]:
        ac_capacity = 0
        dc_capacity = 0
    else:
        ac_capacity = params["pv_ac_capacity_kW"] * 1000
        dc_capacity = params["pv_dc_capacity_kW"] * 1000

    coord = Coordinate(
        latitude=params["latitude"],
        longitude=params["longitude"],
        altitude=0,
    )

    direction = Direction(
        azimuth=params["pv_azimuth"],
        elevation=params["pv_tilt"],
    )

    return PVSystem(
        system_params=PVSystemParameters(
            module_params=ModuleParameters(
                temperature_coefficient=params["pv_temperature_coefficient"],
                dc_capacity=dc_capacity,
            ),
            inverter_params=InverterParameters(
                nominal_efficiency=params["pv_efficiency"],
                ac_capacity=ac_capacity,
            ),
            thermal_params=ThermalParameters(
                a=-3.47,
                b=-0.0594,
                deltaT=3,
            ),
        ),
        direction=direction,
        coordinate=coord,
    )


def get_battery_model(
    params: dict,
):
    if params["no_battery"]:
        max_energy = 0
    else:
        max_energy = params["battery_max_energy_kWh"] * 3600000  # Convert kWh to J

    return Battery(
        max_energy=max_energy,
        charge_efficiency=params["battery_efficiency"],
        discharge_efficiency=params["battery_efficiency"],
        min_state_of_charge=0.0,
        max_state_of_charge=1.0,
        max_charge_power=params["battery_max_power_kW"] * 1000,
        max_discharge_power=params["battery_max_power_kW"] * 1000,
    )


def get_hybrid_system_model(params: dict):
    return HybridSystem(
        pv_system=get_pv_system_model(params),
        battery=get_battery_model(params),
    )
