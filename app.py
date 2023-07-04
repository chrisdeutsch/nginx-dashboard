import dash_bootstrap_components as dbc
from dash import Dash

from nginx_dashboard.callbacks import register_callbacks
from nginx_dashboard.layout import get_layout

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = get_layout()
register_callbacks(app)


if __name__ == "__main__":
    app.run(debug=True)
