import streamlit as st
import pandas as pd
import plotly.express as px
# Load data
st.set_page_config(page_title="Maheen ", page_icon=":bar_chart:",layout="wide")

st.title(" :taurus: Maheen CAI")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)
@st.cache
def load_data():
    df = pd.read_csv('Adidas.csv')
    # Convert numerical values from strings to numeric type
    df['PriceperUnit'] = df['PriceperUnit'].str.replace('$', '').str.replace(',', '').astype(float)
    df['UnitsSold'] = df['UnitsSold'].str.replace(',', '').astype(int)
    df['TotalSales'] = df['TotalSales'].str.replace('$', '').str.replace(',', '').astype(float)
    df['OperatingProfit'] = df['OperatingProfit'].str.replace('$', '').str.replace(',', '').astype(float)
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

    return df

df = load_data()

st.sidebar.header('Dashboard Settings')

# Selecting columns for analysis
columns = st.sidebar.multiselect('Select columns for analysis', df.columns)

# Displaying the selected columns
st.write('## Data')
st.write(df[columns])

# Scatter plot for Total Sales vs Operating Profit
st.write('## Scatter Plot: Total Sales vs Operating Profit')
scatter_fig = px.scatter(df, x='TotalSales', y='OperatingProfit', color='SalesMethod', hover_data=['Product'])
st.plotly_chart(scatter_fig)

# Bar chart for Total Sales by Region
st.write('## Bar Chart: Total Sales by Region')
bar_fig = px.bar(df, x='Region', y='TotalSales', color='Region', title='Total Sales by Region')
st.plotly_chart(bar_fig)

# Histogram for Price per Unit
st.write('## Histogram: Price per Unit')
hist_fig = px.histogram(df, x='PriceperUnit', nbins=20, title='Distribution of Price per Unit')
st.plotly_chart(hist_fig)

# Piechart for  price in diffrent region
st.write('## Price In Different Region')
hist_fig = px.pie(df, values='PriceperUnit', names='Region', title='Price in Different region')
st.plotly_chart(hist_fig)

 # Create bar chart Total Sales by Sales Method
st.write('## Sales Method Analysis: Total Sales by Sales Method')
sales_fig = px.bar(df, x='SalesMethod', y='TotalSales', title='Total Sales by Sales Method')
st.plotly_chart(sales_fig)

# Calculate Operating Margin (%)
df['OperatingMarginPct'] = (df['OperatingProfit'] / df['TotalSales']) * 100

# Create bar chart
st.write('## Profit Margin Analysis: Operating Margin as Percentage of Total Sales')
margin_fig = px.bar(df, x='Region', y='OperatingMarginPct', title='Operating Margin as Percentage of Total Sales')
st.plotly_chart(margin_fig)

# Create bar chart
st.write('## Product Analysis: Total Sales by Product')
bar_fig = px.bar(df, x='Product', y='TotalSales', title='Total Sales by Product')
st.plotly_chart(bar_fig)


# Create histogram
st.write('## Price Analysis: Distribution of Price per Unit')
hist_fig = px.histogram(df, x='PriceperUnit', nbins=20, title='Distribution of Price per Unit')
st.plotly_chart(hist_fig)


"""# Create choropleth map with a different column for coloring
st.write('## Regional Analysis: Coloring by Another Column')
choropleth_fig = px.choropleth(df, locations='Region', color='OperatingProfit', hover_name='Region', title='Operating Profit by Region')
st.plotly_chart(choropleth_fig) """ 