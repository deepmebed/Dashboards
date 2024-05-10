import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objs as go
import pandas as pd
import world_bank_data as wb

dash.register_page(__name__, path="/gdp")

# Function to generate Sunburst plot data for GDP
def generate_gdp_sunburst_data():
    # Countries and associated regions
    countries = wb.get_countries()

    # Same data set, indexed with the country code
    gdp = wb.get_series('NY.GDP.MKTP.CD', id_or_value='id', simplify_index=True, mrv=1)

    # Aggregate region, country, and GDP
    df = countries[['region', 'name']].rename(columns={'name': 'country'}).loc[countries.region != 'Aggregates']
    df['gdp'] = gdp

    # Calculate total GDP
    total_gdp = df['gdp'].sum()

    # Calculate GDP percentages
    df['gdp_percent'] = df['gdp'] / total_gdp * 100

    # The sunburst plot requires weights (values), labels, and parent (region, or World)
    # We build the corresponding table here
    columns = ['parents', 'labels', 'values', 'text']

    level1 = df.copy()
    level1.columns = columns
    level1['text'] = level1['values'].apply(lambda gdp: '${:,.2f} ({:.2f}%)'.format(gdp, gdp/total_gdp*100))

    level2 = df.groupby('region').gdp.sum().reset_index()[['region', 'region', 'gdp']]
    level2.columns = columns[:-1]
    level2['parents'] = 'World'
    level2['text'] = level2['values'].apply(lambda gdp: '${:,.2f} ({:.2f}%)'.format(gdp, gdp/total_gdp*100))
    level2['values'] = 0

    level3 = pd.DataFrame({'parents': [''], 'labels': ['World'],
                           'values': [0.0], 'text': ['${:,.2f} ({:.2f}%)'.format(total_gdp, 100.0)]})

    all_levels = pd.concat([level1, level2, level3], axis=0).reset_index(drop=True)

    return dict(
        data=[dict(type='sunburst', hoverinfo='text', **all_levels)],
        layout=dict(title='Click on a region to zoom',
                    width=800, height=800)
    )

HEADING_STYLE = {
    "background-color": "#f5f5f5",
    "border": "1px solid #ebebeb",
    "padding": "5px",
    "font-size": "24px",
    "text-transform": "uppercase",
    "text-align": "center",
}

# Dash layout for GDP Sunburst Plot
layout = html.Div([
    html.H1('GDP Overview - Sunburst Plot', style=HEADING_STYLE),
    dcc.Input(id='dummy-input-gdp', type='hidden', value=''),  # Dummy input component
    
    html.Div([
            dcc.Graph(id='gdp-sunburst-graph'),
        ],
        style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'height': '100vh'},),
    
])

# Dash callback to update GDP Sunburst plot
@callback(
    Output('gdp-sunburst-graph', 'figure'),
    Input('dummy-input-gdp', 'value')  # Dummy input to trigger the update
)
def update_gdp_sunburst(dummy_input):
    return generate_gdp_sunburst_data()
