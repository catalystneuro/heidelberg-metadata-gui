import dash
import dash_html_components as html
import dash_bootstrap_components as dbc

from .metadata_forms import MetadataForms
from .navbar import render_navbar


def init_forms(server, converter_class):
    FONT_AWESOME = "https://use.fontawesome.com/releases/v5.7.2/css/all.css"
    external_stylesheets = [dbc.themes.BOOTSTRAP, FONT_AWESOME]
    dash_app = dash.Dash(
        server=server,
        external_stylesheets=external_stylesheets,
        suppress_callback_exceptions=True,
        routes_pathname_prefix='/metadata-forms/',
    )

    navbar = render_navbar()
    # Create Dash Layout
    dash_app.layout = html.Div([
        navbar,
        MetadataForms(parent_app=dash_app, converter_class=converter_class)
    ])
    dash_app.enable_dev_tools(debug=True)

    return dash_app.server
