import dash_mantine_components as dmc
import xarray as xr
from calculations import utils


def area(
    ds: xr.Dataset,
    x: dict,
    y: list[dict],
    yaxis_label: str,
    right_yaxis_label: str = None,
    curve_type: str = "monotone",
    type: str = None,
):
    ds = ds.round(2)

    # ds = ds.where(ds != 0, None)

    freq = ds.attrs["freq"]

    if freq == "W-MON":
        xaxis_time_format = "%G/%V"
        xaxis_label = "År/Uge"
        curve_type = "step"
    elif freq == "D":
        xaxis_time_format = "%Y-%m-%d"
        xaxis_label = "Dato"
        curve_type = "step"
    elif freq == "h":
        xaxis_time_format = "%Y-%m-%d %H:%M"
        xaxis_label = "Tidspunkt"
        curve_type = "step"
    elif freq == "ME":
        xaxis_time_format = "%Y %b"
        xaxis_label = "År/Måned"
        curve_type = "step"
    else:
        raise ValueError(f"Unsupported frequency: {freq}")

    ds["time_utc"] = ds["time_utc"].dt.strftime(xaxis_time_format)

    df = ds.to_dataframe()

    df = df.reset_index()

    df = df.filter([i["column"] for i in [x] + y])

    df = df.rename(columns={x["column"]: x["label"]})
    df = df.rename(columns={i["column"]: i["label"] for i in y})

    series = []
    for i in y:
        serie = {"name": i["label"], "color": i["color"]}
        if "right" in i:
            serie["yAxisId"] = "right"
        if "fillOpacity" in i:
            serie["fillOpacity"] = i["fillOpacity"]
        series.append(serie)

    unit = f" {yaxis_label}"

    return dmc.AreaChart(
        h=300,
        data=df.to_dict(orient="records"),
        dataKey=x["label"],
        withRightYAxis=True,
        xAxisLabel=xaxis_label,
        unit=unit,
        rightYAxisLabel=right_yaxis_label,
        withDots=False,
        withLegend=True,
        series=series,
        curveType=curve_type,
        type=type,
    )
