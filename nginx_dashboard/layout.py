from collections import namedtuple

import dash_bootstrap_components as dbc
from dash import dcc, html


def get_layout():
    return dbc.Container(
        [
            get_selector(),
            get_header("NGINX Dashboard"),
            html.Hr(),
            *get_cards(),
            html.Br(),
            get_graphs(),
        ]
    )


def get_selector():
    label = dbc.Label("")
    dropdown = dcc.Dropdown(
        id="date-range",
        options=[
            {"label": f"Last {days} days", "value": days} for days in [7, 30, 120]
        ],
        value=7,
        style={"marginTop": 12},
    )

    return dbc.Row(
        [dbc.Col(label, md=1), dbc.Col(dropdown, md=3)], justify="end", align="center"
    )


def get_header(title):
    title = html.H1(title, style={"marginTop": 12})
    logo = html.Img(
        src="https://upload.wikimedia.org/wikipedia/commons/c/c5/Nginx_logo.svg",
        style={"float": "right", "height": 30, "marginTop": 12},
    )
    return dbc.Row([dbc.Col(title, md=9), dbc.Col(logo, md=3)], align="center")


def get_cards():
    CardConfig = namedtuple("CardConfig", ["id", "desc", "kwargs"])

    card_configs = [
        CardConfig("total-requests", "Total Requests", {"color": "primary"}),
        CardConfig("valid-requests", "Valid Requests", {"color": "success"}),
        CardConfig("failed-requests", "Failed Requests", {"color": "warning"}),
        CardConfig("unique-visitors", "Unique Visitors", {"color": "light"}),
        CardConfig("referrers", "Referrers", {"color": "light"}),
        CardConfig("not-found", "Not Found", {"color": "light"}),
    ]

    cards = []
    for card_config in card_configs:
        card = dbc.Card(
            [
                html.H4("", className="card-title", id=card_config.id),
                html.P(card_config.desc, className="card-text"),
            ],
            body=True,
            **card_config.kwargs,
        )

        cards.append(card)

    return [
        dbc.Row([dbc.Col(card, md=4) for card in cards[:3]]),
        html.Br(),
        dbc.Row([dbc.Col(card, md=4) for card in cards[3:]]),
    ]


def get_graphs():
    graph_1 = dcc.Graph("graph-1")
    graph_2 = dcc.Graph("graph-2")

    return dbc.Row(
        [
            dbc.Col(graph_1, xs=12, lg=6),
            dbc.Col(graph_2, xs=12, lg=6),
        ]
    )
