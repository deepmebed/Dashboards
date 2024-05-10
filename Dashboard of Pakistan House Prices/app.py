import dash
import dash_bootstrap_components as dbc 
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from pages import home, dashboard, predictions
from app_config import app
# from dashboard import layout as dashboard_layout


# Navbar Structure
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/", active='exact')),
        dbc.NavItem(dbc.NavLink("Dashboard", href="/dashboard", active='exact')),
        dbc.NavItem(dbc.NavLink("Predictions", href="/predictions", active='exact'))
    ],
    brand="House Pricing Dashboard",
    brand_href="/",
    color="primary",
    dark=True,
)

# Basic App Layout with Navigation
# Updated App Layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),  
    navbar,  # Include the navbar
    html.Div(id='page-content')
])

# Callback to update page content based on the URL
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/dashboard':
        return dashboard.layout
    elif pathname == '/predictions':
        return predictions.layout
    else:  # Default to homepage
        return home.layout





if __name__ == '__main__':
    app.run_server(debug=True) 
