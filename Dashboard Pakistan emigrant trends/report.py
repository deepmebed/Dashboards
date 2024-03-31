import pandas as pd
import streamlit as st
import base64  # Import base64 module
import altair as alt  # Import altair for creating charts

# Load emigrants dataset
emigration_data = pd.read_excel("F:/streamlit project/Emigrants Data (1981-2023).xlsx")

# Emigrants Report page
def report_():
    try:
        # Sidebar for selecting region, start year, end year, and number of top countries
        selected_region = st.sidebar.selectbox("Select Region", emigration_data['Destination Region'].unique())
        start_year = st.sidebar.selectbox("Select Starting Year", range(1981, 2024), index=1)
        end_year = st.sidebar.selectbox("Select Ending Year", range(1981, 2024), index=42)

        # Filter data based on selected region
        region_data = emigration_data[emigration_data['Destination Region'] == selected_region]

        # Get unique countries within the selected region
        unique_countries_in_region = region_data['Destination Country'].unique()

        top_countries = st.sidebar.slider("Select Number of Top Countries", min_value=1,
                                          max_value=len(unique_countries_in_region), value=5)

        st.markdown(f"## Report of {selected_region} ({start_year}-{end_year})")

        # Filter data based on selected region and year range
        filtered_data = region_data[(region_data['Year'] >= start_year) &
                                    (region_data['Year'] <= end_year)]

        # Aggregate data for the selected range of years
        aggregated_data = filtered_data.groupby('Destination Country')['No. of Emigrants'].sum().reset_index()
        aggregated_data = aggregated_data.sort_values(by='No. of Emigrants', ascending=False).reset_index(drop=True)

        # Calculate total number of emigrants
        total_emigrants = aggregated_data['No. of Emigrants'].sum()

        # Append total number of emigrants as a new row to the DataFrame
        top_aggregated_data = aggregated_data.head(top_countries)
        top_aggregated_data.loc[len(top_aggregated_data)] = ['Total', top_aggregated_data['No. of Emigrants'].sum()]

        # Display table with region, country names, number of emigrants, and total
        st.write("### Table of Emigration Data:")
        st.table(top_aggregated_data)



    except Exception as e:
        st.error(f"An error occurred: {e}")

# report_()
