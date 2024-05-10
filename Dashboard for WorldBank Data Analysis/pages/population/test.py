import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objs as go
from plotly.subplots import make_subplots

dash.register_page(__name__,path="/population/test")


# Sample data for demonstration
years = [2019, 2020, 2021]
data = {
    2019: [100, 200, 300],
    2020: [150, 250, 350],
    2021: [200, 300, 400]
}

# Define Dash app
app = dash.Dash(__name__)

# Define app layout
# Define app layout
layout = html.Div([
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': str(year), 'value': year} for year in years],
        value=years[0]  # Default value
    ),
    dcc.Graph(id='bar-graph')
])

# Define callback to update bar graph
@callback(
    Output('bar-graph', 'figure'),
    [Input('year-dropdown', 'value')]
)
def update_graph(selected_year):
    fig = make_subplots(rows=1, cols=1)

    # Add trace for each category
    for i, category in enumerate(['Category 1', 'Category 2', 'Category 3']):
        fig.add_trace(
            go.Bar(x=[category], y=[data[selected_year][i]], name=category),
            row=1, col=1
        )

    # Update layout
    fig.update_layout(
        title=f'Bar Graph for {selected_year}',
        showlegend=True,
        yaxis=dict(title='Value')
    )

    return fig

