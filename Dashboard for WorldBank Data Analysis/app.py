import dash
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc


app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True) 
# (later) make: suppress_callback_exceptions=True

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "padding": "2rem 1rem",
    "background-color": "#f5f5f5",
}

# add some padding.
CONTENT_STYLE = {
    "margin-left": "22rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


sidebar = html.Div(
    [
        html.H2("World Bank Data", className="display-5 text-center"),
        html.Hr(),
        
        
        html.Div(
            [
                dbc.Accordion(
                [
                    dbc.AccordionItem(
                        [
                            dbc.Nav([
                                dbc.NavLink("Population Overview", href="/", active="exact", class_name="link-dark "),
                                dbc.NavLink("Population Intensity", href="/population/intense", active="exact", class_name="link-dark"),
                                dbc.NavLink("Population Trend", href="/population/trend", active="exact", class_name="link-dark"),
                                dbc.NavLink("Population Comparison", href="/population/compare", active="exact", class_name="link-dark"),
                            ],

                            vertical=True,
                            pills=True,
                            class_name="text-dark",
                            
                            ),
                        ],
                        title="Population",
                        class_name="text-dark",
                    ),
                    dbc.AccordionItem(
                        [
                            dbc.Nav([
                                dbc.NavLink("GDP Overview", href="/gdp", active="exact", className="link-dark "),
                                dbc.NavLink("GDP Trend", href="/gdp/trend", active="exact", className="link-dark"),
                                dbc.NavLink("GDP Growth Comparison", href="/gdp/compare", active="exact", className="link-dark"),
                            ],

                            vertical=True,
                            pills=True,
                            class_name="text-dark",
                            ),
                        ],
                        title="GDP",
                        class_name="text-dark",
                    ),

                ],
                    start_collapsed=True,
                    class_name="text-dark",
                    always_open=True,
                ),
                
            ],
            className="text-dark",
        ), 
        
    ],
    style=SIDEBAR_STYLE,
)



content = html.Div(dash.page_container, id="page-content", style=CONTENT_STYLE, )

app.layout = html.Div([sidebar, content])



if __name__ == '__main__':
    app.run(debug=True)