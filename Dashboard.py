import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

import plotly.graph_objs as go
import os

from data_loader import load_patient_data, get_resampled_windows

app = dash.Dash(__name__)


# =========================
# LAYOUT
# =========================
app.layout = html.Div([

    html.H2("ICU Multi-Patient Comparison (Window Cache Only)"),

    html.Div([
        html.Label("Patient 1 Path"),
        dcc.Input(id="patient1-path", type="text", style={"width": "45%"})
    ]),

    html.Br(),

    html.Div([
        html.Label("Patient 2 Path"),
        dcc.Input(id="patient2-path", type="text", style={"width": "45%"})
    ]),

    html.Br(),

    html.Button("Load Patients", id="load-btn"),

    html.Br(), html.Br(),

    dcc.Dropdown(
        id="channel-dropdown",
        placeholder="Select signal"
    ),

    html.Br(),

    dcc.RadioItems(
        id="mode",
        options=[
            {"label": "5 Second Windows", "value": "5"},
            {"label": "30 Second Windows", "value": "30"},
        ],
        value="5",
        labelStyle={"display": "inline-block", "margin-right": "15px"}
    ),

    html.Br(),

    dcc.Graph(id="signal-plot"),

    html.Div(id="output-text")
])


# =========================
# LOAD PATIENTS (NO FULL CACHE)
# =========================
@app.callback(
    Output("channel-dropdown", "options"),
    Input("load-btn", "n_clicks"),
    State("patient1-path", "value"),
    State("patient2-path", "value")
)
def load_patients(n_clicks, p1, p2):

    if not p1 or not p2:
        return []

    df1 = load_patient_data(p1)
    df2 = load_patient_data(p2)

    channels = set(df1.columns).intersection(set(df2.columns))
    channels.discard("time")

    return [{"label": c, "value": c} for c in sorted(channels)]


# =========================
# PLOT (WINDOW CACHE ONLY)
# =========================
@app.callback(
    Output("signal-plot", "figure"),
    Output("output-text", "children"),
    Input("channel-dropdown", "value"),
    Input("mode", "value"),
    State("patient1-path", "value"),
    State("patient2-path", "value")
)
def update_plot(channel, mode, p1, p2):

    if not channel or not p1 or not p2:
        return {}, ""

    df1 = load_patient_data(p1)
    df2 = load_patient_data(p2)

    id1 = os.path.basename(p1)
    id2 = os.path.basename(p2)

    window_size = int(mode)

    df1_w = get_resampled_windows(id1, df1, window_size)
    df2_w = get_resampled_windows(id2, df2, window_size)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df1_w["time"],
        y=df1_w[channel],
        name="Patient 1"
    ))

    fig.add_trace(go.Scatter(
        x=df2_w["time"],
        y=df2_w[channel],
        name="Patient 2"
    ))

    fig.update_layout(
        title=f"{window_size}s Window Comparison - {channel}",
        xaxis_title="Time (seconds)",
        yaxis_title="Mean Amplitude"
    )

    return fig, ""


# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True)