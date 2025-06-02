import datetime as dt
from dataclasses import dataclass


@dataclass
class ThermalParameters:
    """Parameters to calculate the temperature of PV cells
    according to the Sandia Array Performance Model (SAPM) [1,2].

    References:
    [1] https://pvpmc.sandia.gov/modeling-guide/2-dc-module-iv/point-value-models/sandia-pv-array-performance-model/
    [2] https://pvlib-python.readthedocs.io/en/stable/reference/generated/pvlib.temperature.sapm_cell.html
    """

    a: float
    b: float
    deltaT: float


@dataclass
class ModuleParameters:
    """Parameters to calculate the DC power output
    of a PV module according to the PVWatts model [1,2].

    References:
    [1] https://pvwatts.nrel.gov/pvwatts.php
    [2] https://pvlib-python.readthedocs.io/en/stable/reference/generated/pvlib.pvsystem.pvwatts_dc.html
    """

    temperature_coefficient: float
    dc_capacity: float


@dataclass
class InverterParameters:
    """Parameters to calculate the AC power output
    of a PV inverter according to the PVWatts model [1,2].

    References:
    [1] https://pvwatts.nrel.gov/pvwatts.php
    [2] https://pvlib-python.readthedocs.io/en/stable/reference/generated/pvlib.inverter.pvwatts.html#pvlib.inverter.pvwatts
    """

    nominal_efficiency: float
    ac_capacity: float


@dataclass
class PVSystemParameters:
    module_params: ModuleParameters
    inverter_params: InverterParameters
    thermal_params: ThermalParameters


@dataclass
class Coordinate:
    latitude: float
    longitude: float
    altitude: float


class Direction:

    def __init__(
        self,
        azimuth: float,
        zenith: float = None,
        elevation: float = None,
    ):
        self.azimuth = azimuth
        if (zenith is None and elevation is None) or (
            not zenith is None and not elevation is None
        ):
            raise ValueError("Must supply one and only one of `zenith` or `elevation`")
        if zenith is None:
            self.zenith = 90 - elevation
            self.elevation = elevation
        if elevation is None:
            self.zenith = zenith
            self.elevation = 90 - zenith


@dataclass
class PVSystem:
    system_params: PVSystemParameters
    direction: Direction
    coordinate: Coordinate


@dataclass
class NWP:
    time: dt.datetime
    air_temperature: float
    wind_speed_u: float
    wind_speed_v: float
    global_radiation: float


@dataclass
class Battery:
    max_energy: float
    charge_efficiency: float
    discharge_efficiency: float
    min_state_of_charge: float
    max_state_of_charge: float
    max_charge_power: float
    max_discharge_power: float


@dataclass
class HybridSystem:
    pv_system: PVSystem
    battery: Battery
    # optimize_for_spot_price: bool
    # optimize_for_forecast: bool
