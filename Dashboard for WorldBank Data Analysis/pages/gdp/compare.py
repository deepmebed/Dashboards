import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd

dash.register_page(__name__, path='/gdp/compare')

gdp_data = pd.read_csv('pages/gdp/gdp_data.csv')

# Function to fetch country names and codes from the dataset
def fetch_country_names():
    countries = [{'label': row['Country Name'], 'value': row['Country Code']} for index, row in gdp_data.iterrows()]
    return countries

HEADING_STYLE = {
    "background-color": "#f5f5f5",
    "border": "1px solid #ebebeb",
    "padding": "5px",
    "font-size": "24px",
    "text-transform": "uppercase",
    "text-align": "center",
}

# Layout of the Dash app for GDP comparison
layout = html.Div([
    html.H1("GDP Growth Comparison", style=HEADING_STYLE),
    html.Div([
        html.Label("Select Countries:"),
        dcc.Dropdown(
            id='countries-dropdown-gdp',
            options=fetch_country_names(),
            value=['PAK', 'BGD', 'IND'],  # Default values
            multi=True
        )
    ]),
    dcc.Graph(id='gdp-comparison-graph', style={'height': '700px'})
])

# Callback to update the graph based on user input for GDP comparison
@callback(
    Output('gdp-comparison-graph', 'figure'),
    [Input('countries-dropdown-gdp', 'value')]
)
def update_gdp_graph(selected_countries):
    # Filter data for selected countries
    filtered_data = gdp_data[gdp_data['Country Code'].isin(selected_countries)]
    
    # Melt the data to long format for easier plotting
    melted_data = filtered_data.melt(id_vars=['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code'], 
                                     var_name='Year', value_name='GDP Growth')
    
    # Convert Year column to numeric
    melted_data['Year'] = pd.to_numeric(melted_data['Year'], errors='coerce')
    
    # Plot the data
    fig = px.bar(melted_data, 
                 x="Country Name", 
                 y="GDP Growth", 
                 animation_frame="Year", 
                 animation_group="Country Name", 
                 hover_name="Country Name",
                 color="Country Name",
                 range_y=[melted_data['GDP Growth'].min()*1.1, melted_data['GDP Growth'].max()*1.1],
                 color_discrete_sequence=px.colors.qualitative.Vivid,
                 labels={'Country Name': 'Country', 'GDP Growth': 'GDP Growth (%)'},
                 title="Global GDP Growth Comparison Over Time"
                )
    
    # Update layout
    fig.update_layout(
        xaxis_title="Country",
        yaxis_title="GDP Growth (%)",
        font=dict(
            family="Arial",
            size=14
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        updatemenus=[{
            'type': 'buttons',
            'showactive': False,
            'buttons': [{
                'label': 'Play',
                'method': 'animate',
                'args': [None, {
                    'frame': {'duration': 500, 'redraw': True},
                    'fromcurrent': True,
                    'mode': 'immediate'
                }]
            }, {
                'label': 'Pause',
                'method': 'animate',
                'args': [[None], {
                    'frame': {'duration': 0, 'redraw': True},
                    'mode': 'immediate'
                }]
            }]
        }]
    )
    
    return fig
