import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objs as go
import requests

dash.register_page(__name__, path='/gdp/trend')


def get_country_data():
    url = 'https://api.worldbank.org/v2/country?format=json&per_page=400'
    response = requests.get(url)
    data = response.json()
    countries = [{'label': country['name'], 'value': country['id']} for country in data[1]]
    return countries

def get_gdp(country_codes):
    gdp_data = []
    for country_code in country_codes:
        if country_code == 'WLD':
            url = 'http://api.worldbank.org/v2/country/WLD/indicator/NY.GDP.MKTP.CD?format=json'
        else:
            url = f'http://api.worldbank.org/v2/country/{country_code}/indicator/NY.GDP.MKTP.CD?format=json'
        response = requests.get(url)
        data = response.json()
        country_gdp_data = [(entry['date'], entry['value']) for entry in data[1]]
        gdp_data.append({'country': country_code, 'data': country_gdp_data})
    return gdp_data

HEADING_STYLE = {
    "background-color": "#f5f5f5",
    "border": "1px solid #ebebeb",
    "padding": "5px",
    "font-size": "24px",
    "text-transform": "uppercase",
    "text-align": "center",
}

layout = html.Div([
        html.H1("GDP Trend Over Year", style=HEADING_STYLE),
        html.Hr(),
        
        html.Div([
        dcc.Dropdown(
            id='country-dropdown-gdp',
            options=get_country_data(),
            value=['PAK', 'BGD' ],  # Default selection
            multi=True  # Allowing multiple selection
        )
        ]),
        html.Div([
            dcc.Graph(id='indicator-graph-gdp')
        ])
    ])

@callback(
    Output('indicator-graph-gdp', 'figure'),
    Input('country-dropdown-gdp', 'value')
)
def update_gdp_graph(selected_countries):
    if not selected_countries:
        selected_countries = ['WLD']  # Default to world GDP if no country is selected
    figure_data = []
    try:
        for country_code in selected_countries:
            gdp_data = get_gdp([country_code])
            country_gdp = gdp_data[0]['data']
            years = [entry[0] for entry in country_gdp]
            gdps = [entry[1] for entry in country_gdp]
            if country_code == 'WLD':
                title = 'World GDP'
            else:
                title = f'{country_code} GDP'
            figure_data.append(go.Scatter(x=years, y=gdps, mode='lines+markers', name=title))

    except:
        return {'layout': go.Layout(title='Data Not Available')}
        
    figure = {
        'data': figure_data,
        'layout': go.Layout(
            title='GDP Trends',
            xaxis={'title': 'Year'},
            yaxis={'title': 'GDP'},
            hovermode='closest'
        )
    }
    return figure
