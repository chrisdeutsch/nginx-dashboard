import dash_bootstrap_components as dbc
from dash import dcc, html


def get_layout():
    return dbc.Container(
        [
            get_selector(),
            get_header("Title of my Dash App"),
            html.Hr(),
            get_cards(),
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
    card_1 = dbc.Card(
        [
            html.H4("", className="card-title", id="bad-requests"),
            html.P("Fraction of bad requests", className="card-text"),
        ],
        body=True,
        color="light",
    )

    card_2 = dbc.Card(
        [
            html.H4("", className="card-title", id="requests"),
            html.P("Requests", className="card-text"),
        ],
        body=True,
        color="dark",
        inverse=True,
    )

    card_3 = dbc.Card(
        [
            html.H4("", className="card-title", id="visitors"),
            html.P("Unique visitors", className="card-text"),
        ],
        body=True,
        color="primary",
        inverse=True,
    )

    return dbc.Row([dbc.Col(card, md=4) for card in (card_1, card_2, card_3)])


def get_graphs():
    graph_1 = dcc.Graph("graph-1")
    graph_2 = dcc.Graph("graph-2")

    return dbc.Row(
        [
            dbc.Col(graph_1, md=6),
            dbc.Col(graph_2, md=6),
        ]
    )
