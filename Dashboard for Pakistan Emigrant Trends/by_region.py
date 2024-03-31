import streamlit as st
import pandas as pd
import plotly.express as px

# Load emigrants dataset
emigration_data = pd.read_excel("F:\streamlit project\Emigrants Data (1981-2023).xlsx")

# Emigrants Map page
def by_region():
    st.markdown("## Year wise Trends ")

    # Sidebar for selecting region and year
    selected_region = st.sidebar.selectbox("Select Region", emigration_data['Destination Region'].unique())
    start_year = st.sidebar.selectbox("Select Starting Year", emigration_data['Year'].unique())
    end_year = st.sidebar.selectbox("Select Ending Year", emigration_data['Year'].unique())

    # Filter data based on selected region and year range
    filtered_data = emigration_data[(emigration_data['Destination Region'] == selected_region) & 
                                    (emigration_data['Year'] >= start_year) & 
                                    (emigration_data['Year'] <= end_year)]

    # Create a bar graph showing number of emigrants for each country in the selected region and year
    if not filtered_data.empty:
        # Calculate statistics
        max_emigrants = filtered_data['No. of Emigrants'].max()
        min_emigrants = filtered_data['No. of Emigrants'].min()
        avg_emigrants = filtered_data['No. of Emigrants'].mean()
        
        if start_year == end_year:
            # For a single year, display the counts
            total_emigrants = filtered_data['No. of Emigrants'].sum()

            # Get country names corresponding to maximum and minimum counts and year
            max_row = filtered_data.loc[filtered_data['No. of Emigrants'].idxmax()]
            min_row = filtered_data.loc[filtered_data['No. of Emigrants'].idxmin()]
            country_max = max_row['Destination Country']
            year_max = max_row['Year']
            country_min = min_row['Destination Country']
            year_min = min_row['Year']

            # Create the bar graph for a single year
            fig = px.bar(filtered_data, x='Destination Country', y='No. of Emigrants', 
                        title=f'Emigrants Count for Countries in {selected_region} in {start_year}',
                        labels={'Destination Country': 'Country', 'No. of Emigrants': 'Number of Emigrants'},
                        color='No. of Emigrants')

        else:
            # Aggregate data for the selected range of years
            aggregated_data = filtered_data.groupby('Destination Country')['No. of Emigrants'].sum().reset_index()

            # Calculate statistics for the range of years
            total_emigrants = aggregated_data['No. of Emigrants'].sum()
            max_row = filtered_data.loc[filtered_data['No. of Emigrants'].idxmax()]
            min_row = filtered_data.loc[filtered_data['No. of Emigrants'].idxmin()]
            country_max = max_row['Destination Country']
            year_max = max_row['Year']
            country_min = min_row['Destination Country']
            year_min = min_row['Year']

            # Create the bar graph for the range of years
            fig = px.bar(aggregated_data, x='Destination Country', y='No. of Emigrants', 
                        title=f'Total Emigrants Count for Countries in {selected_region} from {start_year} to {end_year}',
                        labels={'Destination Country': 'Country', 'No. of Emigrants': 'Number of Emigrants'},
                        color='No. of Emigrants')

        # Add total emigrants on the top left corner
        fig.add_annotation(x=0, y=1, xref='paper', yref='paper', text=f'Total Emigrants: {total_emigrants}', 
                        showarrow=False, font=dict(color='white', size=14))
        # Add statistics to the graph
        fig.add_annotation(x=0, y=0.95, xref='paper', yref='paper', text=f'Max ({country_max} - {year_max}): {max_emigrants}', 
                        showarrow=False, font=dict(color='orange', size=14))
        fig.add_annotation(x=0, y=0.9, xref='paper', yref='paper', text=f'Min ({country_min} - {year_min}): {min_emigrants}', 
                        showarrow=False, font=dict(color='lightblue', size=14))
        fig.add_annotation(x=0, y=0.85, xref='paper', yref='paper', text=f'Avg: {avg_emigrants:.2f}', 
                        showarrow=False, font=dict(color='lightgray', size=14))

        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',  # Set plot background color to transparent
            paper_bgcolor='rgba(0,0,0,0)',  # Set paper background color to transparent
            font=dict(color='white'),  # Set font color to white
            hovermode='x unified',  # Set hover mode to display hover information for all data points at a given x-value
            height=450,  # Set height of the graph
            width=850,  # Set width of the graph
        )

        st.plotly_chart(fig)
    else:
        st.write("No data available for the selected region and year range.")

        # st.markdown("## Year wise Trends ")
    # # Sidebar for selecting region and year
    # selected_region = st.sidebar.selectbox("Select Region", emigration_data['Destination Region'].unique())
    # selected_year = st.sidebar.selectbox("Select Year", emigration_data['Year'].unique())

    # # Filter data based on selected region and year
    # filtered_data = emigration_data[(emigration_data['Destination Region'] == selected_region) & (emigration_data['Year'] == selected_year)]

    # # Create a bar graph showing number of emigrants for each country in the selected region and year
    # if not filtered_data.empty:
    #     # Calculate statistics
    #     max_emigrants = filtered_data['No. of Emigrants'].max()
    #     min_emigrants = filtered_data['No. of Emigrants'].min()
    #     avg_emigrants = filtered_data['No. of Emigrants'].mean()
    #     total_emigrants = filtered_data['No. of Emigrants'].sum()

    #     # Get country names corresponding to maximum and minimum counts
    #     country_max = filtered_data.loc[filtered_data['No. of Emigrants'].idxmax()]['Destination Country']
    #     country_min = filtered_data.loc[filtered_data['No. of Emigrants'].idxmin()]['Destination Country']

    #     # Create the bar graph
    #     fig = px.bar(filtered_data, x='Destination Country', y='No. of Emigrants', 
    #                 title=f'Emigrants Count for Countries in {selected_region} in {selected_year}',
    #                 labels={'Destination Country': 'Country', 'No. of Emigrants': 'Number of Emigrants'},
    #                 color='No. of Emigrants')

    #     # Add total emigrants on the top left corner
    #     fig.add_annotation(x=0, y=1, xref='paper', yref='paper', text=f'Total Emigrants: {total_emigrants}', 
    #                     showarrow=False, font=dict(color='white', size=14))
    #     # Add statistics to the graph
    #     fig.add_annotation(x=0, y=0.95, xref='paper', yref='paper', text=f'Max ({country_max}): {max_emigrants}', 
    #                     showarrow=False, font=dict(color='orange', size=14))
    #     fig.add_annotation(x=0, y=0.9, xref='paper', yref='paper', text=f'Min ({country_min}): {min_emigrants}', 
    #                     showarrow=False, font=dict(color='lightblue', size=14))
    #     fig.add_annotation(x=0, y=0.85, xref='paper', yref='paper', text=f'Avg: {avg_emigrants:.2f}', 
    #                     showarrow=False, font=dict(color='lightgray', size=14))
        
    #     # Add emigrant count on each bar
    #     for i in range(len(filtered_data)):
    #         color = 'red' if filtered_data['No. of Emigrants'].iloc[i] < avg_emigrants else 'blue'
    #         fig.add_annotation(x=filtered_data['Destination Country'].iloc[i], y=filtered_data['No. of Emigrants'].iloc[i],
    #                         text=str(filtered_data['No. of Emigrants'].iloc[i]),
    #                         showarrow=False, font=dict(color='white', size=10), textangle=45,
    #                         bgcolor=color)

    #     fig.update_layout(
    #         plot_bgcolor='rgba(0,0,0,0)',  # Set plot background color to transparent
    #         paper_bgcolor='rgba(0,0,0,0)',  # Set paper background color to transparent
    #         font=dict(color='white'),  # Set font color to white
    #         hovermode='x unified',  # Set hover mode to display hover information for all data points at a given x-value
    #         height=450,  # Set height of the graph
    #         width=800,  # Set width of the graph
    #     )

    #     st.plotly_chart(fig)
    # else:
    #     st.write("No data available for the selected region and year.")