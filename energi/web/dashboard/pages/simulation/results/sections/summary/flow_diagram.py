import base64 as b64
from pathlib import Path

from dash import html


def make_flow_diagram(metrics: dict[str, float]) -> html.Div:
    path = Path(__file__).parent / "power-flow.svg"
    content = path.read_text()
    content = content.format(
        pv_grid=metrics["pv_to_grid_J"],
        pv_bat=metrics["pv_to_battery_J"],
        pv_cons=metrics["pv_to_consumption_J"],
        grid_cons=metrics["grid_to_consumption_J"],
        bat_cons=metrics["battery_to_consumption_J"],
    )
    encoded = b64.b64encode(content.encode("utf-8"))
    svg = "data:image/svg+xml;base64,{}".format(encoded.decode())
    return html.Img(src=svg, height=300)
