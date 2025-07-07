import dash_mantine_components as dmc
from dash import Input, Output, callback, html
from dash_iconify import DashIconify

from . import base


def get_battery_properties(params) -> html.Div:
    return dmc.Stack(
        gap="xs",
        children=[
            dmc.NumberInput(
                id={"id": "battery_max_energy_kWh", "type": "param"},
                label="Batterikapacitet [kWh]",
                hideControls=True,
                decimalSeparator=".",
                decimalScale=2,
                min=0,
                max=1e9,
                placeholder=["kWh"],
                value=params["battery_max_energy_kWh"],
                fixedDecimalScale=True,
            ),
            dmc.NumberInput(
                id={"id": "battery_max_power_kW", "type": "param"},
                label="Batteri effekt [kW]",
                hideControls=True,
                decimalSeparator=".",
                decimalScale=2,
                min=0,
                max=1e9,
                placeholder=["kW"],
                value=params["battery_max_power_kW"],
                fixedDecimalScale=True,
            ),
        ],
    )


def get_advanced_battery_properties(params) -> html.Div:
    return dmc.Stack(
        gap="xs",
        children=[
            dmc.NumberInput(
                id={"id": "battery_efficiency", "type": "param"},
                label="Ladningseffektivitet",
                hideControls=True,
                decimalSeparator=".",
                decimalScale=2,
                min=0,
                max=1e9,
                placeholder=["%"],
                value=params["battery_efficiency"],
                fixedDecimalScale=True,
            ),
        ],
    )


def get_active_battery_properties(params) -> html.Div:
    return html.Div(
        id="battery-section",
        children=[
            base.get_section(
                name="Egenskaber", children=[get_battery_properties(params)]
            )
        ],
    )


def get_battery_panel(params) -> html.Div:
    return base.get_panel(
        name="Batteri",
        children=[
            dmc.Switch(
                label="Intet batteri",
                id={"id": "no_battery", "type": "param"},
                checked=params["no_battery"],
            ),
            get_active_battery_properties(params),
        ],
    )


@callback(
    Output("battery-section", "style"),
    Input({"id": "no_battery", "type": "param"}, "checked"),
)
def toggle_battery_section(checked: bool) -> dict:
    show = {"display": "block"}
    hide = {"display": "none"}
    if checked:
        return hide
    return show


@callback(
    Output("battery-section-icon", "children"),
    Input({"id": "no_battery", "type": "param"}, "checked"),
)
def toggle_battery_section_icon(checked: bool) -> html.Div:
    if checked:
        return DashIconify(icon="ic:twotone-battery-2-bar")
    return DashIconify(icon="ic:twotone-battery-2-bar", color="#40C057")
