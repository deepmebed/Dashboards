import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import folium
import dash_bootstrap_components as dbc

from app_config import app  # Assuming 'app_config' contains your Dash app instance

# Load your Dataset (replace with your CSV filename)
df = pd.read_csv('cleaned_housing_data.csv')

# Lists of the locations in each city
cities = df['city'].unique()
location_dict = {city: df['location'][df['city'] == city].unique() for city in cities}

## Heading Style of Graphs

graph_heading  = { 
  'font-family': 'Arial, sans-serif', 
  'font-size': '24px',
  'font-weight': 'bold', 
  'color': '#242424',
  'text-align': 'center',
  'margin-bottom': '15px'
}

# Dropdown style

select_dropdown = {
    'width': '100%',
    'padding': '10px',
    'font-size': '16px',
    'border-radius': '5px',
    'border': '1px solid #ccc'
}



graph_container = {
    'border': '1px solid #ccc',
    'border-radius': '5px',
    'margin-top': '20px',
    'padding': '20px'
}
map_container = {
    'border': '1px solid #ccc',
    'border-radius': '5px',
    'margin-top': '20px',
    'padding': '20px',
    'height': '500px'  # Adjust height as needed
}

body_dict = {
    "font-family": "Arial, sans-serif",
    "background-color": "#f5f5f5",
    "color": "#333"
}

h = {
    "color": "#333"
}

container = {
    "max-width": "1200px",
    "margin": "0 auto",
    "padding": "20px"
}

graph_heading = {
    "font-size": "24px",
    "font-weight": "bold",
    "color": "#242424",
    "text-align": "center",
    "margin-bottom": "15px"
}

row = {
    "margin-bottom": "20px"
}

form_control = {
    "width": "100%",
    "padding": "10px",
    "border-radius": "5px",
    "border": "1px solid #ccc",
    "background-color": "#fff",
    "color": "#333"
}

form_control_focus = {
    "border-color": "#007bff",
    "outline": "none",
    "box-shadow": "0 0 0 0.2rem rgba(0,123,255,.25)"
}



layout = html.Div([
        # html.H1("Real Estate Dashboard", className="text-center my-4"),
    html.H2("Average Property Prices by Type" , style=graph_heading),  
    html.Div([
        html.Div([
            html.Label("Select City for Bar Graph:", className="font-weight-bold"),
            dcc.Dropdown(
                id='city-dropdown-bar',
                options=[{'label': city, 'value': city} for city in cities],
                value=cities[0],  # Set default value
                className="form-control select_dropdown"
            ),
        ], className="col-md-3"),

        html.Div([
            html.Label("Select Location:", className="font-weight-bold"),
            dcc.Dropdown(
                id='location-dropdown',
                placeholder="Select a location",
                multi=True,
                className="form-control select_dropdown"
            ),
        ], className="col-md-3"),

        html.Div([
            html.Label("Select Area Category:", className="font-weight-bold"),
            dcc.Dropdown(
                id='area-category-dropdown',
                options=[{'label': cat, 'value': cat} for cat in df['Area Category'].unique()],
                placeholder="Select an area category",
                className="form-control select_dropdown"
            )
        ], className="col-md-3"),

        html.Div([
            html.Label("Select Bedrooms:", className="font-weight-bold"),
            dcc.Dropdown(
                id='bedrooms-dropdown',
                options=[{'label': beds, 'value': beds} for beds in df['bedrooms'].unique()],
                placeholder="Select number of bedrooms",
                className="form-control select_dropdown"
            )
        ], className="col-md-2"),
    ], className="row mt-4 "),
    dcc.Graph(id='average-price-graph', className="mt-4 graph_container"),
    html.H2("Top Expensive and Cheap Locations" , style=graph_heading),  
    html.Div([
        html.Div([
            html.Label("Select City:", className="font-weight-bold"),
            dcc.Dropdown(
                id='city-dropdown',
                options=[{'label': city, 'value': city} for city in cities],
                value=cities[0],  # Set default value
                className="form-control select_dropdown"
            ),
        ], className="col-md-4"),

        html.Div([
            html.Label("Select Number of Bars:", className="font-weight-bold"),
            dcc.Dropdown(
                id='num-bars-dropdown',
                options=[{'label': i, 'value': i} for i in range(5, 21)],  # Choose up to top 10
                value=5,  # Default to 5
                className="form-control select_dropdown"
            ),
        ], className="col-md-4"),
    ], className="row mt-4"),

    html.Div([
        dcc.Graph(id='expensive-graph', className="col-md-6 mt-4 graph_container"),
        dcc.Graph(id='cheap-graph', className="col-md-6 mt-4 graph_container")
    ], className="row"),
    html.H2("Visualizing Expensive and Affordable Areas" , style=graph_heading),  
    html.Div([
        html.Div([
            html.Label("Select City for Map:", className="font-weight-bold"),
            dcc.Dropdown(
                id='city-dropdown-map',
                options=[{'label': city, 'value': city} for city in cities],
                value=cities[0],  # Set default value
                className="form-control select_dropdown"
            ),
        ], className="col-md-4"),

        html.Div([
            html.Label("Select Number of Top Expensive Areas:", className="font-weight-bold"),
            dcc.Dropdown(
                id='top-expensive-dropdown',
                options=[{'label': i, 'value': i} for i in range(5, 21)],  # Choose up to top 10
                value=5,  # Default to 5
                className="form-control select_dropdown"
            ),
        ], className="col-md-4"),

        html.Div([
            html.Label("Select Number of Top Cheap Areas:", className="font-weight-bold"),
            dcc.Dropdown(
                id='top-cheap-dropdown',
                options=[{'label': i, 'value': i} for i in range(5, 21)],  # Choose up to top 10
                value=5,  # Default to 5
                className="form-control select_dropdown"
            ),
        ], className="col-md-4"),
    ], className="row mt-4"),

    html.Div(id='map-container', className="mt-4 p-2 border map_container "),  # Added map-container component here

html.H2("Locations of the properties available for Sale", style=graph_heading),  
# Detailed map layout
html.Div([
    dbc.Row([  # or html.Div with className="row"
        dbc.Col([  # or html.Div with className="col-md-4"
            html.Label("Select City:", className="font-weight-bold"),
            dcc.Dropdown(
                id='city-dropdown-detailed-map',
                options=[{'label': city, 'value': city} for city in cities],
                value=cities[0],  # Set default value
                className="form-control select_dropdown"
            ),
        ], width=4),

        dbc.Col([  # or html.Div with className="col-md-4"
            html.Label("Select Location:", className="font-weight-bold"),
            dcc.Dropdown(
                id='location-dropdown-detailed-map',
                placeholder="Select a location",
                className="form-control select_dropdown"
            ),
        ], width=4),
    ]),
    
    html.Div(id='detailed-map-container', className="mt-4 p-2 border map_container")  # Detailed map container
]),


    html.H2("Property Type Breakdown by Location" , style=graph_heading),
    # Property type pie chart layout
    html.Div([
        html.Div([
            html.Label("Select City for Property Type Pie Chart:", className="font-weight-bold"),
            dcc.Dropdown(
                id='city-dropdown-pie-chart',
                options=[{'label': city, 'value': city} for city in cities],
                value=cities[0],  # Set default value
                className="form-control select_dropdown"
            ),
        ], className="col-md-4"),

        html.Div([
            html.Label("Select Location:", className="font-weight-bold"),
            dcc.Dropdown(
                id='location-dropdown-pie-chart',
                placeholder="Select a location",
                className="form-control select_dropdown"
            ),
        ], className="col-md-4"),

        html.Div([
            html.Label("Select Chart Type:", className="font-weight-bold"),
            dcc.Dropdown(
                id='chart-type-dropdown',
                options=[
                    {'label': 'Bar Chart', 'value': 'bar'},
                    {'label': 'Pie Chart', 'value': 'pie'}
                ],
                value='bar',  # Default to pie chart
                className="form-control select_dropdown"
            ),
        ], className="col-md-4"),
    ], className="row mt-4"),

    dcc.Graph(id='property-type-graph', className="mt-4 graph_container"),

    html.H2("Area Category Breakdown by Location" , style=graph_heading),
   # Area category chart layout
    html.Div([
        html.Div([
            html.Label("Select City for Area Category Chart:", className="font-weight-bold"),
            dcc.Dropdown(
                id='city-dropdown-area-category',
                options=[{'label': city, 'value': city} for city in cities],
                value=cities[0],  # Set default value
                className="form-control select_dropdown"
            ),
        ], className="col-md-4"),

        html.Div([
            html.Label("Select Location:", className="font-weight-bold"),
            dcc.Dropdown(
                id='location-dropdown-area-category',
                placeholder="Select a location",
                className="form-control select_dropdown"
            ),
        ], className="col-md-4"),

        html.Div([
            html.Label("Select Chart Type:", className="font-weight-bold"),
            dcc.Dropdown(
                id='chart-type-dropdown-area-category',
                options=[
                    {'label': 'Bar Chart', 'value': 'bar'},
                    {'label': 'Pie Chart', 'value': 'pie'}
                ],
                value='bar',  # Default to pie chart
                className="form-control select_dropdown"
            ),
        ], className="col-md-4"),
    ], className="row mt-4"),

    dcc.Graph(id='area-category-graph', className="mt-4 graph_container"),

    html.H2("Bedrooms vs. Price" , style=graph_heading),
    # Layout for the bedrooms vs. price graph
    html.Div([
        html.Div([
            html.Label("Select City for Bedrooms vs. Price Graph:", className="font-weight-bold"),
            dcc.Dropdown(
            id='city-dropdown-bedrooms',
            options=[{'label': city, 'value': city} for city in cities],
            value=cities[0],  # Set default value
            className="form-control select_dropdown"
        ),
    ], className="col-md-4"),

        html.Div([
            html.Label("Select Location:", className="font-weight-bold"),
            dcc.Dropdown(
            id='location-dropdown-bedrooms',
            placeholder="Select a location",
            className="form-control select_dropdown"
        ),
    ], className="col-md-4"),

        html.Div([
            html.Label("Select Property Type:", className="font-weight-bold"),
        dcc.Dropdown(
            id='property-type-dropdown-bedrooms',
            options=[{'label': prop_type, 'value': prop_type} for prop_type in df['property_type'].unique()],
            placeholder="Select a property type",
            className="form-control select_dropdown"
        ),
    ], className="col-md-4"),
], className="row mt-4"),

    dcc.Graph(id='bedrooms-price-graph', className="mt-4 graph_container"),
])

# Define callback to update location dropdown options based on selected city for bar graph
@app.callback(
    Output('location-dropdown', 'options'),
    Input('city-dropdown-bar', 'value')
)
def update_location_options(selected_city):
    locations = location_dict.get(selected_city, [])
    return [{'label': loc, 'value': loc} for loc in locations]

# Define callback to update average price graph based on selected city and location
@app.callback(
    Output('average-price-graph', 'figure'),
    [Input('city-dropdown-bar', 'value'),
     Input('location-dropdown', 'value'),
     Input('area-category-dropdown', 'value'),
     Input('bedrooms-dropdown', 'value')]
)
def update_average_price_graph(city, locations, area_category, bedrooms):
    filtered_df = df[df['city'] == city]

    if locations:
        filtered_df = filtered_df[filtered_df['location'].isin(locations)]
    if area_category:
        filtered_df = filtered_df[filtered_df['Area Category'] == area_category]
    if bedrooms:
        filtered_df = filtered_df[filtered_df['bedrooms'] == bedrooms]

    # Group by property_type and calculate average price
    avg_prices = filtered_df.groupby('property_type')['price'].mean().reset_index()

    # Create a bar chart using Plotly Express
    fig = px.bar(avg_prices, x='property_type', y='price', title='Average Price of Properties by Type')

    return fig

# Define callback to update location price graphs based on selected city and options
@app.callback(
    [Output('expensive-graph', 'figure'),
     Output('cheap-graph', 'figure')],
    [Input('city-dropdown', 'value'),
     Input('num-bars-dropdown', 'value')]
)
def update_location_price_graphs(city, num_bars):
    # Filter the dataset based on the selected city for expensive areas
    city_df_expensive = df[df['city'] == city]

    # Filter the dataset based on the selected city for cheap areas
    city_df_cheap = df[df['city'] == city]

    # Calculate average price for each location for expensive areas
    avg_prices_expensive = city_df_expensive.groupby('location')['price'].mean().reset_index()

    # Calculate average price for each location for cheap areas
    avg_prices_cheap = city_df_cheap.groupby('location')['price'].mean().reset_index()

    # Sort locations by price to identify top expensive and cheap locations
    top_expensive = avg_prices_expensive.nlargest(num_bars, 'price')
    top_cheap = avg_prices_cheap.nsmallest(num_bars, 'price')

    # Create bar charts for expensive and cheap locations using Plotly Express
    fig_expensive = px.bar(top_expensive, x='location', y='price', title=f'Top {num_bars} Expensive Areas in {city}')
    fig_cheap = px.bar(top_cheap, x='location', y='price', title=f'Top {num_bars} Cheap Areas in {city}')

    return fig_expensive, fig_cheap

# Define callback to update map based on selected city for map
@app.callback(
    Output('map-container', 'children'),
    Input('city-dropdown-map', 'value'),
    Input('top-expensive-dropdown', 'value'),
    Input('top-cheap-dropdown', 'value')
)
def update_map(selected_city, top_expensive, top_cheap):
    # Filter the dataset based on the selected city
    city_df = df[df['city'] == selected_city]

    # Calculate average price for each location
    avg_prices = city_df.groupby('location')['price'].mean().reset_index()

    # Sort locations by price to identify top expensive and cheap locations
    top_expensive = avg_prices.nlargest(top_expensive, 'price')
    top_cheap = avg_prices.nsmallest(top_cheap, 'price')

    # Get the top expensive and cheap locations
    top_expensive_locations = top_expensive['location'].tolist()
    top_cheap_locations = top_cheap['location'].tolist()

    # Filter the dataset for the specified city and top expensive locations
    expensive_df = df[(df['city'] == selected_city) & (df['location'].isin(top_expensive_locations))]

    # Filter the dataset for the specified city and top cheap locations
    cheap_df = df[(df['city'] == selected_city) & (df['location'].isin(top_cheap_locations))]

    # Create a Folium map
    m = folium.Map(location=[city_df['latitude'].mean(), city_df['longitude'].mean()], zoom_start=12)

    # Add markers for top expensive and cheap locations
    for idx, row in expensive_df.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=row['location'] + f" (Expensive: pkr {row['price']:,.2f})",
            icon=folium.Icon(color='red')  # Red markers for expensive locations
        ).add_to(m)

    for idx, row in cheap_df.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=row['location'] + f" (Cheap: pkr {row['price']:,.2f})",
            icon=folium.Icon(color='green')  # Green markers for cheap locations
        ).add_to(m)

    # Convert Folium map to HTML
    html_map = m._repr_html_()

    return html.Iframe(srcDoc=html_map, style={'width': '100%', 'height': '500px'})


# Define callback to update location dropdown options based on selected city for detailed map
@app.callback(
    [Output('location-dropdown-detailed-map', 'options'),
     Output('location-dropdown-detailed-map', 'value')],
    Input('city-dropdown-detailed-map', 'value')
)
def update_location_options_detailed_map(selected_city):
    locations = location_dict.get(selected_city, [])
    location_options = [{'label': loc, 'value': loc} for loc in locations]
    default_location = locations[0] if len(locations) > 0 else None  # Set default to first location or None
    return location_options, default_location

# Define callback to update detailed map based on selected city and location
@app.callback(
    Output('detailed-map-container', 'children'),
    [Input('city-dropdown-detailed-map', 'value'),
     Input('location-dropdown-detailed-map', 'value')]
)
def update_detailed_map(selected_city, selected_location):
    # Filter the dataset based on the selected city and location
    if selected_location is None:
        filtered_df = df[df['city'] == selected_city]
    else:
        filtered_df = df[(df['city'] == selected_city) & (df['location'] == selected_location)]

    # Create a Folium map
    m = folium.Map(location=[filtered_df['latitude'].mean(), filtered_df['longitude'].mean()], zoom_start=14)

    # Add markers for each house
    for idx, row in filtered_df.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"Price: pkr {row['price']:,.2f}",
            icon=folium.Icon(color='blue')
        ).add_to(m)

    # Convert Folium map to HTML
    html_map = m._repr_html_()

    return html.Iframe(srcDoc=html_map, style={'width': '100%', 'height': '500px'})

# Define callback to update location dropdown options based on selected city for pie chart
@app.callback(
    Output('location-dropdown-pie-chart', 'options'),
    Input('city-dropdown-pie-chart', 'value')
)
def update_location_options_pie_chart(selected_city):
    locations = location_dict.get(selected_city, [])
    return [{'label': loc, 'value': loc} for loc in locations]

# Define callback to update the property type graph based on selected city, location, and chart type
@app.callback(
    Output('property-type-graph', 'figure'),
    [Input('city-dropdown-pie-chart', 'value'),
     Input('location-dropdown-pie-chart', 'value'),
     Input('chart-type-dropdown', 'value')]
)
def update_property_type_graph(city, selected_location, chart_type):
    filtered_df = df[df['city'] == city]

    if selected_location:
        filtered_df = filtered_df[filtered_df['location'] == selected_location]

    if chart_type == 'pie':
        # Count the number of properties for each type
        property_type_counts = filtered_df['property_type'].value_counts().reset_index()
        property_type_counts.columns = ['Property Type', 'Count']

        # Create a pie chart for property types using Plotly Express
        fig = px.pie(property_type_counts, values='Count', names='Property Type', title=f'Property Types in {city}')
    else:  # Bar chart
        # Count the number of properties for each type
        property_type_counts = filtered_df['property_type'].value_counts().reset_index()
        property_type_counts.columns = ['Property Type', 'Count']

        # Create a bar chart for property types using Plotly Express
        fig = px.bar(property_type_counts, x='Property Type', y='Count', title=f'Property Types in {city}')

    return fig



# Define callback to update location dropdown options based on selected city for area category chart
@app.callback(
    Output('location-dropdown-area-category', 'options'),
    Input('city-dropdown-area-category', 'value')
)
def update_location_options_area_category(selected_city):
    locations = location_dict.get(selected_city, [])
    return [{'label': loc, 'value': loc} for loc in locations]

# Define callback to update the area category graph based on selected city, location, and chart type
@app.callback(
    Output('area-category-graph', 'figure'),
    [Input('city-dropdown-area-category', 'value'),
     Input('location-dropdown-area-category', 'value'),
     Input('chart-type-dropdown-area-category', 'value')]
)
def update_area_category_graph(city, selected_location, chart_type):
    filtered_df = df[df['city'] == city]

    if selected_location:
        filtered_df = filtered_df[filtered_df['location'] == selected_location]

    if chart_type == 'pie':
        # Count the number of properties for each area category
        area_category_counts = filtered_df['Area Category'].value_counts().reset_index()
        area_category_counts.columns = ['Area Category', 'Count']

        # Create a pie chart for area categories using Plotly Express
        fig = px.pie(area_category_counts, values='Count', names='Area Category', title=f'Area Categories in {city}')
    else:  # Bar chart
        # Count the number of properties for each area category
        area_category_counts = filtered_df['Area Category'].value_counts().reset_index()
        area_category_counts.columns = ['Area Category', 'Count']

        # Create a bar chart for area categories using Plotly Express
        fig = px.bar(area_category_counts, x='Area Category', y='Count', title=f'Area Categories in {city}')

    return fig
# Callbacks for the bedrooms vs. price graph with property type filter
@app.callback(
    Output('location-dropdown-bedrooms', 'options'),
    Input('city-dropdown-bedrooms', 'value')
)
def update_location_options_bedrooms(selected_city):
    locations = location_dict.get(selected_city, [])
    return [{'label': loc, 'value': loc} for loc in locations]

@app.callback(
    Output('bedrooms-price-graph', 'figure'),
    [Input('city-dropdown-bedrooms', 'value'),
     Input('location-dropdown-bedrooms', 'value'),
     Input('property-type-dropdown-bedrooms', 'value')]
)
def update_bedrooms_price_graph(city, selected_location, selected_property_type):
    # Filter the DataFrame to remove rows where bedrooms == 0
    filtered_df = df[(df['city'] == city) & (df['bedrooms'] > 0)]

    if selected_location:
        filtered_df = filtered_df[filtered_df['location'] == selected_location]
    if selected_property_type:
        filtered_df = filtered_df[filtered_df['property_type'] == selected_property_type]

    # Group by bedrooms and calculate the average price
    avg_price_by_bedrooms = filtered_df.groupby('bedrooms')['price'].mean().reset_index()

    # Create a line graph for bedrooms vs. average price
    fig = px.line(avg_price_by_bedrooms, x='bedrooms', y='price', title=f'Bedrooms vs. Average Price in {city}')

    return fig



# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
