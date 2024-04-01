import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Set page configuration
st.set_page_config(layout="wide")



# Load the dataset
def load_data(csv_file_path):
    df = pd.read_csv(csv_file_path)
    return df
# Load data
df = load_data(r'C:\Users\Eman\Downloads\depressive-disorders-prevalence-ihme.csv')
df = load_data(r'C:\Users\Eman\Downloads\anxiety-disorders-prevalence.csv')


# Page 1: Introduction
def page_introduction():
    st.title("Exploring the Impact of Demographic, Economic, and Geographic Factors on Mental Health Disorders")
    st.markdown(
        """
        Welcome to the Mental Health Explorer dashboard! This interactive tool delves into the world of mental health, analyzing how demographic, economic, and geographic factors influence the prevalence and treatment of mental disorders across various populations and regions.
        """
    )

    st.image(r'C:\Users\Eman\Downloads\mental-health-2019924_640.jpg', width=500)  # Adjust width as needed

    st.write("### How to Use:")
    st.write(
        """
        - Use the sidebar navigation to explore different sections of the dashboard.
        - Each section provides insights into different aspects of mental health disorders such as depression, anxiety, and eating disorders.
        - Interact with the visualizations to gain deeper insights into the data.
        """
    )

    # Data for the bar chart
    data = {
        'Condition': ['Anxiety', 'Depression', 'Eating disorders'],
        'Prevalence Rate (%)': [4.1, 3.8, 0.2]
    }

    df = pd.DataFrame(data)

    # Create the bar chart
    fig = px.bar(df, x='Condition', y='Prevalence Rate (%)', color='Condition',
                 title='Average Prevalence Rates of Mental Health Conditions')
    # Customize layout
    fig.update_layout(xaxis_title=None, yaxis_title='Prevalence Rate (%)')
    fig.update_traces(marker_line_width=1.5, marker_line_color="black")

    # Display the bar chart
    st.plotly_chart(fig)


# Page 2: Data Exploration
def page_depressive_prevalence():
    st.title("Depressive Disorders Prevalence")
    # Load data for depressive disorders
    df_depressive = load_data(r'C:\Users\Eman\Downloads\depressive-disorders-prevalence-ihme.csv')
    df = load_data(r'C:\Users\Eman\Downloads\depressive-disorders-prevalence-vs-gdp.csv')

    # Get unique countries
    countries = df_depressive['Entity'].unique()

    # Display dropdown to select country
    selected_country = st.selectbox('Select Country', countries)

    # Filter data for selected country
    filtered_data_depressive = df[df['Entity'] == selected_country]

    # Get unique years
    years = filtered_data_depressive['Year'].unique()

    # Slider to select years
    min_year = int(min(years))
    max_year = int(max(years))
    selected_years = st.slider('Select Years', min_year, max_year, (min_year, max_year))

    # Filter data for selected years
    filtered_data = filtered_data_depressive[
        (filtered_data_depressive['Year'] >= selected_years[0]) & (
                    filtered_data_depressive['Year'] <= selected_years[1])]

    # Ask user for preferred chart type
    chart_type = st.selectbox("Select Chart Type", options=["None", "Line Chart", "Histogram", "Choropleth Map"])

    # Display selected chart type and map
    if chart_type == "Line Chart":
        # Display line chart for anxiety disorders prevalence over years
        st.subheader(
            f'Depressive Disorders Prevalence Trend in {selected_country} ({selected_years[0]} - {selected_years[1]})')
        fig = px.line(filtered_data, x='Year',
                      y='Depressive disorders (share of population) - Sex: Both - Age: Age-standardized',
                      title=f'Depressive Disorders Prevalence Trend in {selected_country} ({selected_years[0]} - {selected_years[1]})')
        st.plotly_chart(fig)
    elif chart_type == "Histogram":
        # Display interactive histogram for distribution of prevalence rates
        st.subheader(f'Distribution of Depressive Disorders Prevalence Rates in {selected_country}')
        fig = px.histogram(filtered_data,
                           x='Depressive disorders (share of population) - Sex: Both - Age: Age-standardized',
                           title=f'Histogram of Depressive Disorders Prevalence Rates in {selected_country}',
                           labels={
                               'Depressive disorders (share of population) - Sex: Both - Age: Age-standardized': 'Prevalence Rate (%)'})
        fig.update_layout(xaxis_title="Prevalence Rate (%)", yaxis_title="Frequency")
        st.plotly_chart(fig)
    elif chart_type == "Choropleth Map":
        # Load data for all countries
        all_countries_data = load_data(r'C:\Users\Eman\Downloads\depressive-disorders-prevalence-ihme.csv')
        # Create choropleth map
        fig_map = px.choropleth(all_countries_data,
                                locations="Entity",
                                locationmode="country names",
                                color="Depressive disorders (share of population) - Sex: Both - Age: Age-standardized",
                                hover_name="Entity",
                                color_continuous_scale="Viridis",
                                title=f"Depressive Disorders Prevalence Worldwide",
                                labels={
                                    'Depressive disorders (share of population) - Sex: Both - Age: Age-standardized': 'Prevalence Rate (%)'},
                                template='plotly_dark',  # Change template for dark theme
                                projection='natural earth',  # Use natural earth projection
                                scope='world',  # Show world map
                                width=1000,  # Set width
                                height=600,  # Set height
                                )
        fig_map.update_layout(geo=dict(showcoastlines=True))
        fig_map.update_geos(
            showcountries=True,  # Show country borders
            countrycolor="Gray",  # Set country border color
            showland=True,  # Show land
            landcolor="LightGray",  # Set land color
            showocean=True,  # Show ocean
            oceancolor="LightBlue",  # Set ocean color
        )
        # Customize colorbar
        fig_map.update_coloraxes(colorbar=dict(
            title="Prevalence Rate (%)",  # Set colorbar title
            ticks="outside",  # Place colorbar ticks outside
            tickvals=[0, 5, 10, 15],  # Set colorbar tick values
            ticktext=["0", "5", "10", "15+"],  # Set colorbar tick labels
            len=0.5,  # Set colorbar length
            thickness=20,  # Set colorbar thickness
        ))
        # Slider for selecting year
        year_slider = st.slider('Select Year', min_year, max_year, min_year)
        # Filter data for selected year
        filtered_data_year = all_countries_data[all_countries_data['Year'] == year_slider]
        # Update map data
        fig_map.update_traces(locations=filtered_data_year['Entity'],
                              z=filtered_data_year[
                                  'Depressive disorders (share of population) - Sex: Both - Age: Age-standardized'])
        # Display the map
        st.plotly_chart(fig_map)
    # Update chart type in session state
    st.session_state.chart_type = chart_type
    # Select continent
    selected_continent = st.selectbox("Select Continent", ['None'] + list(df['Continent'].unique()))

    if selected_continent != 'None':
        # Slider for selecting year range
        min_year = df['Year'].min()
        max_year = df['Year'].max()
        selected_year_range = st.slider("Select Year Range", min_value=min_year, max_value=max_year,
                                        value=(min_year, max_year))

        # Filter data based on selected continent and year range
        filtered_df = df[(df['Continent'] == selected_continent) &
                         (df['Year'].between(selected_year_range[0], selected_year_range[1]))]

        # Scatter plot showing relationship between depressive disorders prevalence and GDP per capita
        st.subheader(
            f"Depressive Disorders Prevalence vs. GDP per Capita in {selected_continent} ({selected_year_range[0]} - {selected_year_range[1]})")
        fig = px.scatter(filtered_df,
                         x='Depressive disorders (share of population) - Sex: Both - Age: Age-standardized',
                         y='GDP per capita, PPP (constant 2017 international $)', color='Entity',
                         title=f"Depressive Disorders Prevalence vs. GDP per Capita in {selected_continent} ({selected_year_range[0]} - {selected_year_range[1]})",
                         hover_name='Entity', labels={



        "Depressive disorders (share of population) - Sex: Both - Age: Age-standardized": "Prevalence"})

        # Customize layout
        fig.update_layout(xaxis_title="Depressive Disorders Prevalence", yaxis_title="GDP per Capita")
        st.plotly_chart(fig)
    else:
        st.write("Please select a continent.")

# Page 3: Anxiety Disorders Prevalence
def page_anxiety_prevalence():
    st.title("Anxiety Disorders Prevalence")
    # Load data
    df = load_data(r'C:\Users\Eman\Downloads\anxiety-disorders-prevalence.csv')
    df_gdp = load_data(r'C:\Users\Eman\Downloads\anxiety-disorders-prevalence-vs-gdp.csv')
    # Get unique countries
    countries = df['Entity'].unique()
    # Display dropdown to select country
    selected_country = st.selectbox('Select Country', countries)
    # Filter data for selected country
    filtered_data = df[df['Entity'] == selected_country]
    # Get unique years
    years = filtered_data['Year'].unique()
    # Slider to select years
    min_year = int(min(years))
    max_year = int(max(years))
    selected_years = st.slider('Select Years', min_year, max_year, (min_year, max_year))
    # Filter data for selected years
    filtered_data = filtered_data[
        (filtered_data['Year'] >= selected_years[0]) & (filtered_data['Year'] <= selected_years[1])]
    # Ask user for preferred chart type
    chart_type = st.selectbox("Select Chart Type", options=["None", "Line Chart", "Histogram", "Choropleth Map"])
    # Display selected chart type and map
    if chart_type == "Line Chart":
        # Display line chart for anxiety disorders prevalence over years
        st.subheader(
            f'Anxiety Disorders Prevalence Trend in {selected_country} ({selected_years[0]} - {selected_years[1]})')
        fig = px.line(filtered_data, x='Year',
                      y='Anxiety disorders (share of population) - Sex: Both - Age: Age-standardized',
                      title=f'Anxiety Disorders Prevalence Trend in {selected_country} ({selected_years[0]} - {selected_years[1]})')
        st.plotly_chart(fig)
    elif chart_type == "Histogram":
        # Display interactive histogram for distribution of prevalence rates
        st.subheader(f'Distribution of Anxiety Disorders Prevalence Rates in {selected_country}')
        fig = px.histogram(filtered_data,
                           x='Anxiety disorders (share of population) - Sex: Both - Age: Age-standardized',
                           title=f'Histogram of Anxiety Disorders Prevalence Rates in {selected_country}',
                           labels={
                               'Anxiety disorders (share of population) - Sex: Both - Age: Age-standardized': 'Prevalence Rate (%)'})
        fig.update_layout(xaxis_title="Prevalence Rate (%)", yaxis_title="Frequency")
        st.plotly_chart(fig)
    elif chart_type == "Choropleth Map":
        # Load data for all countries
        all_countries_data = load_data(r'C:\Users\Eman\Downloads\anxiety-disorders-prevalence.csv')
        # Create choropleth map
        fig_map = px.choropleth(all_countries_data,
                                locations="Entity",
                                locationmode="country names",
                                color="Anxiety disorders (share of population) - Sex: Both - Age: Age-standardized",
                                hover_name="Entity",
                                color_continuous_scale="Viridis",
                                title=f"Anxiety Disorders Prevalence Worldwide",
                                labels={
                                    'Anxiety disorders (share of population) - Sex: Both - Age: Age-standardized': 'Prevalence Rate (%)'},
                                template='plotly_dark',  # Change template for dark theme
                                projection='natural earth',  # Use natural earth projection
                                scope='world',  # Show world map
                                width=1000,  # Set width
                                height=600,  # Set height
                                )
        fig_map.update_layout(geo=dict(showcoastlines=True))
        fig_map.update_geos(
            showcountries=True,  # Show country borders
            countrycolor="Gray",  # Set country border color
            showland=True,  # Show land
            landcolor="LightGray",  # Set land color
            showocean=True,  # Show ocean
            oceancolor="LightBlue",  # Set ocean color
        )
        # Customize colorbar
        fig_map.update_coloraxes(colorbar=dict(
            title="Prevalence Rate (%)",  # Set colorbar title
            ticks="outside",  # Place colorbar ticks outside
            tickvals=[0, 5, 10, 15],  # Set colorbar tick values
            ticktext=["0", "5", "10", "15+"],  # Set colorbar tick labels
            len=0.5,  # Set colorbar length
            thickness=20,  # Set colorbar thickness
        ))
        # Slider for selecting year
        year_slider = st.slider('Select Year', min_year, max_year, min_year)
        # Filter data for selected year
        filtered_data_year = all_countries_data[all_countries_data['Year'] == year_slider]
        # Update map data
        fig_map.update_traces(locations=filtered_data_year['Entity'],
                              z=filtered_data_year[
                                  'Anxiety disorders (share of population) - Sex: Both - Age: Age-standardized'])
        # Display the map
        st.plotly_chart(fig_map)
    # Update chart type in session state
    st.session_state.chart_type = chart_type

    # Select continent
    selected_continent = st.selectbox("Select Continent", ['None'] + list(df_gdp['Continent'].unique()))

    if selected_continent != 'None':
        # Slider for selecting year range
        min_year = df_gdp['Year'].min()
        max_year = df_gdp['Year'].max()
        selected_year_range = st.slider("Select Year Range", min_value=min_year, max_value=max_year,
                                        value=(min_year, max_year))

        # Filter data based on selected continent and year range
        filtered_df_gdp = df_gdp[(df_gdp['Continent'] == selected_continent) &
                                 (df_gdp['Year'].between(selected_year_range[0], selected_year_range[1]))]

        # Scatter plot showing relationship between anxiety disorders prevalence and GDP per capita
        st.subheader(
            f"Anxiety Disorders Prevalence vs. GDP per Capita in {selected_continent} ({selected_year_range[0]} - {selected_year_range[1]})")
        fig = px.scatter(filtered_df_gdp,
                         x='Anxiety disorders (share of population) - Sex: Both - Age: Age-standardized',
                         y='GDP per capita, PPP (constant 2017 international $)', color='Entity',
                         title=f"Anxiety Disorders Prevalence vs. GDP per Capita in {selected_continent} ({selected_year_range[0]} - {selected_year_range[1]})",
                         hover_name='Entity', labels={
                "Anxiety disorders (share of population) - Sex: Both - Age: Age-standardized": "Prevalence"})
        # Customize layout
        fig.update_layout(xaxis_title="Anxiety Disorders Prevalence", yaxis_title="GDP per Capita")
        st.plotly_chart(fig)
    else:
        st.write("Please select a continent.")

def page_eating_disorder():
    st.title("Eating Disorders")
    # Load data
    df_eating = load_data(r'C:\Users\Eman\Downloads\eating-disorders-prevalence.csv')

    # Get unique countries
    countries = df_eating['Entity'].unique()
    # Display dropdown to select country
    selected_country = st.selectbox('Select Country', countries)
    # Filter data for selected country
    filtered_data = df_eating[df_eating['Entity'] == selected_country]
    # Get unique years
    years = filtered_data['Year'].unique()
    # Slider to select years
    min_year = int(min(years))
    max_year = int(max(years))
    selected_years = st.slider('Select Years', min_year, max_year, (min_year, max_year))
    # Filter data for selected years
    filtered_data = filtered_data[
        (filtered_data['Year'] >= selected_years[0]) & (filtered_data['Year'] <= selected_years[1])]
    # Ask user for preferred chart type
    chart_type = st.selectbox("Select Chart Type", options=["None", "Line Chart", "Histogram", "Choropleth Map"])
    # Display selected chart type and map
    if chart_type == "Line Chart":
        # Display line chart for eating disorders prevalence over years
        st.subheader(f'Eating Disorders Trend in {selected_country} ({selected_years[0]} - {selected_years[1]})')
        fig = px.line(filtered_data, x='Year',
                      y='Eating disorders (share of population) - Sex: Both - Age: Age-standardized',
                      title=f'Eating Disorders Trend in {selected_country} ({selected_years[0]} - {selected_years[1]})')
        st.plotly_chart(fig)
    elif chart_type == "Histogram":
        # Display interactive histogram for distribution of prevalence rates
        st.subheader(f'Distribution of Eating Disorders Rates in {selected_country}')
        fig = px.histogram(filtered_data,
                           x='Eating disorders (share of population) - Sex: Both - Age: Age-standardized',
                           title=f'Histogram of Eating Disorders Rates in {selected_country}',
                           labels={'Eating disorders (share of population) - Sex: Both - Age: Age-standardized': 'Prevalence Rate (%)'})
        fig.update_layout(xaxis_title="Prevalence Rate (%)", yaxis_title="Frequency")
        st.plotly_chart(fig)
    elif chart_type == "Choropleth Map":
        # Load data for all countries
        all_countries_data = load_data(r'C:\Users\Eman\Downloads\eating-disorders-prevalence.csv')
        # Create choropleth map
        fig_map = px.choropleth(all_countries_data,
                                locations="Entity",
                                locationmode="country names",
                                color="Eating disorders (share of population) - Sex: Both - Age: Age-standardized",
                                hover_name="Entity",
                                color_continuous_scale="Viridis",
                                title=f"Eating Disorders Worldwide",
                                labels={'Eating disorders (share of population) - Sex: Both - Age: Age-standardized': 'Prevalence Rate (%)'},
                                template='plotly_dark',  # Change template for dark theme
                                projection='natural earth',  # Use natural earth projection
                                scope='world',  # Show world map
                                width=1000,  # Set width
                                height=600,  # Set height
                                )
        fig_map.update_layout(geo=dict(showcoastlines=True))
        fig_map.update_geos(
            showcountries=True,  # Show country borders
            countrycolor="Gray",  # Set country border color
            showland=True,  # Show land
            landcolor="LightGray",  # Set land color
            showocean=True,  # Show ocean
            oceancolor="LightBlue",  # Set ocean color
        )
        # Customize colorbar
        fig_map.update_coloraxes(colorbar=dict(
            title="Prevalence Rate (%)",  # Set colorbar title
            ticks="outside",  # Place colorbar ticks outside
            tickvals=[0, 5, 10, 15],  # Set colorbar tick values
            ticktext=["0", "5", "10", "15+"],  # Set colorbar tick labels
            len=0.5,  # Set colorbar length
            thickness=20,  # Set colorbar thickness
        ))
        # Slider for selecting year
        year_slider = st.slider('Select Year', min_year, max_year, min_year)
        # Filter data for selected year
        filtered_data_year = all_countries_data[all_countries_data['Year'] == year_slider]
        # Update map data
        fig_map.update_traces(locations=filtered_data_year['Entity'],
                              z=filtered_data_year['Eating disorders (share of population) - Sex: Both - Age: Age-standardized'])
        # Display the map
        st.plotly_chart(fig_map)
    # Update chart type in session state
    st.session_state.chart_type = chart_type
# Page 4: Conclusion and Recommendations
def page_surveys():
    # Load the dataset
    csv_file_path = r'C:\Users\Eman\Downloads\Text File.txt'
    df = pd.read_csv(csv_file_path)

    # Page title
    st.title('Anxiety/Depression Survey Analysis')

    # Select country
    countries = ['None', 'All'] + list(df['Entity'].unique())
    selected_country = st.selectbox('Select Country', countries)

    # Select condition
    conditions = df.columns[3:]  # Exclude non-relevant columns
    selected_condition = st.selectbox('Select Condition', conditions)

    # Filter by country if not "None" selected
    if selected_country != 'None':
        if selected_country == 'All':
            filtered_df_country = df
            title_country = 'All Countries'
        else:
            filtered_df_country = df[df['Entity'] == selected_country]
            title_country = selected_country

        # Bar chart
        st.subheader(f'Percentage of People Engaged in {selected_condition} in {title_country}')
        fig_bar = px.bar(filtered_df_country, x='Entity', y=selected_condition,
                         title=f'Percentage of People Engaged in {selected_condition} in {title_country}',
                         labels={'Entity': 'Country', selected_condition: 'Percentage'},
                         width=800, height=500)
        fig_bar.update_layout(xaxis_title='Country', yaxis_title='Percentage')
        st.plotly_chart(fig_bar)

        # Choropleth map
        st.subheader(f'Geographical Distribution of People Engaged in {selected_condition}')
        fig_map = px.choropleth(filtered_df_country,
                                locations='Code',
                                color=selected_condition,
                                hover_name='Entity',
                                hover_data={'Code': False, 'Entity': True, selected_condition: ':.2f'},
                                title=f'Geographical Distribution of People Engaged in {selected_condition}',
                                color_continuous_scale='Viridis',
                                labels={selected_condition: 'Percentage'},
                                width=900, height=600)

        fig_map.update_layout(geo=dict(showcoastlines=True, projection=dict(type='natural earth')))
        # Remove coastlines and set projection to natural earth

        # Add water and land
        fig_map.update_geos(
            showocean=True, oceancolor="LightBlue", showland=True, landcolor="LightGray"
        )

        # Update map layout
        fig_map.update_layout(
            coloraxis_colorbar=dict(title='Percentage', thicknessmode='pixels', thickness=20, lenmode='pixels',
                                    len=300),  # Customize color bar
        )

        # Add hover effects
        fig_map.update_traces(hoverinfo='all', hovertemplate='%{hovertext}<br>%{z:.2f}%')

        st.plotly_chart(fig_map)
    else:
        st.write("Please select a country to display the analysis.")

# Sidebar navigation
def sidebar_navigation():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", options=[
        "Introduction",
        "Depression Prevalence",
        "Anxiety Prevalence",
        "Surveys and analysis",
        "Eating disorders"  # Corrected page name
    ])

    return page

# Main function to run the app
def main():
    page = sidebar_navigation()

    if page == "Introduction":
        page_introduction()
    elif page == "Depression Prevalence":
        page_depressive_prevalence()
    elif page == "Anxiety Prevalence":
        page_anxiety_prevalence()
    elif page == "Surveys and analysis":
        page_surveys()
    elif page == "Eating disorders":  # Corrected page name
        page_eating_disorder()


if __name__ == "__main__":
    main()