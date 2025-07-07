import dash_mantine_components as dmc
from dash import Input, Output, callback, dcc, html

from . import base


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


def get_step(num: int, title: str, description: str = None):
    return dmc.Stack(
        gap=0,
        children=[
            dmc.Group(
                align="flex-start",
                children=[
                    dmc.Text(
                        children=str(num),
                        style={
                            "display": "flex",
                            "justify-content": "center",
                            "align-items": "center",
                            "width": "30px",
                            "height": "30px",
                            "border-radius": "50%",
                            "border-width": "1px",
                            "border-style": "solid",
                            "border-color": dmc.theme.DEFAULT_THEME["colors"]["gray"][
                                4
                            ],
                        },
                    ),
                    dmc.Stack(
                        children=[
                            title,
                            description,
                        ]
                    ),
                ],
            ),
        ],
    )


def get_manual_section(params) -> html.Div:
    return html.Div(
        id="manual-section",
        children=[
            dmc.Stack(
                children=[
                    dmc.Stack(
                        gap="xs",
                        children=[
                            get_step(
                                1,
                                dmc.Box(
                                    children=[
                                        dmc.Text("Login på ", span=True),
                                        html.A(
                                            "ElOverblik.dk",
                                            href="https://eloverblik.dk/",
                                            style={
                                                "text-decoration": "none",
                                                "color": dmc.theme.DEFAULT_THEME[
                                                    "colors"
                                                ]["blue"][6],
                                            },
                                        ),
                                    ]
                                ),
                            ),
                            get_step(
                                2,
                                dmc.Box(
                                    children=[
                                        dmc.Text("Klik på ", span=True),
                                        dmc.Text("Download", fs="italic", span=True),
                                        dmc.Text(" og vælg ", span=True),
                                        dmc.Text("Forbrug", fs="italic", span=True),
                                    ]
                                ),
                            ),
                            get_step(
                                num=3,
                                title=dmc.Box(
                                    children=[
                                        dmc.Box(
                                            children=[
                                                dmc.Text(
                                                    "Sæt følgende filtre og tryk ",
                                                    span=True,
                                                ),
                                                dmc.Text(
                                                    "Download ", fs="italic", span=True
                                                ),
                                            ]
                                        ),
                                    ]
                                ),
                                description=dmc.List(
                                    children=[
                                        dmc.ListItem(
                                            dmc.Box(
                                                [
                                                    dmc.Text(
                                                        "Fra dato",
                                                        fs="italic",
                                                        span=True,
                                                    ),
                                                    dmc.Text(
                                                        " til ønsket start", span=True
                                                    ),
                                                ]
                                            )
                                        ),
                                        dmc.ListItem(
                                            dmc.Box(
                                                [
                                                    dmc.Text(
                                                        "Til dato",
                                                        fs="italic",
                                                        span=True,
                                                    ),
                                                    dmc.Text(
                                                        " til ønsket slut", span=True
                                                    ),
                                                ]
                                            )
                                        ),
                                        dmc.ListItem(
                                            dmc.Box(
                                                [
                                                    dmc.Text(
                                                        "Tidsoplsøning",
                                                        fs="italic",
                                                        span=True,
                                                    ),
                                                    dmc.Text(" til ", span=True),
                                                    dmc.Text("Time", fw=700, span=True),
                                                ]
                                            )
                                        ),
                                        dmc.ListItem(
                                            dmc.Box(
                                                [
                                                    dmc.Text(
                                                        "Format", fs="italic", span=True
                                                    ),
                                                    dmc.Text(" til ", span=True),
                                                    dmc.Text("CSV", fw=700, span=True),
                                                ]
                                            )
                                        ),
                                    ]
                                ),
                            ),
                            get_step(
                                num=4,
                                title=dmc.Text("Upload fil herunder"),
                                description=dmc.Group(
                                    grow=True,
                                    children=dcc.Upload(
                                        children=dmc.Stack(
                                            children=[
                                                dmc.Text("Træk og slip en fil eller"),
                                                dmc.Button("Vælg en fil"),
                                            ]
                                        ),
                                        accept=".csv",
                                        style={
                                            "padding": "30px",
                                            "border-width": "1px",
                                            "border-style": "dashed",
                                            "border-radius": "5px",
                                            "border-color": dmc.theme.DEFAULT_THEME[
                                                "colors"
                                            ]["gray"][4],
                                        },
                                    ),
                                ),
                            ),
                        ],
                    ),
                ]
            )
        ],
    )


def get_data_type(params) -> html.Div:
    return dmc.Stack(
        children=[
            dmc.SegmentedControl(
                id={"id": "consumption_data_choice", "type": "param"},
                value=params["consumption_data_choice"],
                data=[
                    {"value": "default", "label": "Gennemsnitlig"},
                    {"value": "manual", "label": "Via ElOverblik"},
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
    return base.get_panel(
        name="Forbrug",
        children=[
            base.get_section(name="Prisområde", children=[get_price_area(params)]),
            base.get_section(
                name="Data",
                children=[
                    get_data_type(params),
                    get_default_section(params),
                    get_manual_section(params),
                ],
            ),
        ],
    )


@callback(
    Output("default-section", "style"),
    Output("manual-section", "style"),
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
            return show, hide
        case "manual":
            return hide, show
    return hide, hide
