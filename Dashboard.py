import dash
from dash import dcc, html
from dash.dependencies import Input, Output

import plotly.graph_objs as go
import numpy as np

from data_loader import get_sorted_records, load_record
from processor import get_channel, get_window, compute_average
from cache import get_from_cache, set_cache

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H2("ICU Signal Dashboard"),

    dcc.Input(
        id="patient-path",
        type="text",
        placeholder="Enter patient folder path",
        style={"width": "60%"}
    ),

    html.Button("Load Records", id="load-btn"),

    html.Br(), html.Br(),

    dcc.Dropdown(id="record-dropdown", placeholder="Select record"),

    html.Br(),

    dcc.Dropdown(
        id="channel-dropdown",
        placeholder="Select signal",
    ),

    html.Br(),

    dcc.RadioItems(
        id="mode",
        options=[
            {"label": "5 seconds", "value": "5"},
            {"label": "30 seconds", "value": "30"},
            {"label": "Average", "value": "avg"},
        ],
        value="5",
        labelStyle={"display": "inline-block", "margin-right": "15px"}
    ),

    dcc.Graph(id="signal-plot"),

    html.Div(id="output-text", style={"marginTop": "20px", "fontSize": 18})
])


# ---------- LOAD RECORD LIST ----------
@app.callback(
    Output("record-dropdown", "options"),
    Input("load-btn", "n_clicks"),
    Input("patient-path", "value")
)
def load_records(n_clicks, patient_path):
    if not patient_path:
        return []

    try:
        records = get_sorted_records(patient_path)
        return [{"label": r, "value": r} for r in records]
    except:
        return []


# ---------- LOAD CHANNELS (WITH NAMES) ----------
@app.callback(
    Output("channel-dropdown", "options"),
    Input("record-dropdown", "value"),
    Input("patient-path", "value")
)
def load_channels(record_name, patient_path):
    if not record_name:
        return []

    key = f"{patient_path}_{record_name}"

    data = get_from_cache(key)
    if data is None:
        signal, fs, sig_names = load_record(patient_path, record_name)
        set_cache(key, (signal, fs, sig_names))
    else:
        signal, fs, sig_names = data

    # fallback if names missing
    options = []
    for i in range(len(sig_names)):
        label = sig_names[i] if sig_names[i] else f"Channel {i}"
        options.append({"label": label, "value": i})

    return options


# ---------- MAIN UPDATE ----------
@app.callback(
    Output("signal-plot", "figure"),
    Output("output-text", "children"),
    Input("record-dropdown", "value"),
    Input("channel-dropdown", "value"),
    Input("mode", "value"),
    Input("patient-path", "value")
)
def update(record_name, channel_idx, mode, patient_path):

    if not record_name or channel_idx is None:
        return {}, ""

    key = f"{patient_path}_{record_name}"

    data = get_from_cache(key)
    if data is None:
        signal, fs, sig_names = load_record(patient_path, record_name)
        set_cache(key, (signal, fs, sig_names))
    else:
        signal, fs, sig_names = data

    channel = get_channel(signal, channel_idx)

    if mode == "avg":
        avg = compute_average(channel)
        return {}, f"Average ({sig_names[channel_idx]}): {avg:.4f}"

    seconds = int(mode)
    segment = get_window(channel, fs, seconds)

    time_axis = np.arange(len(segment)) / fs

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=time_axis, y=segment, mode="lines"))

    fig.update_layout(
        title=f"{seconds}-Second Signal ({sig_names[channel_idx]})",
        xaxis_title="Time (seconds)",
        yaxis_title="Amplitude"
    )

    return fig, ""


# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)