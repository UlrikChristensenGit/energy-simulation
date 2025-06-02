import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

from . import sections


def get_form(params) -> html.Div:
    return dmc.Stack(
        children=[
            dmc.Tabs(
                value="consumption",
                children=[
                    dmc.TabsList(
                        justify="center",
                        grow=True,
                        children=[
                            dmc.TabsTab(
                                children=dmc.Text("Forbrug"),
                                value="consumption",
                                leftSection=DashIconify(
                                    icon="ic:twotone-other-houses", color="#228BE6"
                                ),
                            ),
                            dmc.TabsTab(
                                children=dmc.Text("Solceller"),
                                value="pv",
                                leftSection=html.Div(id="pv-section-icon"),
                            ),
                            dmc.TabsTab(
                                children=dmc.Text("Batteri"),
                                value="battery",
                                leftSection=html.Div(id="battery-section-icon"),
                            ),
                        ],
                    ),
                    dmc.TabsPanel(
                        value="consumption",
                        children=dmc.Group(
                            pt="md",
                            grow=True,
                            children=sections.get_consumption_panel(params),
                        ),
                    ),
                    dmc.TabsPanel(
                        value="pv",
                        children=dmc.Group(
                            pt="md",
                            grow=True,
                            children=sections.get_pv_panel(params),
                        ),
                    ),
                    dmc.TabsPanel(
                        value="battery",
                        children=dmc.Group(
                            pt="md",
                            grow=True,
                            children=sections.get_battery_panel(params),
                        ),
                    ),
                ],
            ),
            #dmc.Button(
            #    id="run-simulation",
            #    leftSection=DashIconify(icon="ic:baseline-refresh"),
            #    children="Kør simulering",
            #)
        ],
    )
