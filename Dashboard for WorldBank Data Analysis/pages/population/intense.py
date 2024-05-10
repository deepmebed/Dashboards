import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import world_bank_data as wb
import pandas as pd
import numpy as np


dash.register_page(__name__, path="/population/intense")

# Load population data from CSV file
df_population = pd.read_csv("pages/population/population_data.csv")

HEADING_STYLE = {
    "background-color": "#f5f5f5",
    "border": "1px solid #ebebeb",
    "padding": "5px",
    "font-size": "24px",
    "text-transform": "uppercase",
    "text-align": "center",
}

# Dash layout
layout = html.Div([
    html.H1('World Population Intensity - Choropleth Map', className="text-5", style=HEADING_STYLE),
    dcc.Graph(id='choropleth-graph'),
    dcc.Slider(
        id='year-slider',
        min=int(df_population.columns[4]),  # the years start from the 5th column
        max=int(df_population.columns[-1]),  # the last column is the latest year
        value=int(df_population.columns[-1]),  # Initial value is the latest year
        marks={str(year): str(year)[2:] for year in df_population.columns[4:]},  # Year marks from columns
        step=None
    )
])

# Dash callback to update choropleth graph
@callback(
    Output('choropleth-graph', 'figure'),
    Input('year-slider', 'value')
)
def update_choropleth(year):
    year_column = str(year)
    filtered_df = df_population[['Country Code', year_column]].copy()
    filtered_df.columns = ['iso_alpha', 'population']  # Renaming columns for consistency with API data
    
    # Log transform population for better color representation
    filtered_df['population_log'] = np.log10(filtered_df['population'])
    
    fig = px.choropleth(filtered_df, locations="iso_alpha",
                        color="population_log",
                        hover_name="iso_alpha",  # Change hover information as needed
                        color_continuous_scale=px.colors.sequential.Plasma,
                        title="World Population",
                        range_color=(0, filtered_df['population_log'].max()))  # Ensure range covers all values
    fig.update_geos(projection_type="natural earth")
    return fig