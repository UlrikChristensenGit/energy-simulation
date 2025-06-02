import dash_mantine_components as dmc
from dash import html

dmc.DEFAULT_THEME
from . import parameters, results


def get_summary(params):
    return dmc.Stack(
        children=[
            dmc.Text("Forbrug (uden solceller og batteri)", c="blue"),
            dmc.Group(
                children=[dmc.Text("Omkostninger"), dmc.Text("123.456 DKK")], ml="xl"
            ),
            dmc.Text("Med solceller", c="blue"),
            dmc.Group(
                children=[dmc.Text("Omkostninger"), dmc.Text("123.456 DKK")], ml="xl"
            ),
            dmc.Group(
                children=[dmc.Text("Besparelse"), dmc.Text("123.456 DKK")], ml="xl"
            ),
            dmc.Text("Med solceller og batteri", c="blue"),
            dmc.Group(
                children=[dmc.Text("Omkostninger"), dmc.Text("123.456 DKK")], ml="xl"
            ),
            dmc.Group(
                children=[dmc.Text("Besparelse"), dmc.Text("123.456 DKK")], ml="xl"
            ),
        ]
    )


def get_summary(params) -> html.Div:
    body = dmc.TableTbody(
        children=[
            dmc.TableTr(
                children=[
                    dmc.TableTd(""),
                    dmc.TableTd("Energi [kWh]", c="gray"),
                    dmc.TableTd("Omkostninger [DKK]", c="gray"),
                ]
            ),
            dmc.TableTr(
                children=[
                    dmc.TableTd("Forbrug", fw=700),
                    dmc.TableTd("123.456", fw=700),
                    dmc.TableTd("234.567", fw=700),
                ]
            ),
            dmc.TableTr(
                children=[
                    dmc.TableTd("Fra nettet"),
                    dmc.TableTd("123.456"),
                    dmc.TableTd("- 234.567", c="red"),
                ]
            ),
            dmc.TableTr(
                children=[
                    dmc.TableTd("Fra solceller"),
                    dmc.TableTd("123.456"),
                    dmc.TableTd("234.567", c="green"),
                ]
            ),
            dmc.TableTr(
                children=[
                    dmc.TableTd("Fra batteri"),
                    dmc.TableTd("123.456"),
                    dmc.TableTd("234.567"),
                ]
            ),
            dmc.TableTr(
                children=[
                    dmc.TableTd("Overskudsproduktion", fw=700),
                    dmc.TableTd("123.456", fw=700),
                    dmc.TableTd("234.567", fw=700),
                ]
            ),
            dmc.TableTr(
                children=[
                    dmc.TableTd("Total", fs="italic"),
                    dmc.TableTd(""),
                    dmc.TableTd("234.567", fs="italic"),
                ]
            ),
            dmc.TableTr(
                children=[
                    dmc.TableTd("Besparelse", fs="italic"),
                    dmc.TableTd(""),
                    dmc.TableTd("234.567", fs="italic"),
                ]
            ),
        ]
    )

    return dmc.Table(children=[body])


def get_metrics(params) -> html.Div:
    return dmc.Grid(
        children=[
            dmc.GridCol(span=6, children=[dmc.Card(id="metrics", children=[])]),
            dmc.GridCol(span=6, children=[dmc.Card(id="summary", children=[])]),
        ]
    )


def get_result_cards(params) -> html.Div:
    return dmc.Grid(
        gutter="xl",
        children=[
            dmc.GridCol(
                span=12,
                children=[
                    dmc.Stack(
                        children=[
                            dmc.Text("Resultater", c="gray"),
                            get_metrics(params),
                            dmc.Card(
                                id="consumption-chart-section",
                                children=[
                                    dmc.Stack(
                                        children=[
                                            dmc.Group(
                                                justify="flex-start",
                                                children=[
                                                    dmc.DatePickerInput(
                                                        id={
                                                            "id": "time_range",
                                                            "type": "param",
                                                        },
                                                        description="Periode",
                                                        value=params["time_range"],
                                                        type="range",
                                                        allowSingleDateInRange=True,
                                                    ),
                                                    dmc.Select(
                                                        id={
                                                            "id": "resolution",
                                                            "type": "param",
                                                        },
                                                        value=params["resolution"],
                                                        description="Aggregering",
                                                        data=[
                                                            {
                                                                "value": "h",
                                                                "label": "Time",
                                                            },
                                                            {
                                                                "value": "D",
                                                                "label": "Dag",
                                                            },
                                                            {
                                                                "value": "W-MON",
                                                                "label": "Uge",
                                                            },
                                                            {
                                                                "value": "ME",
                                                                "label": "Måned",
                                                            },
                                                        ],
                                                    ),
                                                ],
                                            ),
                                            dmc.Text("Forbrug", fw=700),
                                            html.Div(id="consumption-chart"),
                                            dmc.Text("Solcelleproduktion", fw=700),
                                            html.Div(id="pv-generation-chart"),
                                            dmc.Text("Omkostningsbesparelse", fw=700),
                                            html.Div(id="cost-savings-chart"),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            )
        ],
    )


def get_input_cards(params) -> html.Div:
    return dmc.Stack(
        children=[
            dmc.Text("Parametre", c="gray"),
            dmc.Card(parameters.get_form(params)),
        ]
    )


def get_main(params) -> html.Div:
    return dmc.Grid(
        gutter="xl",
        children=[
            dmc.GridCol(
                span=3,
                children=get_input_cards(params),
            ),
            dmc.GridCol(
                span=9,
                children=get_result_cards(params),
            ),
        ],
    )
