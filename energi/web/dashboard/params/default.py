import datetime as dt

DEFAULT_END_DATE = dt.datetime.now()
DEFAULT_START_DATE = DEFAULT_END_DATE - dt.timedelta(days=3)
DEFAULT_PARAMS = {
    "date_range": [
        DEFAULT_START_DATE.strftime("%Y%m%d"),
        DEFAULT_END_DATE.strftime("%Y%m%d"),
    ],
    "battery_max_energy_kWh": 10.0,
    "battery_efficiency": 0.96,
    "battery_max_power_kW": 3.0,
    "no_battery": True,
    "consumption_data_choice": "default",
    "num_adults": 2,
    "num_children": 2,
    "price_area": "DK1",
    "location_choice": "address",
    "latitude": 55.6761,
    "longitude": 12.5683,
    "address": "Nørrebrogade 123, 2200 København N",
    "pv_dc_capacity_kW": 5.1,
    "pv_ac_capacity_kW": 5.0,
    "pv_tilt": 37.5,
    "pv_azimuth": 180,
    "pv_efficiency": 0.96,
    "pv_temperature_coefficient": 0.004,
    "no_pv": False,
    "resolution": "D",
    "time_range": [dt.datetime(2024, 6, 1), dt.datetime(2025, 5, 1)],
}
