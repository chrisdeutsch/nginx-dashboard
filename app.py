import dash_bootstrap_components as dbc
from dash import Dash

from nginx_dashboard.callbacks import update_dashboard  # noqa: F401
from nginx_dashboard.layout import get_layout

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = get_layout()


if __name__ == "__main__":
    app.run(debug=True)
