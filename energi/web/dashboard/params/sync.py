import dash
from dash import ALL, Input, Output, State, callback


@callback(
    Output("params", "data"),
    Input({"id": ALL, "type": "param"}, "value"),
    Input({"id": ALL, "type": "param"}, "checked"),
    State("params", "data"),
    prevent_initial_call=True,
)
def update_params(
    _1: list,
    _2: list,
    current_params: dict,
) -> tuple:
    """
    Update parameters with choosen filter values
    """
    all_inputs = (
        dash.callback_context.inputs_list[0] + dash.callback_context.inputs_list[1]
    )

    value_inputs = [input_ for input_ in all_inputs if "value" in input_]

    updated_params = {input_["id"]["id"]: input_["value"] for input_ in value_inputs}

    current_params.update(updated_params)

    return current_params
