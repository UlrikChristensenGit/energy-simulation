import urllib.parse

from dash import Input, Output, State, callback, html

from dashboard import pages

PAGE_REGISTRY = {"/": pages.simulation.get_main}


@callback(
    Output("main", "children"),
    Output("url", "href"),
    Input("url", "href"),
    State("params", "data"),
)
def fill_shell(url: str, params: dict) -> html.Div:
    """
    Fill the main aside window on the website with
    the content of the given page.
    Potential query parameters are used
    to set the filter values.

    Args:
        pathname (str): Path of subpage
    """
    url_parts = urllib.parse.urlparse(url)
    page_path = url_parts.path
    query_params = urllib.parse.parse_qs(url_parts.query)

    url_parts_without_query = url_parts._replace(query=None)
    url_without_query = urllib.parse.urlunparse(url_parts_without_query)

    main = PAGE_REGISTRY[page_path](params)

    return (main, url_without_query)
