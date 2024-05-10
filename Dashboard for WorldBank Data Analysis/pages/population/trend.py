import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objs as go
import requests

dash.register_page(__name__, path='/population/trend')


def get_country_data():
    url = 'https://api.worldbank.org/v2/country?format=json&per_page=400'
    response = requests.get(url)
    data = response.json()
    countries = [{'label': country['name'], 'value': country['id']} for country in data[1]]
    return countries

def get_population(country_codes):
    population_data = []
    for country_code in country_codes:
        if country_code == 'WLD':
            url = 'http://api.worldbank.org/v2/country/WLD/indicator/SP.POP.TOTL?format=json'
        else:
            url = f'http://api.worldbank.org/v2/country/{country_code}/indicator/SP.POP.TOTL?format=json'
        response = requests.get(url)
        data = response.json()
        country_population_data = [(entry['date'], entry['value']) for entry in data[1]]
        population_data.append({'country': country_code, 'data': country_population_data})
    return population_data

HEADING_STYLE = {
    "background-color": "#f5f5f5",
    "border": "1px solid #ebebeb",
    "padding": "5px",
    "font-size": "24px",
    "text-transform": "uppercase",
    "text-align": "center",
}


layout = html.Div([
        html.H1("Population Trend Over Year", style=HEADING_STYLE),
        html.Hr(),
        
        html.Div([
        dcc.Dropdown(
            id='country-dropdown',
            options=get_country_data(),
            value=['PAK','NGA'],  # Default selection
            multi=True  # Allowing multiple selection
        )
        ]),
        html.Div([
            dcc.Graph(id='indicator-graph')
        ])
    ])

@callback(
    Output('indicator-graph', 'figure'),
    Input('country-dropdown', 'value')
)
def update_graph(selected_countries):
    if not selected_countries:
        selected_countries = ['WLD']  # Default to world population if no country is selected
    figure_data = []
    try:
        for country_code in selected_countries:
            population_data = get_population([country_code])
            country_population = population_data[0]['data']
            years = [entry[0] for entry in country_population]
            populations = [entry[1] for entry in country_population]
            if country_code == 'WLD':
                title = 'World Population'
            else:
                title = f'{country_code} Population'
            figure_data.append(go.Scatter(x=years, y=populations, mode='lines+markers', name=title))

    except:
        return {'layout': go.Layout(title='Data Not Available')}
        
    figure = {
        'data': figure_data,
        'layout': go.Layout(
            title='Population Trends',
            xaxis={'title': 'Year'},
            yaxis={'title': 'Population'},
            hovermode='closest'
        )
    }
    return figure
