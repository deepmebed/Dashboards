import pandas as pd
import plotly.express as px
import streamlit as st

df = pd.read_csv('Superstore.csv', encoding='latin-1')

df['Order Date'] = pd.to_datetime(df['Order Date'])

st.set_page_config(page_title="Superstore Dashboard")
st.title("Superstore Data Dashboard")

st.sidebar.title("Filters")

date_range = st.sidebar.date_input("Select Date Range", [df['Order Date'].min().date(), df['Order Date'].max().date()])
filtered_df = df[(df['Order Date'] >= pd.Timestamp(date_range[0])) & (df['Order Date'] <= pd.Timestamp(date_range[1]))]

selected_category = st.sidebar.selectbox("Select Product Category", df['Category'].unique())
filtered_df = filtered_df[filtered_df['Category'] == selected_category]

st.sidebar.subheader("Overall Overview")
total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
st.sidebar.metric("Total Sales", total_sales)
st.sidebar.metric("Total Profit", total_profit)

st.subheader("Sales Trend")
sales_by_date = filtered_df.groupby('Order Date')['Sales'].sum().reset_index()
fig_sales_trend = px.line(sales_by_date, x='Order Date', y='Sales')
st.plotly_chart(fig_sales_trend)

st.subheader("Product Analysis")
product_sales = filtered_df.groupby('Product Name')['Sales'].sum().reset_index()
product_sales = product_sales.sort_values('Sales', ascending=False)
fig_top_products = px.bar(product_sales.head(10), x='Product Name', y='Sales')
st.plotly_chart(fig_top_products)

st.subheader("Customer Analysis")
customer_sales = filtered_df.groupby('Customer Name')['Sales'].sum().reset_index()
customer_sales = customer_sales.sort_values('Sales', ascending=False)
fig_top_customers = px.bar(customer_sales.head(10), x='Customer Name', y='Sales')
st.plotly_chart(fig_top_customers)

st.subheader("Geographical Analysis")
fig_map = px.choropleth(filtered_df, locations='State', color='Profit', locationmode="USA-states",
                       scope="usa", labels={'State':'State'})
st.plotly_chart(fig_map)

st.subheader("Sales Distribution")
fig_sales_dist = px.histogram(filtered_df, x="Sales", nbins=30)
st.plotly_chart(fig_sales_dist)

st.subheader("Sales vs Profit")
fig_scatter = px.scatter(filtered_df, x="Sales", y="Profit", trendline="ols")
st.plotly_chart(fig_scatter)

st.subheader("Sales by Region")
sales_by_region = filtered_df.groupby('Region')['Sales'].sum().reset_index()
fig_sales_region = px.bar(sales_by_region, x='Region', y='Sales')
st.plotly_chart(fig_sales_region)
