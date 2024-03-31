from dash import html
from dash import dcc
from app_config import app

# Define styles
page_style = {
    'textAlign': 'center',
    'margin': 'auto',
    'width': '80%',
    'padding': '20px',
    'fontFamily': 'Arial, sans-serif',
    'backgroundColor': '#F5F5F5'
}

header_style = {
    'fontSize': '36px',
    'fontWeight': 'bold',
    'marginBottom': '20px',
    'color': '#007BFF'
}

section_header_style = {
    'fontSize': '24px',
    'fontWeight': 'bold',
    'marginTop': '30px',
    'marginBottom': '10px',
    'color': '#007BFF'
}

paragraph_style = {
    'fontSize': '18px',
    'marginBottom': '15px',
    'color': '#333333'
}

link_style = {
    'color': 'white',
    'textDecoration': 'underline',
}

footer_style = {
    'position': 'fixed',
    'bottom': '0',
    'width': '100vw',
    'backgroundColor': '#007BFF',
    'color': 'white',
    'padding': '10px 0',
    'fontSize': '14px',
    'textAlign': 'center'
}

# Define layout
layout = html.Div([
    html.Div(style=page_style, children=[
        html.H1(style=header_style, children="Welcome to the House Pricing Project Dashboard."),
        html.H2(style=section_header_style, children="Dashboard Overview"),
        html.P(style=paragraph_style, children="This dashboard provides insights into real estate trends and helps you make informed decisions. It includes a dashboard to explore the dataset and a page to make predictions. Use the navigation bar to explore the dashboard."),
        html.H2(style=section_header_style, children="About the Dataset"),
        html.P(style=paragraph_style, children="The dataset used in this dashboard contains information about house prices, location, and other features. The dataset contains data of five cities: Islamabad, Lahore, Faisalabad, Rawalpindi, and Karachi."),
        html.P(style=paragraph_style, children=["Data Source: ", html.A('Zameen.com', href='https://www.zameen.com/', target="_blank", style=link_style)]),
        html.P(style=paragraph_style, children=["Dataset Source: ", html.A('Kaggle', href='https://www.kaggle.com/datasets/jillanisofttech/pakistan-house-price-dataset', target="_blank", style=link_style)]),
    ]),
html.Footer(style=footer_style, children=[
    html.Div("© 2024 House Pricing Project Dashboard. All rights reserved."),
    html.Div([
        "Designed by ",
        html.A('Shahzaib Hassan', href='', target="_blank", style=link_style)  # Replace 'https://yourwebsite.com' with the actual URL of your website
    ], style={'marginTop': '5px'}),
])
])