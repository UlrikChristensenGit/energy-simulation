import dash_mantine_components as dmc
from dash import html


def make_balance_sheet(metrics: dict[str, float]) -> html.Div:
    return dmc.Table(
        children=[
            dmc.TableTbody(
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
                            dmc.TableTd(metrics["consumption_J"], fw=700),
                            dmc.TableTd("234.567", fw=700),
                        ]
                    ),
                    dmc.TableTr(
                        children=[
                            dmc.TableTd("Fra nettet"),
                            dmc.TableTd(metrics["grid_to_consumption_J"]),
                            dmc.TableTd("- 234.567", c="red"),
                        ]
                    ),
                    dmc.TableTr(
                        children=[
                            dmc.TableTd("Fra solceller"),
                            dmc.TableTd(metrics["pv_to_consumption_J"]),
                            dmc.TableTd("234.567", c="green"),
                        ]
                    ),
                    dmc.TableTr(
                        children=[
                            dmc.TableTd("Fra batteri"),
                            dmc.TableTd(metrics["battery_to_consumption_J"]),
                            dmc.TableTd("234.567"),
                        ]
                    ),
                    dmc.TableTr(
                        children=[
                            dmc.TableTd("Overskudsproduktion", fw=700),
                            dmc.TableTd(metrics["pv_to_grid_J"], fw=700),
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
        ]
    )
