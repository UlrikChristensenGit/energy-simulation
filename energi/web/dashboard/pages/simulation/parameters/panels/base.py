import dash_mantine_components as dmc
from dash import html


def get_panel(name: str, children: list[html.Div]) -> html.Div:
    return dmc.TabsPanel(
        value=name,
        pt="md",
        children=dmc.Stack(children),
    )


def get_section(name: str, children: list[html.Div]) -> html.Div:
    return dmc.Stack(
        children=[
            dmc.Text(name, c="blue"),
            *children,
        ],
    )
