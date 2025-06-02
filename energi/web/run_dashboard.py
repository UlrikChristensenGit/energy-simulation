import dash_mantine_components as dmc
import dotenv
from dash import Dash, _dash_renderer

from dashboard import pages, shell

dotenv.load_dotenv("/home/uch/Energi/energi/web/.env")

from logs import get_logger

logger = get_logger(__name__)


_dash_renderer._set_react_version("18.2.0")


stylesheets = [
    "https://unpkg.com/@mantine/dates@7/styles.css",
    "https://unpkg.com/@mantine/code-highlight@7/styles.css",
    "https://unpkg.com/@mantine/charts@7/styles.css",
    "https://unpkg.com/@mantine/carousel@7/styles.css",
    "https://unpkg.com/@mantine/notifications@7/styles.css",
    "https://unpkg.com/@mantine/nprogress@7/styles.css",
    dmc.styles.CHARTS,
]

app = Dash(
    __name__, suppress_callback_exceptions=True, external_stylesheets=stylesheets
)

app.layout = dmc.MantineProvider(shell.layout.get_layout())

if __name__ == "__main__":

    app.run(debug=True)
