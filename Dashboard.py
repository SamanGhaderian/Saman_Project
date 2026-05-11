import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

import plotly.graph_objs as go
import numpy as np

from data_loader import load_patient_data, resample_windows
from cache import get_from_cache, set_cache

app = dash.Dash(__name__)


# =========================
# LAYOUT
# =========================
app.layout = html.Div([

    html.H2("ICU Signal Dashboard (v4 - Continuous Timeline)"),

    dcc.Input(
        id="patient-path",
        type="text",
        placeholder="Enter patient folder path",
        style={"width": "60%"}
    ),

    html.Button("Load Patient", id="load-btn"),

    html.Br(), html.Br(),

    dcc.Dropdown(
        id="channel-dropdown",
        placeholder="Select signal"
    ),

    html.Br(),

    dcc.RadioItems(
        id="mode",
        options=[
            {"label": "Full Signal", "value": "full"},
            {"label": "5 Second Windows", "value": "5"},
            {"label": "30 Second Windows", "value": "30"},
            {"label": "Average", "value": "avg"},
        ],
        value="5",
        labelStyle={"display": "inline-block", "margin-right": "15px"}
    ),

    html.Br(),

    dcc.Graph(id="signal-plot"),

    html.Div(id="output-text", style={"marginTop": "20px", "fontSize": 18})
])


# =========================
# LOAD PATIENT
# =========================
@app.callback(
    Output("channel-dropdown", "options"),
    Input("load-btn", "n_clicks"),
    State("patient-path", "value")
)
def load_patient(n_clicks, patient_path):

    if not patient_path:
        return []

    key = f"patient_{patient_path}"

    df = get_from_cache(key)

    if df is None:
        df = load_patient_data(patient_path)
        set_cache(key, df)

    channels = [c for c in df.columns if c != "time"]

    return [{"label": ch, "value": ch} for ch in channels]


# =========================
# UPDATE PLOT
# =========================
@app.callback(
    Output("signal-plot", "figure"),
    Output("output-text", "children"),
    Input("channel-dropdown", "value"),
    Input("mode", "value"),
    State("patient-path", "value")
)
def update_plot(channel, mode, patient_path):

    if not channel or not patient_path:
        return {}, ""

    key = f"patient_{patient_path}"
    df = get_from_cache(key)

    if df is None:
        df = load_patient_data(patient_path)
        set_cache(key, df)

    time = df["time"]
    signal = df[channel]

    # =========================
    # MODE: AVG
    # =========================
    if mode == "avg":
        avg = signal.mean()
        return {}, f"Average {channel}: {avg:.4f}"


    # =========================
    # MODE: FULL SIGNAL
    # =========================
    if mode == "full":
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=time,
            y=signal,
            mode="lines"
        ))

        fig.update_layout(
            title=f"Full ICU Signal - {channel}",
            xaxis_title="Time (seconds)",
            yaxis_title="Amplitude"
        )

        return fig, ""


    # =========================
    # MODE: WINDOWED (5s / 30s)
    # =========================
    window_size = int(mode)

    df_windowed = resample_windows(df, window_size)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_windowed["time"],
        y=df_windowed[channel],
        mode="lines"
    ))

    fig.update_layout(
        title=f"{window_size}-Second Windowed Signal - {channel}",
        xaxis_title="Time (seconds)",
        yaxis_title="Mean Amplitude"
    )

    return fig, ""


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(debug=True)