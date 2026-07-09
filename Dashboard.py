import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import numpy as np
import plotly.graph_objs as go
import os

from data_loader import load_patient_windows
from similarity import build_similarity_matrix
from clustering import (
    hierarchical_clustering,
    dbscan_clustering
)
from embedding import compute_umap


CACHE_ROOT = "cache"


# =========================
# VALIDATION
# =========================

def validate_patients():

    valid = []
    invalid = []

    if not os.path.exists(CACHE_ROOT):
        return [], ["Cache missing"]

    for p in os.listdir(CACHE_ROOT):

        patient_path = os.path.join(CACHE_ROOT, p)

        if not os.path.isdir(patient_path):
            continue

        try:

            df = load_patient_windows(
                p,
                "5s"
            )

            if df is None or df.empty:
                invalid.append(
                    (p, "Empty")
                )

            else:
                valid.append(p)

        except Exception as e:

            invalid.append(
                (p, str(e))
            )


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


    html.H2(
        "ICU Dashboard (DTW + Clustering + UMAP)"
    ),


    dcc.Dropdown(
        id="patient-selector",
        options=[
            {
                "label": p,
                "value": p
            }
            for p in VALID_PATIENTS
        ],
        multi=True
    ),


    html.Br(),


    dcc.Dropdown(
        id="channel-dropdown",
        placeholder="Select signal"
    ),


    html.Br(),


    dcc.RadioItems(
        id="mode",
        options=[
            {
                "label": "5s",
                "value": "5"
            },
            {
                "label": "30s",
                "value": "30"
            }
        ],
        value="5"
    ),


    html.Br(),


    dcc.RadioItems(
        id="cluster-method",

        options=[

            {
                "label": "Hierarchical Clustering",
                "value": "hierarchical"
            },

            {
                "label": "DBSCAN",
                "value": "dbscan"
            }

        ],

        value="hierarchical"
    ),


    html.Br(),


    dcc.Graph(
        id="signal-plot"
    ),


    html.Br(),


    html.Button(
        "Run DTW + Clustering + UMAP",
        id="run"
    ),


    html.Br(),
    html.Br(),


    html.Div(
        id="output"
    ),


    html.Br(),


    dcc.Graph(
        id="umap-plot"
    )

])



# =========================
# CHANNEL OPTIONS
# =========================

@app.callback(
    Output(
        "channel-dropdown",
        "options"
    ),

    Input(
        "patient-selector",
        "value"
    )
)

def channels(patients):


    if not patients:
        return []


    dfs = []


    for p in patients[:2]:

        df = load_patient_windows(
            p,
            "5s"
        )

        if df is not None:
            dfs.append(df)



    if len(dfs) < 2:
        return []



    common = set(
        dfs[0].columns
    )


    for d in dfs:
        common &= set(
            d.columns
        )


    common.discard(
        "time"
    )


    return [
        {
            "label": c,
            "value": c
        }

        for c in sorted(common)
    ]



# =========================
# SIGNAL PLOT
# =========================

@app.callback(
    Output(
        "signal-plot",
        "figure"
    ),

    Input(
        "patient-selector",
        "value"
    ),

    Input(
        "channel-dropdown",
        "value"
    ),

    Input(
        "mode",
        "value"
    )
)

def plot(
    patients,
    channel,
    mode
):

    fig = go.Figure()


    if not patients or not channel:
        return fig



    for p in patients:


        df = load_patient_windows(
            p,
            f"{mode}s"
        )


        if df is None or df.empty:
            continue


        if channel not in df:
            continue



        fig.add_trace(

            go.Scatter(

                x=df["time"],

                y=df[channel],

                name=p

            )

        )



    return fig



# =========================
# MAIN PIPELINE
# =========================

@app.callback(

    Output(
        "output",
        "children"
    ),

    Output(
        "umap-plot",
        "figure"
    ),

    Input(
        "run",
        "n_clicks"
    ),

    State(
        "patient-selector",
        "value"
    ),

    State(
        "channel-dropdown",
        "value"
    ),

    State(
        "mode",
        "value"
    ),

    State(
        "cluster-method",
        "value"
    )
)


def run(
    n,
    patients,
    channel,
    mode,
    cluster_method
):


    if not n:
        return "", {}



    if not patients or not channel:
        return "Select inputs", {}



    # =========================
    # DTW
    # =========================

    ids, matrix = build_similarity_matrix(

        patients,

        channel,

        f"{mode}s"

    )
    print("==============================")
    print("DTW DISTANCE DEBUG")

    print("Number of patients:", len(ids))

    positive = matrix[matrix > 0]

    print("Minimum distance:", positive.min())
    print("Maximum distance:", positive.max())
    print("Mean distance:", positive.mean())
    print("Median distance:", np.median(positive))

    print("==============================")

    if len(ids) < 2:
        return "Not enough data", {}



    # =========================
    # CLUSTERING
    # =========================


    if cluster_method == "hierarchical":


        clusters, labels = hierarchical_clustering(

            matrix,

            ids

        )


    else:


        clusters, labels = dbscan_clustering(

            matrix,

            ids,

            eps=1500,

            min_samples=3

        )



    # =========================
    # UMAP
    # =========================

    embedding = compute_umap(
        matrix
    )



    # =========================
    # OUTPUT
    # =========================


    out = [

        f"=== METHOD: {cluster_method.upper()} ===\n"

    ]


    for k, v in clusters.items():

        out.append(

            f"Cluster {k}: {', '.join(v)}"

        )



    # =========================
    # UMAP
    # =========================


    fig = go.Figure()



    for i, pid in enumerate(ids):


        cluster_id = labels[i]


        fig.add_trace(

            go.Scatter(

                x=[
                    embedding[i,0]
                ],

                y=[
                    embedding[i,1]
                ],

                mode="markers+text",

                text=[
                    pid
                ],

                textposition="top center",

                marker=dict(
                    size=12
                ),

                name=f"Cluster {cluster_id}"

            )

        )



    fig.update_layout(

        title=
        "ICU Patient Similarity Map (UMAP)",

        xaxis_title=
        "UMAP-1",

        yaxis_title=
        "UMAP-2"

    )


    return "\n".join(out), fig



# =========================
# RUN
# =========================

if __name__ == "__main__":

    app.run(
        debug=True
    )