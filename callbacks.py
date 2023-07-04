import datetime
from glob import glob
from parser import parse_log

import pandas as pd
import plotly.express as px
from dash import Input, Output, callback

from preprocessing import preprocess


@callback(
    [
        Output("bad-requests", "children"),
        Output("requests", "children"),
        Output("visitors", "children"),
        Output("graph-1", "figure"),
        Output("graph-2", "figure"),
    ],
    Input("date-range", "value"),
)
def update_dashboard(days):
    infiles = glob("data/access*")
    df = pd.concat([preprocess(parse_log(fn)) for fn in infiles], ignore_index=True)

    current_datetime = datetime.datetime.now(datetime.timezone.utc)
    df_selected = df[
        current_datetime - df["timestamp"] < pd.Timedelta(days, unit="days")
    ].copy()

    bad_requests = (df_selected["status"] != 200).astype(int).mean()
    requests = len(df_selected)
    visitors = df_selected.query("status == 200")["remote_addr"].nunique()

    df_selected["day"] = df["timestamp"].dt.floor("d")
    df_unique_visitors = (
        df_selected.groupby("day")["remote_addr"].nunique().to_frame("unique_visitors")
    )
    g1 = px.bar(df_unique_visitors, x=df_unique_visitors.index, y="unique_visitors")
    g1.update_yaxes(rangemode="tozero")
    g1.update_layout(bargap=0.05)

    g2 = px.line(df_unique_visitors, x=df_unique_visitors.index, y="unique_visitors")
    g2.update_yaxes(rangemode="tozero")

    return (
        "{:.1f} %".format(100 * bad_requests),
        "{}".format(requests),
        "{}".format(visitors),
        g1,
        g2,
    )
