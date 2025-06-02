import xarray as xr

KEY_FILTERS = {
    ("temperature", 2): {
        "stepType": "instant",
        "typeOfLevel": "heightAboveGround",
        "parameterCategory": 0,
        "parameterNumber": 0,
        "level": 2,
    },
    ("temperature", 100): {
        "stepType": "instant",
        "typeOfLevel": "heightAboveGround",
        "parameterCategory": 0,
        "parameterNumber": 0,
        "level": 100,
    },
    ("wind", 10): {
        "stepType": "instant",
        "typeOfLevel": "heightAboveGround",
        "parameterCategory": 2,
        "parameterNumber": [2, 3],
        "level": 10,
    },
    ("wind", 100): {
        "stepType": "instant",
        "typeOfLevel": "heightAboveGround",
        "parameterCategory": 2,
        "parameterNumber": [2, 3],
        "level": 100,
    },
    ("radiation", 0): {
        "typeOfLevel": "heightAboveGround",
        "parameterCategory": 4,
        "parameterNumber": [3, 9],
        "level": 0,
    },
}

USED_KEYS = [("temperature", 2), ("wind", 10), ("radiation", 0)]


def read_grib_param(file_path: str, parameter: str, altitude: float) -> xr.Dataset:
    key_filters = KEY_FILTERS[(parameter, altitude)]

    return xr.open_dataset(
        file_path,
        engine="cfgrib",
        backend_kwargs={
            "filter_by_keys": key_filters,
            "indexpath": "",
        },
    )


def read_grib(file_path: str) -> xr.Dataset:
    ds_params = []
    for parameter, altitude in USED_KEYS:
        ds_param = read_grib_param(file_path, parameter, altitude)
        ds_param = ds_param.expand_dims("heightAboveGround")
        ds_params.append(ds_param)

    return xr.merge(ds_params)


def transform(ds: xr.Dataset) -> xr.Dataset:
    ds = ds.rename(
        {
            "t2m": "temperature_K",
            "u10": "wind_u_m_s",
            "v10": "wind_v_m_s",
            "grad": "accumulated_global_radiation_J_m2",
            "unknown": "accumulated_direct_radiation_J_m2",
            "heightAboveGround": "altitude_m",
            "valid_time": "time_utc",
            "time": "model_run_time_utc",
        }
    )

    ds = ds.set_coords(["latitude", "longitude"])

    ds["horizon"] = ds["time_utc"] - ds["model_run_time_utc"]

    ds = ds.set_coords(["horizon"])

    ds = ds.drop_vars(["number", "step", "time_utc"])

    ds = ds.expand_dims(["model_run_time_utc", "horizon"])

    return ds
