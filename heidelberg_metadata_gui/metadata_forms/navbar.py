import dash_html_components as html
import dash_bootstrap_components as dbc


NAV_LOGO = "assets/logo_nwb.png"


def render_navbar():
    """Make Navbar"""
    navbar = dbc.Navbar(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=NAV_LOGO, height="60px"))
                    ],
                    align="center",
                    no_gutters=True,
                ),
                href="/",
                id="nav_brand"
            )
        ],
        color="dark",
        dark=True
    )
    return navbar
