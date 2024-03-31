
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
import plotly.express as px

# Load emigrants dataset
emigration_data = pd.read_excel("F:\streamlit project\Emigrants Data (1981-2023).xlsx")


# Home page
def home_page(): 

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

    
    
    # Group emigration data by year and sum the number of emigrants
    emigration_by_year = emigration_data.groupby('Year')['No. of Emigrants'].sum().reset_index()

    # Calculate mean, maximum, and minimum values
    mean_value = round(emigration_by_year['No. of Emigrants'].mean(),2)
    max_value = emigration_by_year['No. of Emigrants'].max()
    min_value = emigration_by_year['No. of Emigrants'].min()

    # Find the year for maximum and minimum values
    max_year = emigration_by_year.loc[emigration_by_year['No. of Emigrants'].idxmax()]['Year']
    min_year = emigration_by_year.loc[emigration_by_year['No. of Emigrants'].idxmin()]['Year']

    # Create a line plot using Plotly Express
    line_plot = px.line(emigration_by_year, x='Year', y='No. of Emigrants', 
                        title='Emigrants Over the Years', 
                        labels={'Year': 'Year', 'No. of Emigrants': 'Number of Emigrants'},
                        hover_data={'No. of Emigrants': True, 'Year': True})

    # Change line color when it increases from the mean value
    line_plot.data[0].update(mode='lines+markers', line=dict(color='blue'))

    # Add shape for the mean line
    line_plot.add_shape(type="line",
                        x0=emigration_by_year['Year'].min(), y0=mean_value, 
                        x1=emigration_by_year['Year'].max(), y1=mean_value,
                        line=dict(color="red", width=2, dash='dash'))

    # Add annotations for mean, maximum, and minimum values
    line_plot.add_annotation(xref='paper', yref='paper', x=0.1, y=0.98,
                            text=f'Max: {max_value} ({max_year})', showarrow=False, 
                            font=dict(color='lightgray', size=14))
    line_plot.add_annotation(xref='paper', yref='paper', x=0.1, y=0.90,
                            text=f'Min: {min_value} ({min_year})', showarrow=False, 
                            font=dict(color='lightblue', size=14))
    line_plot.add_annotation(xref='paper', yref='paper', x=0.1, y=0.82,
                            text=f'Mean: {mean_value}', showarrow=False,
                            font=dict(color='red', size=14))

    # Customize layout
    line_plot.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Set plot background color to transparent
        paper_bgcolor='rgba(0,0,0,0)',  # Set paper background color to transparent
        font=dict(color='white'),  # Set font color to white
        hovermode='x unified',  # Set hover mode to display hover information for all data points at a given x-value
        height=450,  # Set height of the graph
        width=850    # Set width of the graph
    )

    # Streamlit app
    st.title('Emigrants Over the Years')
    # st.write("Total number of emigrants over the years")

    # Display Plotly line plot using Streamlit's Plotly chart function
    st.plotly_chart(line_plot)


    ######################################################################################
    # Group data by Destination Region and count the number of emigrants
    region_counts = emigration_data.groupby('Destination Region')['No. of Emigrants'].sum().reset_index()

    # Calculate percentage for each region
    total_emigrants = region_counts['No. of Emigrants'].sum()
    region_counts['Percentage'] = region_counts['No. of Emigrants'] / total_emigrants * 100

    # Plot based on selected plot type
    plot_type = st.radio("Select Plot Type", ['Line', 'Bar'])
    if plot_type == 'Line':
        # Create line plot
        fig = px.line(region_counts, x='Destination Region', y='No. of Emigrants', 
                    title='Total Emigrants by Destination Region (1981-2023)',
                    labels={'No. of Emigrants': 'Number of Emigrants', 'Destination Region': 'Region'},
                    hover_data={'Percentage': ':.2f%'})
    else:
        # Create bar plot
        fig = px.bar(region_counts, x='Destination Region', y='No. of Emigrants', 
                    title='Total Emigrants by Destination Region (1981-2023)',
                    labels={'No. of Emigrants': 'Number of Emigrants', 'Destination Region': 'Region'},
                    hover_data={'Percentage': ':.2f%'})

    # Customize layout
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Set plot background color to transparent
        paper_bgcolor='rgba(0,0,0,0)',  # Set paper background color to transparent
        font=dict(color='white'),  # Set font color to white
        hovermode='x unified',  # Set hover mode to display hover information for all data points at a given x-value
        height=550,  # Set height of the graph
        width=850    # Set width of the graph
    )


    # Display plot
    st.plotly_chart(fig)