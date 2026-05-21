import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import os

from data_loader import load_patient_windows


CACHE_ROOT = "cache"


# =========================
# PATIENT VALIDATION SYSTEM
# =========================
def validate_patients():
    valid = []
    invalid = []

    if not os.path.exists(CACHE_ROOT):
        return [], ["Cache folder not found"]

    for p in os.listdir(CACHE_ROOT):

        patient_path = os.path.join(CACHE_ROOT, p)

        if not os.path.isdir(patient_path):
            continue

        files = os.listdir(patient_path)

        # must have at least one parquet file
        parquet_files = [f for f in files if f.endswith(".parquet")]

        if len(parquet_files) == 0:
            invalid.append((p, "No parquet files"))
            continue

        # check at least one usable file
        try:
            df = load_patient_windows(p, "5s")
            if df is None or df.empty:
                invalid.append((p, "Empty dataset"))
            else:
                valid.append(p)

        except Exception as e:
            invalid.append((p, str(e)))

    return valid, invalid


VALID_PATIENTS, INVALID_PATIENTS = validate_patients()


# =========================
# APP
# =========================
app = dash.Dash(__name__)


# =========================
# LAYOUT
# =========================
app.layout = html.Div([

    html.H2("ICU Multi-Patient Dashboard (Validated Cache System)"),

    # =========================
    # PATIENT SELECTOR
    # =========================
    html.Label("Select Valid Patients"),

    dcc.Dropdown(
        id="patient-selector",
        options=[
            {
                "label": p,
                "value": p,
                "title": "Valid patient (cached and ready)"  # tooltip
            }
            for p in VALID_PATIENTS
        ],
        multi=True,
        placeholder="Only validated patients shown"
    ),

    html.Br(),

    # =========================
    # CHANNEL SELECTOR
    # =========================
    dcc.Dropdown(
        id="channel-dropdown",
        placeholder="Select signal"
    ),

    html.Br(),

    # =========================
    # MODE
    # =========================
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

    # =========================
    # TIME MODE
    # =========================
    dcc.RadioItems(
        id="time-mode",
        options=[
            {"label": "Absolute Time", "value": "absolute"},
            {"label": "Normalized Time (0–1)", "value": "normalized"},
        ],
        value="normalized",
        labelStyle={"display": "inline-block", "margin-right": "15px"}
    ),

    html.Br(),

    # =========================
    # LOADING STATUS PANEL
    # =========================
    html.Div(id="loading-status", style={
        "whiteSpace": "pre-line",
        "backgroundColor": "#f4f4f4",
        "padding": "10px",
        "borderRadius": "8px"
    }),

    html.Br(),

    # =========================
    # SKIP REPORT PANEL
    # =========================
    html.Div([
        html.H4("Skipped / Invalid Patients"),
        html.Div([
            html.Div(f"{p} → {reason}") for p, reason in INVALID_PATIENTS
        ])
    ], style={
        "backgroundColor": "#fff3f3",
        "padding": "10px",
        "border": "1px solid #ffcccc",
        "borderRadius": "8px"
    }),

    html.Br(),

    dcc.Graph(id="signal-plot"),
])


# =========================
# CHANNEL OPTIONS
# =========================
@app.callback(
    Output("channel-dropdown", "options"),
    Input("patient-selector", "value")
)
def load_channels(selected):

    if not selected or len(selected) < 2:
        return []

    dfs = []

    for p in selected[:2]:
        df = load_patient_windows(p, "5s")
        if df is not None and not df.empty:
            dfs.append(df)

    if len(dfs) < 2:
        return []

    common = set(dfs[0].columns)

    for df in dfs[1:]:
        common = common.intersection(set(df.columns))

    common.discard("time")

    return [{"label": c, "value": c} for c in sorted(common)]


# =========================
# PLOT + LOADING STATUS
# =========================
@app.callback(
    Output("signal-plot", "figure"),
    Output("loading-status", "children"),
    Input("patient-selector", "value"),
    Input("channel-dropdown", "value"),
    Input("mode", "value"),
    Input("time-mode", "value")
)
def update_plot(patients, channel, mode, time_mode):

    if not patients or not channel:
        return {}, "No patients selected"

    fig = go.Figure()

    status_lines = []

    for p in patients:

        try:
            df = load_patient_windows(p, f"{mode}s")

            if df is None or df.empty:
                status_lines.append(f"❌ {p}: empty dataset")
                continue

            if channel not in df.columns:
                status_lines.append(f"⚠️ {p}: missing channel {channel}")
                continue

            df = df.copy()

            # =========================
            # TIME NORMALIZATION
            # =========================
            if time_mode == "normalized":
                tmin, tmax = df["time"].min(), df["time"].max()

                if tmax == tmin:
                    status_lines.append(f"⚠️ {p}: invalid time range")
                    continue

                df["time"] = (df["time"] - tmin) / (tmax - tmin)

            else:
                df["time"] = df["time"] - df["time"].min()

            fig.add_trace(go.Scatter(
                x=df["time"],
                y=df[channel],
                name=f"Patient {p}"
            ))

            status_lines.append(f"✅ {p}: loaded")

        except Exception as e:
            status_lines.append(f"❌ {p}: error {str(e)}")

    fig.update_layout(
        title=f"{mode}s Window - {channel} ({time_mode})",
        xaxis_title="Time",
        yaxis_title="Value"
    )

    return fig, "\n".join(status_lines)


# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True)