import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

from . import panels


def get_tab(name: str, icon: DashIconify) -> dmc.TabsTab:
    return dmc.TabsTab(
        children=dmc.Text(name),
        value=name,
        leftSection=icon,
    )


def get_panel(name: str, content: html.Div) -> dmc.TabsPanel:
    return dmc.TabsPanel(
        value=name,
        pt="md",
        children=content,
    )


def get_form(params) -> html.Div:
    return dmc.Tabs(
        value="Forbrug",
        children=[
            dmc.TabsList(
                justify="center",
                grow=True,
                children=[
                    get_tab(
                        name="Forbrug",
                        icon=DashIconify(
                            icon="ic:twotone-other-houses", color="#228BE6"
                        ),
                    ),
                    get_tab(
                        name="Solceller",
                        icon=html.Div(
                            id="pv-section-icon"
                        ),  # placeholder for dynamic icon
                    ),
                    get_tab(
                        name="Batteri",
                        icon=html.Div(
                            id="battery-section-icon"
                        ),  # placeholder for dynamic icon
                    ),
                ],
            ),
            panels.get_consumption_panel(params),
            get_panel(name="Solceller", content=panels.get_pv_panel(params)),
            panels.get_battery_panel(params),
        ],
    )
