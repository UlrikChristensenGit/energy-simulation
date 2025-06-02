import dash_mantine_components as dmc
from dash import Input, Output, callback, html


def get_default_section(params) -> html.Div:
    return html.Div(
        id="default-section",
        children=[
            dmc.Stack(
                gap="xs",
                children=[
                    dmc.Select(
                        id={"id": "num_adults", "type": "param"},
                        value=str(params["num_adults"]),
                        label="Antal voksne",
                        data=[{"value": str(i), "label": str(i)} for i in range(1, 10)],
                    ),
                    dmc.Select(
                        id={"id": "num_children", "type": "param"},
                        value=str(params["num_children"]),
                        label="Antal børn",
                        data=[{"value": str(i), "label": str(i)} for i in range(0, 10)],
                    ),
                ],
            )
        ],
    )


def get_manual_section(params) -> html.Div:
    return html.Div(id="manual-section")


def get_datahub_section(params) -> html.Div:
    return html.Div(id="datahub-section")


def get_data_type(params) -> html.Div:
    return dmc.Stack(
        children=[
            dmc.SegmentedControl(
                id={"id": "consumption_data_choice", "type": "param"},
                value=params["consumption_data_choice"],
                data=[
                    {"value": "default", "label": "Gennemsnitlig"},
                    {"value": "manual", "label": "Upload"},
                    {"value": "datahub", "label": "Via ElOverblik"},
                ],
            )
        ]
    )


def get_price_area(params):
    return dmc.Stack(
        children=[
            dmc.SegmentedControl(
                id={"id": "price_area", "type": "param"},
                value=params["price_area"],
                data=[
                    {"value": "DK1", "label": "Østdanmark"},
                    {"value": "DK2", "label": "Vestdanmark"},
                ],
            ),
        ]
    )


def get_consumption_panel(params) -> html.Div:
    return dmc.Stack(
        children=[
            dmc.Text("Prisområde", c="blue"),
            get_price_area(params),
            dmc.Text("Data", c="blue"),
            get_data_type(params),
            get_default_section(params),
            get_manual_section(params),
            get_datahub_section(params),
        ]
    )


@callback(
    Output("default-section", "style"),
    Output("manual-section", "style"),
    Output("datahub-section", "style"),
    Input({"id": "consumption_data_choice", "type": "param"}, "value"),
)
def data_choice_toggle(tense: str):
    """
    Show or hide the absolute/relative time travel filter
    depending on the selected time travel type
    """
    hide = {"display": "none"}
    show = {"display": "block"}
    match tense:
        case "default":
            return show, hide, hide
        case "manual":
            return hide, show, hide
        case "datahub":
            return hide, hide, show
    return hide, hide, hide
