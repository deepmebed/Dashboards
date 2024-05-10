import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
# #2C313D
# Set page configuration
def set_page_config():
    page_bg_color = "#FFF44F"  # Lemon yellow background color
    sidebar_color = "#F9E6A7"  # Light yellowish color for sidebar

    page_width = 1200
    st.set_page_config(
        page_title="🌍 South Asian Country Explorer (2000-2023)",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded",
    )


# Read the data
def read_data():
    df_pak = pd.read_csv("\pak.csv")
    df_ind = pd.read_csv("ind.csv")
    df_chi = pd.read_csv("chi.csv")
    df_afg = pd.read_csv("afg.csv")
    df_ira = pd.read_csv("ira.csv")

    for df in [df_pak, df_ira, df_ind, df_afg, df_chi]:
        df.replace('..', np.nan, inplace=True)

    return df_pak, df_ind, df_chi, df_afg, df_ira

# Replace NaN values with appropriate statistics
def replace_null_values(df):
    for column in df.columns:
        if df[column].dtype == 'object':
            mode_val = df[column].mode()[0]
            df[column].fillna(mode_val, inplace=True)
        else:
            mean_val = df[column].astype(float).mean()
            df[column].fillna(mean_val, inplace=True)
    return df

# Simplify columns for all dataframes
def simplify_columns(df):
    df.columns = df.columns.str.split(' \[|\]', expand=True).get_level_values(0)
    return df

# Set the index to the 'Time' column
def set_index_to_time(df):
    df.set_index('Time', inplace=True)
    return df

# Select data dashboard
def select_data_dashboard():
    set_page_config()
    st.title('🌍 South Asian Country Explorer')
    
    df_pak, df_ind, df_chi, df_afg, df_ira = read_data()
    df_pak, df_ind, df_chi, df_afg, df_ira = map(replace_null_values, [df_pak, df_ind, df_chi, df_afg, df_ira])
    df_pak, df_ind, df_chi, df_afg, df_ira = map(simplify_columns, [df_pak, df_ind, df_chi, df_afg, df_ira])
    df_pak, df_ind, df_chi, df_afg, df_ira = map(set_index_to_time, [df_pak, df_ind, df_chi, df_afg, df_ira])

    countries = ['Afghanistan', 'Iran', 'India', 'Pakistan', 'China']

    categories = {
        'Population': ['Population, total', 'Rural population', 'Urban population'],
        'Economy': ['GDP growth (annual %)', 'Inflation, GDP deflator (annual %)',
                    'Agriculture, forestry, and fishing, value added (% of GDP)',
                    'Industry (including construction), value added (% of GDP)',
                    'Exports of goods and services (% of GDP)', 'Imports of goods and services (% of GDP)'],
        'Expenditure': ['Government expenditure on education, total (% of GDP)',
                          'Current health expenditure (% of GDP)', 'Military expenditure (% of GDP)'],
        'Land': ['Agricultural irrigated land (% of total agricultural land)', 'Agricultural land (% of land area)']
    }

    selected_country = st.sidebar.selectbox('Select Country', countries)
    selected_category = st.selectbox('Select Category', list(categories.keys()))

    if selected_category in categories.keys():
        st.subheader(selected_category + ' Dynamics')
        selected_columns = st.multiselect('Select Indicators', categories[selected_category])
        year_range = st.slider('Select Years', min_value=2000, max_value=2023, value=(2000, 2023))

        selected_plot_type = st.selectbox('Select Plot Type', ['Line Plot', 'Bar Plot'])
        if selected_country == 'Afghanistan':
            display_country_data(df_afg, selected_country, year_range, selected_columns, selected_plot_type, categories)
        elif selected_country == 'India':
            display_country_data(df_ind, selected_country, year_range, selected_columns, selected_plot_type, categories)
        elif selected_country == 'Iran':
            display_country_data(df_ira, selected_country, year_range, selected_columns, selected_plot_type, categories)
        elif selected_country == 'Pakistan':
            display_country_data(df_pak, selected_country, year_range, selected_columns, selected_plot_type, categories)
        elif selected_country == 'China':
            display_country_data(df_chi, selected_country, year_range, selected_columns, selected_plot_type, categories)

        if selected_category == 'Population' or selected_category == 'Economy':
            additional_columns = st.checkbox('Plot Additional Dynamics')
            if additional_columns:
                if selected_country == 'Afghanistan':
                    additional_indicators(df_afg, selected_country, year_range, selected_plot_type, selected_category, categories)
                elif selected_country == 'India':
                    additional_indicators(df_ind, selected_country, year_range, selected_plot_type, selected_category,categories)
                elif selected_country == 'Iran':
                    additional_indicators(df_ira, selected_country, year_range, selected_plot_type, selected_category,categories)
                elif selected_country == 'China':
                    additional_indicators(df_chi, selected_country, year_range, selected_plot_type,selected_category, categories)
                elif selected_country == 'Pakistan':
                    additional_indicators(df_pak, selected_country, year_range, selected_plot_type,selected_category, categories)

        compare_with_other_countries(selected_category, selected_columns, year_range, selected_plot_type, selected_country, countries, df_afg, df_ira, df_ind, df_pak, df_chi)

    st.stop()

# Display data for selected country
def display_country_data(df, country_name, year_range, selected_categories, selected_plot_type, categories):
    start_year, end_year = year_range
    filtered_df = df.loc[start_year:end_year, selected_categories]

    filtered_df.dropna(inplace=True)
    filtered_df = filtered_df.apply(pd.to_numeric, errors='ignore')

    if selected_plot_type == 'Line Plot':
        fig = px.line(filtered_df, x=filtered_df.index, y=selected_categories,
                      title=f"{', '.join(selected_categories)} over Time")
        for trace in fig.data:
            trace.line.color = random.choice(px.colors.qualitative.Plotly)
        st.plotly_chart(fig)

    elif selected_plot_type == 'Bar Plot':
        fig = go.Figure()
        for col in selected_categories:
            fig.add_trace(go.Bar(x=filtered_df.index, y=filtered_df[col], name=col, width=0.4, opacity=0.8))
        st.plotly_chart(fig)

# Display additional indicators
def additional_indicators(df, selected_country, year_range, selected_plot_type, selected_category ,categories):
    
    if selected_country == 'Afghanistan':
        if selected_category == 'Economy':
            display_country_data(df, selected_country, year_range, ['GDP (current US$)', 'Personal remittances, received (current US$)'], selected_plot_type, categories)
        elif selected_category == 'Population':
            display_country_data(df, selected_country, year_range, ['Population density (people per sq. km of land area)',
                                     'Life expectancy at birth, total (years)', 'Fertility rate, total (births per woman)']
, selected_plot_type, categories)
       
       
    elif selected_country == 'Iran':
         if selected_category == 'Economy':
            display_country_data(df, selected_country, year_range, ['GDP (current US$)', 'Personal remittances, received (current US$)'], selected_plot_type, categories)
         elif selected_category == 'Population':
            display_country_data(df, selected_country, year_range, ['Population density (people per sq. km of land area)',
                                     'Life expectancy at birth, total (years)', 'Fertility rate, total (births per woman)']
, selected_plot_type, categories)
       
    elif selected_country == 'India':
          if selected_category == 'Economy':
            display_country_data(df, selected_country, year_range, ['GDP (current US$)', 'Personal remittances, received (current US$)'], selected_plot_type, categories)
          elif selected_category == 'Population':
            display_country_data(df, selected_country, year_range, ['Population density (people per sq. km of land area)',
                                     'Life expectancy at birth, total (years)', 'Fertility rate, total (births per woman)']
, selected_plot_type, categories)
       
    elif selected_country == 'Pakistan':
          if selected_category == 'Economy':
            display_country_data(df, selected_country, year_range, ['GDP (current US$)', 'Personal remittances, received (current US$)'], selected_plot_type, categories)
          elif selected_category == 'Population':
            display_country_data(df, selected_country, year_range, ['Population density (people per sq. km of land area)',
                                     'Life expectancy at birth, total (years)', 'Fertility rate, total (births per woman)']
, selected_plot_type, categories)
       
    elif selected_country == 'China':
          if selected_category == 'Economy':
            display_country_data(df, selected_country, year_range, ['GDP (current US$)', 'Personal remittances, received (current US$)'], selected_plot_type, categories)
          elif selected_category == 'Population':
            display_country_data(df, selected_country, year_range, ['Population density (people per sq. km of land area)',
                                     'Life expectancy at birth, total (years)', 'Fertility rate, total (births per woman)']
, selected_plot_type, categories)
       

# Compare selected categories with other countries
def compare_with_other_countries(selected_category, selected_columns, year_range, selected_plot_type, selected_country, countries, df_afg, df_ira, df_ind, df_pak, df_chi):
    comparison_type = st.radio("Compare with other countries ", ("Select Countries",))

    if comparison_type == "Select Countries":
        selected_countries = st.multiselect('Select Countries to Compare', [country for country in countries if country != selected_country])
        selected_countries.append(selected_country)

        combined_df = pd.DataFrame()
        for country in selected_countries:
            selected_df = None
            if country == 'Afghanistan':
                selected_df = df_afg
            elif country == 'Iran':
                selected_df = df_ira
            elif country == 'India':
                selected_df = df_ind
            elif country == 'Pakistan':
                selected_df = df_pak
            elif country == 'China':
                selected_df = df_chi

            if selected_df is not None:
                selected_country_data = selected_df.loc[year_range[0]:year_range[1], selected_columns]
                selected_country_data.columns = [f"{country}: {column}" for column in selected_country_data.columns]

                selected_country_data = selected_country_data.reset_index().melt(id_vars=['Time'], var_name='Category', value_name='Value')
                selected_country_data['Country'] = country
                combined_df = pd.concat([combined_df, selected_country_data], axis=0)

        if not combined_df.empty:
            st.subheader("Comparison between Countries")
            
            fig = px.line(combined_df, x='Time', y='Value', color='Category', facet_col='Country',
                              title=f"Comparison of {', '.join(selected_columns)} over Time for Selected Countries")
            
            fig.update_layout(height=600, width=1000)

            fig.update_layout(legend_title_text='Country')
                
            fig.update_layout(colorway=px.colors.qualitative.Set3)

            st.plotly_chart(fig)

if __name__ == "__main__":
    select_data_dashboard()
