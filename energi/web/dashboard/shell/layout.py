import datetime as dt

import dash_mantine_components as dmc
from dash import dcc, html
from dash_iconify import DashIconify

from dashboard.params.default import DEFAULT_PARAMS


def get_link_sharing() -> dmc.Flex:
    """
    Make link sharing section
    """
    return dmc.Button(
        id="share-button",
        children="Kopiér link",
        leftSection=DashIconify(icon="ic:baseline-share"),
    )


def get_logo() -> dmc.Anchor:
    """
    Make website logo section
    """
    return dmc.Anchor(
        children="G☀️D S🌤️L · DK",
        size="xl",
        href="/",
        underline=False,
    )


def get_header() -> dmc.AppShellHeader:
    """
    Make website header
    """
    return dmc.AppShellHeader(
        px="xl",
        children=[
            dmc.Flex(
                h="100%",
                align="center",
                justify="space-between",
                children=[
                    get_logo(),
                    get_link_sharing(),
                ],
            ),
        ],
    )


def get_main() -> dmc.AppShellMain:
    """
    Make main content
    """
    return dmc.AppShellMain(
        id="main",
        px="xl",
        bg=dmc.theme.DEFAULT_THEME["colors"]["gray"][1],
        children=[],
    )


def get_layout() -> html.Div:
    """
    Make layout for application shell
    """
    return (
        html.Div(
            children=[
                # The `Location` element makes it possible
                # to make callbacks acting on URL change
                dcc.Location(id="url", refresh=False),
                dcc.Store(id="params", storage_type="session", data=DEFAULT_PARAMS),
                # Make application shell containing
                # header, footer, navigation bar and aside
                dmc.AppShell(
                    header={"height": "80px"},
                    children=[
                        dcc.Clipboard(id="clipboard"),
                        get_header(),
                        get_main(),
                    ],
                ),
            ],
        ),
    )
