import dash_mantine_components as dmc
from dash import Input, Output, callback, html
from dash_iconify import DashIconify

from . import base


def get_location_choice(params) -> html.Div:
    return dmc.Stack(
        children=[
            dmc.SegmentedControl(
                id={"id": "location_choice", "type": "param"},
                variant="outline",
                value=params["location_choice"],
                data=[
                    {"value": "address", "label": "Adresse"},
                    {"value": "coordinate", "label": "Koordinater"},
                ],
            )
        ]
    )


def get_coordinate_location(params) -> html.Div:
    return dmc.Stack(
        id="coordinate-location",
        children=[
            dmc.NumberInput(
                id={"id": "latitude", "type": "param"},
                label="Breddegrad",
                hideControls=True,
                decimalSeparator=".",
                decimalScale=6,
                min=-90,
                max=90,
                placeholder=["Grader"],
                value=params["latitude"],
            ),
            dmc.NumberInput(
                id={"id": "longitude", "type": "param"},
                label="Længdegrad",
                hideControls=True,
                decimalSeparator=".",
                decimalScale=6,
                min=-180,
                max=180,
                placeholder=["Grader"],
                value=params["longitude"],
            ),
        ],
    )


def get_address_location(params) -> html.Div:
    return dmc.Stack(
        id="address-location",
        children=[
            dmc.TextInput(
                id={"id": "address", "type": "param"},
                label="Adresse",
                placeholder="Indtast adresse",
                value=params["address"],
            )
        ],
    )


def get_pv_properties(params) -> html.Div:
    return dmc.Stack(
        children=[
            dmc.NumberInput(
                id={"id": "pv_dc_capacity_kW", "type": "param"},
                label="Modulkapacitet (DC) [kW]",
                hideControls=True,
                decimalSeparator=".",
                decimalScale=2,
                min=1e-3,
                max=1e9,
                placeholder=["kW"],
                value=params["pv_dc_capacity_kW"],
                fixedDecimalScale=True,
            ),
            dmc.NumberInput(
                id={"id": "pv_ac_capacity_kW", "type": "param"},
                label="Inverterkapacitet (AC) [kW]",
                hideControls=True,
                decimalSeparator=".",
                decimalScale=2,
                min=0,
                max=1e9,
                placeholder=["kW"],
                value=params["pv_ac_capacity_kW"],
                fixedDecimalScale=True,
            ),
            dmc.NumberInput(
                id={"id": "pv_tilt", "type": "param"},
                label="Hældning (målt fra vandret) [grader]",
                hideControls=True,
                decimalSeparator=".",
                decimalScale=2,
                min=0,
                max=90,
                placeholder=["Grader"],
                value=params["pv_tilt"],
            ),
            dmc.NumberInput(
                id={"id": "pv_azimuth", "type": "param"},
                label="Orientering (målt fra nord) [grader]",
                hideControls=True,
                decimalSeparator=".",
                decimalScale=2,
                min=0,
                max=359,
                placeholder=["Grader"],
                value=params["pv_azimuth"],
            ),
        ]
    )


def get_advanced_pv_properties(params) -> html.Div:
    return dmc.Stack(
        children=[
            dmc.NumberInput(
                id={"id": "pv_efficiency", "type": "param"},
                label="Effektivitet",
                hideControls=True,
                decimalSeparator=".",
                decimalScale=2,
                min=1e-3,
                max=1,
                placeholder=["%"],
                value=params["pv_efficiency"],
                fixedDecimalScale=True,
            ),
        ]
    )


def get_active_pv_parameters(params) -> html.Div:
    return html.Div(
        id="pv-section",
        children=[
            base.get_section(
                name="Placering",
                children=[
                    get_location_choice(params),
                    get_coordinate_location(params),
                    get_address_location(params),
                ],
            ),
            base.get_section(
                name="Egenskaber",
                children=[
                    get_pv_properties(params),
                ],
            ),
            base.get_section(
                name="Avancerede egenskaber",
                children=[
                    get_advanced_pv_properties(params),
                ],
            ),
        ],
    )


def get_pv_panel(params) -> html.Div:
    return base.get_panel(
        name="Solceller",
        children=[
            dmc.Switch(
                label="Ingen solceller",
                id={"id": "no_pv", "type": "param"},
                checked=params["no_pv"],
            ),
            get_active_pv_parameters(params),
        ],
    )


@callback(
    Output("coordinate-location", "style"),
    Output("address-location", "style"),
    Input({"id": "location_choice", "type": "param"}, "value"),
)
def location_choice_toggle(value):
    show = {"display": "block"}
    hide = {"display": "none"}
    match value:
        case "address":
            return hide, show
        case "coordinate":
            return show, hide
    return hide, hide


@callback(
    Output("pv-section", "style"),
    Input({"id": "no_pv", "type": "param"}, "checked"),
)
def pv_toggle(checked: bool):
    show = {"display": "block"}
    hide = {"display": "none"}
    if checked:
        return hide
    return show


@callback(
    Output("pv-section-icon", "children"),
    Input({"id": "no_pv", "type": "param"}, "checked"),
)
def color_pv_icon(checked: bool):
    if checked:
        return DashIconify(icon="ic:twotone-wb-sunny")
    return DashIconify(icon="ic:twotone-wb-sunny", color="#FAB005")
