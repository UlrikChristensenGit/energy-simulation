import datetime as dt

import numpy as np
import pvlib

from calculations.models import NWP, Coordinate, PVSystem, PVSystemParameters

from . import constants


def kelv2cels(temperature: float) -> float:
    return temperature - 273.15


def deg2rad(angle: float) -> float:
    return np.deg2rad(angle)


def magnitude(x: float, y: float) -> float:
    return np.sqrt(np.power(x, 2) + np.power(y, 2))


def poa_from_irradiance_components(
    surface_tilt: float,
    surface_azimuth: float,
    solar_zenith: float,
    solar_azimuth: float,
    global_horizontal_irradiance: float,
    direct_normal_irradiance: float,
    diffuse_horizontal_irradiance: float,
) -> float:
    """Compute the global plane-of-array irradiance (POA)
    given the ambient irradiance components.

    Args:
        surface_tilt (float): Surface tilt [degrees]
        surface_azimuth (float): Surface azimuth angle [degrees]
        solar_zenith (float): Solar zenith angle [degrees]
        solar_azimuth (float): Solar azimuth angle [degrees]
        global_horizontal_irradiance (float): Global horizontal irradiance [W/m2]
        direct_normal_irradiance (float): Direct normal irradiance [W/m2]
        diffuse_horizontal_irradiance (float): Diffuse horizontal irradiance [W/m2]

    Returns:
        float: Global plane-of-array irradiance [W/m2]
    """

    global_poa = pvlib.irradiance.get_total_irradiance(
        surface_tilt=surface_tilt,
        surface_azimuth=surface_azimuth,
        solar_zenith=solar_zenith,
        solar_azimuth=solar_azimuth,
        ghi=global_horizontal_irradiance,
        dni=direct_normal_irradiance,
        dhi=diffuse_horizontal_irradiance,
    )["poa_global"].values

    return global_poa


def ac_power_from_poa(
    system_params: PVSystemParameters,
    global_poa: float,
    air_temperature: float,
    wind_speed: float,
    ac_capacity: float,
) -> float:
    """Compute the AC power output given the plane-of-array irradiance.

    Args:
        global_poa (float): Global plane-of-array irradiance [W/m2]
        air_temperature (float): Air temperature [K]
        wind_speed (float): Wind speed [m/s]
        ac_capacity (float): Nominal AC power

    Returns:
        float: AC power output
    """

    temp_cell = pvlib.temperature.sapm_cell(
        poa_global=global_poa,
        temp_air=kelv2cels(air_temperature),
        wind_speed=wind_speed,
        a=system_params.thermal_params.a,
        b=system_params.thermal_params.b,
        deltaT=system_params.thermal_params.deltaT,
        irrad_ref=constants.STANDARD_CONDITION_RADIATION,
    )

    dc_power = pvlib.pvsystem.pvwatts_dc(
        g_poa_effective=global_poa,
        temp_cell=temp_cell,
        pdc0=system_params.module_params.dc_capacity,
        gamma_pdc=system_params.module_params.temperature_coefficient,
        temp_ref=constants.STANDARD_CONDITION_TEMPERATURE,
    )

    ac_power_no_inverter_limit = pvlib.inverter.pvwatts(
        dc_power,
        system_params.module_params.dc_capacity,
        eta_inv_nom=system_params.inverter_params.nominal_efficiency,
    ).fillna(0)

    ac_power = np.clip(ac_power_no_inverter_limit, 0.0, ac_capacity)

    return ac_power


def zenith_smootherstep(x: float, lower: float = 80.0, upper: float = 90.0) -> float:
    """
    Function for smooth transition, for the zenith
    using the smootherstep function
    (https://en.wikipedia.org/wiki/Smoothstep)
    """
    x = (np.clip(x, lower, upper) - lower) / (upper - lower)
    return 1 - (6 * x**5 - 15 * x**4 + 10 * x**3)


def estimate_irradiance_components(
    global_horizontal_irradiance: float,
    solar_zenith: float,
    day_of_year: int,
):
    """
    Estimate direct normal irradiance (DNI) and diffuse horizontal irradiance (DHI)
    from global horizontal irradiance (GHI) using the Erbs-Driesse model
    """
    # we use the Erbs-Driesse model to estimate the DNI and DHI from GHI.
    # This model calculates DHI = GHI*DF and  DNI=(GHI-DHI)/cos(zenith).
    # In theory, these formulas should pose no problems: When zenith=90,
    # the GHI should also be 0, and we should get DNI=0/0=0. In practice however,
    # when we interpolate the GHI from NWP data, we can not ensure it is 0 when
    # zenith=90. To mitigate this problem, we adjust the GHI here, to ensure it
    # is 0 when zenith=0. We need to do the adjustment in a smooth way.
    # We do this, by making a smooth transition from 0 to 1, when the zenith
    # goes from 80 to 90.

    smooth_transition = zenith_smootherstep(solar_zenith)
    adjusted_ghi = global_horizontal_irradiance * smooth_transition

    irr = pvlib.irradiance.erbs_driesse(
        ghi=adjusted_ghi,
        zenith=solar_zenith,
        datetime_or_doy=day_of_year,
    )
    # the pvlib method doesn't return the global
    # normal irradiance, so we recalculate it here
    irr["gni"] = adjusted_ghi / pvlib.tools.cosd(solar_zenith)

    irr["ghi"] = adjusted_ghi

    return irr


def ac_power_from_ghi(
    system_params: PVSystemParameters,
    global_horizontal_irradiance: float,
    solar_zenith: float,
    solar_azimuth: float,
    surface_tilt: float,
    surface_azimuth: float,
    day_of_year: dt.datetime,
    air_temperature: float,
    wind_speed: float,
):
    irradiance_components = estimate_irradiance_components(
        global_horizontal_irradiance, solar_zenith, day_of_year
    )

    global_poa = poa_from_irradiance_components(
        surface_tilt,
        surface_azimuth,
        solar_zenith,
        solar_azimuth,
        irradiance_components["ghi"],
        irradiance_components["dni"],
        irradiance_components["dhi"],
    )

    return ac_power_from_poa(
        system_params,
        global_poa,
        air_temperature,
        wind_speed,
        system_params.inverter_params.ac_capacity,
    )


def solar_position_from_time(
    coordinate: Coordinate,
    time: dt.datetime,
) -> float:
    time = np.array(time)
    if time.shape == ():
        time = np.array([time])

    location = pvlib.location.Location(
        latitude=coordinate.latitude,
        longitude=coordinate.longitude,
        altitude=coordinate.altitude,
    )

    solar_position = location.get_solarposition(
        time,
    )

    return solar_position


def ac_power_from_nwp(
    system: PVSystem,
    nwp: NWP,
):
    solar_position = solar_position_from_time(
        coordinate=system.coordinate,
        time=nwp.index,
    )

    ac_power = ac_power_from_ghi(
        system_params=system.system_params,
        global_horizontal_irradiance=nwp["global_radiation_W_m2"],
        solar_azimuth=solar_position["azimuth"],
        solar_zenith=solar_position["zenith"],
        surface_azimuth=system.direction.azimuth,
        surface_tilt=system.direction.elevation,
        day_of_year=nwp.index.dayofyear,
        air_temperature=nwp["temperature_K"],
        wind_speed=magnitude(nwp["wind_u_m_s"], nwp["wind_v_m_s"]),
    )

    return ac_power
