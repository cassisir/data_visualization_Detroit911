import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import dash_labs as dl
from dashboard_utils import H1_style

app = Dash(__name__, pages_folder="pages", use_pages=True, external_stylesheets=[dbc.themes.CYBORG])

navbar = dbc.Navbar([
            dbc.Nav(
                    [
                        dbc.NavItem(dbc.NavLink(page["name"], href=page["path"]), style={'font-size':'20px'}, className="mr-5")
                        for page in dash.page_registry.values()
                        if page["module"] != "pages.not_found_404"
                    ],
                    navbar=True,
                    className="mx-auto"
                ),
            ],
            color="dark", 
            dark=True, 
            className="mb-4",
)

app.layout = dbc.Container([
    html.H1('Detroit 911 Calls',
            style=H1_style,
            className='text-center font-weight-bold, mb-4',
    ),
    navbar, 
    dash.page_container
], fluid=True)

if __name__ == '__main__':
    app.run(debug=False)