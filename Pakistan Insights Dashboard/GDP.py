import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_excel("GDP.xlsx")

def plot_GDP(selected_plot):
    st.title("💰 Gross Domestic Production")
    max_year = df['Year'].max()

    if max_year < 2022:
        missing_years = list(range(max_year + 1, 2023))

        for year in missing_years:
            data = df.append({'Year': year}, ignore_index=True)

    if selected_plot == 'GDP over Time':
        fig = px.line(df, x='Year', y='GDP', title='GDP Over Time')
        st.plotly_chart(fig, use_container_width=True)
    elif selected_plot == 'Contribution to GDP Over Time':
        fig = px.area(df, x='Year', y=['Crops', 'Livestock', 'Forestry', 'Fishing', 'Mining', 'Manufacturing',
                                         'Electricity, Gas,Water', 'Construction', 'Wholesale & Retail',
                                         'Transport, Storage', 'Hotels & Restaurants ', 'Information and Communication',
                                         'Financial and Insurance Activities', 'Real Estate Activities',
                                         'Public Administration & Social Security', 'Education',
                                         'Human Health and Social Work Activities', 'Other Private Services'],
                      title='Contribution to GDP Over Time')
        st.plotly_chart(fig, use_container_width=True)
    elif selected_plot == 'GDP vs Taxes Over Time':
        fig = px.bar(df, x='Year', y=['GDP', 'Taxes'], title='GDP vs Taxes Over Time')
        st.plotly_chart(fig, use_container_width=True)
    elif selected_plot == 'GDP vs Gross National Income':
        fig = px.line(df, x='GDP', y='Gross National Income', title='GDP vs Gross National Income')
        st.plotly_chart(fig, use_container_width=True)
    elif selected_plot == 'Distribution of GDP Across Sectors':
        fig = px.box(df, x='Year', y=['Crops', 'Livestock', 'Forestry', 'Fishing', 'Mining', 'Manufacturing',
                                        'Electricity, Gas,Water', 'Construction', 'Wholesale & Retail',
                                        'Transport, Storage', 'Hotels & Restaurants ', 'Information and Communication',
                                        'Financial and Insurance Activities', 'Real Estate Activities',
                                        'Public Administration & Social Security', 'Education',
                                        'Human Health and Social Work Activities', 'Other Private Services'],
                     title='Distribution of GDP Across Sectors')
        st.plotly_chart(fig, use_container_width=True)
    elif selected_plot == "GDP vs. Taxes vs. Subsidies":
        fig = px.scatter(df, x='GDP', y='Taxes', size='Subsidies', hover_name='Year',
                         title='GDP vs. Taxes vs. Subsidies')
        st.plotly_chart(fig, use_container_width=True)
    elif selected_plot == "GDP at Current Market Prices":
        fig = px.line(df, x='Year', y='GDP(at Current Market Prices)',
                     title='Distribution of GDP at Current Market Prices')
        st.plotly_chart(fig, use_container_width=True)
    elif selected_plot == "Net Primary Income":
        fig = px.line(df, x='Year', y='Net Primary Income', title='Net Primary Income Over Time')
        st.plotly_chart(fig, use_container_width=True)
