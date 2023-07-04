from glob import glob

import pandas as pd
import plotly.express as px
from dash import Input, Output
from flask_caching import Cache

from nginx_dashboard.parser import parse_log
from nginx_dashboard.preprocessing import preprocess


def register_callbacks(app, cache_timeout=900):
    outputs = [
        Output("total-requests", "children"),
        Output("valid-requests", "children"),
        Output("failed-requests", "children"),
        Output("unique-visitors", "children"),
        Output("referrers", "children"),
        Output("not-found", "children"),
        Output("graph-1", "figure"),
        Output("graph-2", "figure"),
    ]

    inputs = [
        Input("date-range", "value"),
    ]

    cache = Cache(
        app.server,
        config={
            "CACHE_TYPE": "filesystem",
            "CACHE_DIR": "cache_dir",
        },
    )

    cached_update_dashboard = cache.memoize(timeout=cache_timeout)(update_dashboard)
    app.callback(outputs, inputs)(cached_update_dashboard)


def update_dashboard(n_days):
    df = get_dataframe(n_days)

    cards = get_cards(df)
    graphs = get_graphs(df)

    return *cards, *graphs


def get_dataframe(n_days):
    infiles = glob("data/access*")
    df = pd.concat([preprocess(parse_log(fn)) for fn in infiles], ignore_index=True)

    # Filter requests from last `n_days` days
    mask = pd.Timestamp.utcnow().floor("d") - df["timestamp"] < pd.Timedelta(
        n_days, unit="days"
    )

    # Adding day column to group by day
    df["day"] = df["timestamp"].dt.floor("d")

    return df.loc[mask]


def get_cards(df):
    total_requests = len(df)
    valid_requests = (df["status"] == 200).sum()
    failed_requests = (df["status"] != 200).sum()
    unique_visitors = (
        df.query("status == 200").groupby("day")["remote_addr"].nunique().sum()
    )
    referrers = df.query("status == 200")["http_referer"].nunique()
    not_found = (df["status"] == 404).sum()

    return (
        str(total_requests),
        str(valid_requests),
        str(failed_requests),
        str(unique_visitors),
        str(referrers),
        str(not_found),
    )


def get_graphs(df):
    df_hits_visitors = (
        df.query("status == 200")
        .groupby("day")["remote_addr"]
        .agg(hits="count", unique_visitors="nunique")
    )

    g1 = px.bar(df_hits_visitors, x=df_hits_visitors.index, y="hits")
    g1.update_yaxes(rangemode="tozero")
    g1.update_layout(bargap=0.05)

    g2 = px.bar(df_hits_visitors, x=df_hits_visitors.index, y="unique_visitors")
    g2.update_yaxes(rangemode="tozero")
    g2.update_layout(bargap=0.05)

    return g1, g2
