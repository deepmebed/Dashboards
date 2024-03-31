
import pandas as pd
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt


# Load emigrants dataset
emigration_data = pd.read_excel("F:\streamlit project\Emigrants Data (1981-2023).xlsx")
def by_country():

    # Calculate total number of emigrants
    total_emigrants = emigration_data['No. of Emigrants'].sum()

    # Find year and details with maximum emigrants
    max_emigrants_row = emigration_data.loc[emigration_data['No. of Emigrants'].idxmax()]

    # Find year and details with minimum emigrants
    min_emigrants_row = emigration_data.loc[emigration_data['No. of Emigrants'].idxmin()]

    # Calculate percentage of total emigrants
    min_emigrants_percentage = (min_emigrants_row['No. of Emigrants'] / total_emigrants) * 100
    max_emigrants_percentage = (max_emigrants_row['No. of Emigrants'] / total_emigrants) * 100

    # Create three expanders side by side horizontally
    col1, col2, col3 = st.columns(3)

    # Expander 1: Total emigrants
    with col1:
        with st.expander("**Total Emigrants**", expanded=True):
            st.write(f"Total number of emigrants: **{total_emigrants}**")

    # Expander 3: Maximum emigrants
    with col2:
        with st.expander("**Maximum Emigrants**"):
            st.write(f"Year: **{max_emigrants_row['Year']}**")
            st.write(f"Region: **{max_emigrants_row['Destination Region']}**")
            st.write(f"Country: **{max_emigrants_row['Destination Country']}**")
            st.write(f"Count: **{max_emigrants_row['No. of Emigrants']}**")
            st.write(f"Percentage of  Emigrants: **{max_emigrants_percentage:.2f}%**")

    # Expander 2: Minimum emigrants
    with col3:
        with st.expander("**Minimum Emigrants**"):
            st.write(f"Year: **{min_emigrants_row['Year']}**")
            st.write(f"Region: **{min_emigrants_row['Destination Region']}**")
            st.write(f"Country: **{min_emigrants_row['Destination Country']}**")
            st.write(f"Count: **{min_emigrants_row['No. of Emigrants']}**")
            st.write(f"Percentage of  Emigrants: **{min_emigrants_percentage:.2f}%**")

    # Streamlit app
    st.markdown("## Country wise Trends ")

    # Sidebar for selecting region, country, and year range
    selected_region = st.sidebar.selectbox("Select Region", emigration_data['Destination Region'].unique())
    countries_in_region = emigration_data[emigration_data['Destination Region'] == selected_region]['Destination Country'].unique()
    selected_country = st.sidebar.selectbox("Select Country", countries_in_region)
    starting_year = st.sidebar.slider("Starting Year", min_value=emigration_data['Year'].min(), max_value=emigration_data['Year'].max(), value=emigration_data['Year'].min())
    ending_year = st.sidebar.slider("Ending Year", min_value=emigration_data['Year'].min(), max_value=emigration_data['Year'].max(), value=emigration_data['Year'].max())

    # Filter data based on selected region, country, and year range
    filtered_data = emigration_data[(emigration_data['Destination Region'] == selected_region) & 
                                    (emigration_data['Destination Country'] == selected_country) & 
                                    (emigration_data['Year'] >= starting_year) &
                                    (emigration_data['Year'] <= ending_year)]

    # Create a bar graph showing number of emigrants for each year
    if not filtered_data.empty:
        total_emigrants = filtered_data['No. of Emigrants'].sum()  # Calculate total emigrants for selected country

        fig = px.bar(filtered_data, x='Year', y='No. of Emigrants', title=f'Emigrants Over Time in {selected_country} ',
                    labels={'Year': 'Year', 'No. of Emigrants': 'Number of Emigrants'}, color='No. of Emigrants')

        # Calculate maximum and minimum years
        max_year_data = filtered_data.loc[filtered_data['No. of Emigrants'].idxmax()]
        min_year_data = filtered_data.loc[filtered_data['No. of Emigrants'].idxmin()]

        # Calculate average count
        avg_emigrants = filtered_data['No. of Emigrants'].mean()

        # Add annotations for maximum and minimum years
        fig.add_annotation(x=0, y=1, xref='paper', yref='paper', text=f'Total Emigrants: {total_emigrants}',
                        showarrow=False, font=dict(color='white', size=14))

        fig.add_annotation(x=0, y=0.95, xref='paper', yref='paper',
                        text=f'Max Year: {max_year_data["Year"]} ({max_year_data["No. of Emigrants"]} emigrants)',
                        showarrow=False, font=dict(color='orange', size=14))
        fig.add_annotation(x=0, y=0.9, xref='paper', yref='paper',
                        text=f'Min Year: {min_year_data["Year"]} ({min_year_data["No. of Emigrants"]} emigrants)',
                        showarrow=False, font=dict(color='lightblue', size=14))
        fig.add_annotation(x=0, y=0.85, xref='paper', yref='paper', text=f'Avg Emigrants: {avg_emigrants:.2f}',
                        showarrow=False, font=dict(color='lightgray', size=14))

        # Add emigrant count on each bar with an angle of 45 degrees
        for i in range(len(filtered_data)):
            color = 'red' if filtered_data['No. of Emigrants'].iloc[i] < avg_emigrants else 'blue'
            fig.add_annotation(x=filtered_data['Year'].iloc[i], y=filtered_data['No. of Emigrants'].iloc[i],
                            text=str(filtered_data['No. of Emigrants'].iloc[i]),
                            showarrow=False, font=dict(color='white', size=10), textangle=45,
                            bgcolor=color)

        fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Set plot background color to transparent
        paper_bgcolor='rgba(0,0,0,0)',  # Set paper background color to transparent
        font=dict(color='white'),  # Set font color to white
        hovermode='x unified',  # Set hover mode to display hover information for all data points at a given x-value
        height=550,  # Set height of the graph
        width=850    # Set width of the graph
    )

        st.plotly_chart(fig)
    else:
        st.write("No data available for the selected region, country, and year range.")