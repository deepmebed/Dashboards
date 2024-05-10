import streamlit as st
import pandas as pd
import plotly.express as px
# Load a sample dataset (replace this with your dataset)
df = pd.read_csv("Country-data.csv")
st.set_page_config(page_title="Fund Allocation Dashboard", page_icon="🌐", layout="wide")




def info_page():
    st.title("Project Information")
    st.write("""
       Welcome to the Fund Allocation Dashboard! This dashboard provides insights into various economic, health, and social indicators of different countries.

       **Features:**
       - Choose economic indicators, health indicators, social indicators, or trade and economic structure for analysis.
       - Select countries, metrics, and year range to customize your view.
       - Explore charts, summary statistics, data tables, and more.""")
    st.write("""
    **Feature Description** 

* country:      Name of the country

* child_mort:   Death of children under 5 years of age per 1000 live births

* exports:      Exports of goods and services per capita. Given as %age of the GDP per capita

* health:       Total health spending per capita. Given as %age of GDP per capita

* imports:      Imports of goods and services per capita. Given as %age of the GDP per capita

* Income:       Net income per person

* life_expec:   The average number of years a new born child would live if the current mortality patterns are to remain the same

* total_fer:    The number of children that would be born to each woman if the current age-fertility rates remain the same

* gdpp:         The GDP per capita. Calculated as the Total GDP divided by the total population""")


def economic_indicator_page(df=df, x="income", y="gdpp"):
    global countries_to_display
    st.title("""Economic Indicators:
Income (per capita): Evaluate the average income per person. A low income level indicates potential poverty.

GDP per capita (gdpp): Assess the country's economic output per person. A lower GDP per capita may indicate economic challenges.""")

    # st.write("""   Countries with higher GDP per capita tend to have lower fertility rates as economic development is often associated with increased access to education, healthcare, and family planning.""")
    # st.image("economic.jpeg")
    economic_status_choice = st.radio("Select Economic Status:", ['Top 10 Rich', 'Top 10 Poor'])

    num_countries = st.slider("Enter the number of countries:", min_value=1, max_value=len(df), value=10, step=1)
    if "Rich" in economic_status_choice:
        countries_to_display = df.nlargest(num_countries, columns=[x])['country'].unique()
    elif "Poor" in economic_status_choice:
        countries_to_display = df.nsmallest(num_countries, columns=[x])['country'].unique()

    st.markdown(f"**Economic Status:** {economic_status_choice}")

    selected_countries = st.multiselect("Select Countries:", countries_to_display, default=countries_to_display)
    selected_metrics = st.multiselect("Select Metrics:", df.columns, default=[x, y])

    if st.sidebar.button("Reset Filters"):
        st.experimental_rerun()

    country_info = df[df['country'].isin(selected_countries)]

    # Radio buttons to choose one chart type
    chart_type = st.selectbox("Select Chart Type:", ["Line Chart", "Scatter Plot", "Bar Chart", "Pie Chart"])

    with st.container():
        if chart_type == "Line Chart":
            st.subheader(f"Line Chart: {x} and {y}")
            line_selected_chart = px.line(country_info[country_info['country'].isin(selected_countries)],
                                          x=country_info.index, y=selected_metrics,
                                          title=f"{x} and {y} Over Time (Selected Countries)")
            st.plotly_chart(line_selected_chart)

        elif chart_type == "Scatter Plot":
            st.subheader(f"Scatter Plot: {x} and {y}")
            scatter_selected_chart = px.scatter(country_info[country_info['country'].isin(selected_countries)], x=x,
                                                y=y,
                                                title=f"Scatter Plot: {x} vs. {y} (Selected Countries)")
            st.plotly_chart(scatter_selected_chart)

        elif chart_type == "Bar Chart":
            st.subheader(f"Grouped Bar Chart: {x} and {y}")
            grouped_bar_chart = px.bar(country_info[country_info['country'].isin(selected_countries)], x='country',
                                       y=[x, y],
                                       title=f"{x} and {y} for Selected Countries",
                                       color_discrete_map={'country': 'green'},
                                       barmode='group')
            st.plotly_chart(grouped_bar_chart)

        elif chart_type == "Pie Chart":
            for metric in selected_metrics:
                st.subheader(f"Pie Chart: {metric}")
                pie_chart = px.pie(df[df['country'].isin(selected_countries)], names='country', values=metric,
                                   title=f"Distribution of {metric} for Selected Countries")
                st.plotly_chart(pie_chart)



    # st.subheader(f"Details for Selected Countries")
    # st.write(country_info)
    #
    # st.subheader("Summary Statistics")
    # st.write(country_info[selected_metrics].describe())


def health_indicator_page(df=df, x ="child_mort",y =  "life_expec"):
    st.title("""Health Indicators:

Child Mortality: High child mortality rates often correlate with poor healthcare, sanitation, and living conditions.
Life Expectancy: A lower life expectancy may suggest challenges in healthcare and overall well-being.""")

    economic_status_choice = st.radio("Select Economic Status:", ['Top 10 Rich', 'Top 10 Poor'])

    num_countries = st.slider("Enter the number of countries:", min_value=1, max_value=len(df), value=10, step=1)
    if "Rich" in economic_status_choice:
        countries_to_display = df.nsmallest(num_countries, columns=[x])['country'].unique()
    elif "Poor" in economic_status_choice:
        countries_to_display = df.nlargest(num_countries, columns=[x])['country'].unique()

    st.markdown(f"**Economic Status:** {economic_status_choice}")

    selected_countries = st.multiselect("Select Countries:", countries_to_display, default=countries_to_display)
    selected_metrics = st.multiselect("Select Metrics:", df.columns, default=[x, y])

    if st.sidebar.button("Reset Filters"):
        st.experimental_rerun()

    country_info = df[df['country'].isin(selected_countries)]

    # Radio buttons to choose one chart type
    chart_type = st.selectbox("Select Chart Type:", ["Line Chart", "Bar Chart", "Pie Chart"])

    with st.container():
        if chart_type == "Line Chart":
            st.subheader(f"Line Chart: {x} and {y}")
            line_selected_chart = px.line(country_info[country_info['country'].isin(selected_countries)],
                                          x=country_info.index, y=selected_metrics,
                                          title=f"{x} and {y} Over Time (Selected Countries)")
            st.plotly_chart(line_selected_chart)



        elif chart_type == "Bar Chart":
            st.subheader(f"Grouped Bar Chart: {x} and {y}")
            grouped_bar_chart = px.bar(country_info[country_info['country'].isin(selected_countries)], x='country',
                                       y=[x, y],
                                       title=f"{x} and {y} for Selected Countries",
                                       color_discrete_map={'country': 'green'},
                                       barmode='group')
            st.plotly_chart(grouped_bar_chart)

        elif chart_type == "Pie Chart":
            for metric in selected_metrics:
                st.subheader(f"Pie Chart: {metric}")
                pie_chart = px.pie(df[df['country'].isin(selected_countries)], names='country', values=metric,
                                   title=f"Distribution of {metric} for Selected Countries")
                st.plotly_chart(pie_chart)



    # st.subheader(f"Details for Selected Countries")
    # st.write(country_info)
    #
    #
    # st.subheader("Summary Statistics")
    # st.write(country_info[selected_metrics].describe())


def inflation(df = df,x="inflation"):

    economic_status_choice = st.radio("Select Economic Status:", ['Top 10 Rich', 'Top 10 Poor'])

    num_countries = st.slider("Enter the number of countries:", min_value=1, max_value=len(df), value=10, step=1)
    if "Rich" in economic_status_choice:
        countries_to_display = df.nsmallest(num_countries, columns=[x])['country'].unique()
    elif "Poor" in economic_status_choice:
        countries_to_display = df.nlargest(num_countries, columns=[x])['country'].unique()

    st.markdown(f"**Economic Status:** {economic_status_choice}")

    selected_countries = st.multiselect("Select Countries:", countries_to_display, default=countries_to_display)
    selected_metrics = st.multiselect("Select Metrics:", df.columns, default=[x])

    if st.sidebar.button("Reset Filters"):
        st.experimental_rerun()

    country_info = df[df['country'].isin(selected_countries)]

    # Radio buttons to choose one chart type
    chart_type = st.selectbox("Select Chart Type:", ["Bar Chart", "Pie Chart"])

    with st.container():
        # if chart_type == "Line Chart":
        #     st.subheader(f"Line Chart: {x}")
        #     line_selected_chart = px.line(country_info[country_info['country'].isin(selected_countries)],
        #                                   x=country_info.index, y=selected_metrics,
        #                                   title=f"{x}  Over Time (Selected Countries)")
        #     st.plotly_chart(line_selected_chart)

        if chart_type == "Bar Chart":
            st.subheader(f"Grouped Bar Chart for: {x}")
            grouped_bar_chart = px.bar(country_info[country_info['country'].isin(selected_countries)], x='country',
                                       y=[x],
                                       title=f"{x}  for Selected Countries",
                                       color_discrete_map={'country': 'green'},
                                       barmode='group')
            st.plotly_chart(grouped_bar_chart)
        elif chart_type == "Pie Chart":
            for metric in selected_metrics:
                st.subheader(f"Pie Chart: {metric}")
                pie_chart = px.pie(df[df['country'].isin(selected_countries)], names='country', values=metric,
                                   title=f"Distribution of {metric} for Selected Countries")
                st.plotly_chart(pie_chart)



    # st.subheader(f"Details for Selected Countries")
    # st.write(country_info)
    #
    # st.subheader("Summary Statistics")
    # st.write(country_info[selected_metrics].describe())


def trade_economic_structure_page(df=df,x= "imports",y= "exports"):
    global countries_to_display
    economic_status_choice = st.radio("Select Economic Status:", ['Top 10 Rich', 'Top 10 Poor'])

    num_countries = st.slider("Enter the number of countries:", min_value=1, max_value=len(df), value=10, step=1)
    if "Rich" in economic_status_choice:
        # Select countries with highest values of x and y
        countries_to_display_x = df.nlargest(num_countries, columns=[x])['country'].unique()
        countries_to_display_y = df.nlargest(num_countries, columns=[y])['country'].unique()
        # Find the intersection of countries with highest values of both x and y
        countries_to_display = set(countries_to_display_x).union(countries_to_display_y)
    elif "Poor" in economic_status_choice:
        # Select countries with lowest values of x and y
        countries_to_display_x = df.nsmallest(num_countries, columns=[x])['country'].unique()
        countries_to_display_y = df.nsmallest(num_countries, columns=[y])['country'].unique()
        # Find the intersection of countries with lowest values of both x and y
        countries_to_display = set(countries_to_display_x).union(countries_to_display_y)

    st.markdown(f"**Economic Status:** {economic_status_choice}")

    selected_countries = st.multiselect("Select Countries:", countries_to_display, default=countries_to_display)
    selected_metrics = st.multiselect("Select Metrics:", df.columns, default=[x, y])

    if st.sidebar.button("Reset Filters"):
        st.experimental_rerun()

    country_info = df[df['country'].isin(selected_countries)]

    # Radio buttons to choose one chart type
    chart_type = st.selectbox("Select Chart Type:", ["Line Chart", "Scatter Plot", "Bar Chart", "Pie Chart"])

    with st.container():
        if chart_type == "Line Chart":
            st.subheader(f"Line Chart: {x} and {y}")
            line_selected_chart = px.line(country_info[country_info['country'].isin(selected_countries)],
                                          x=country_info.index, y=selected_metrics,
                                          title=f"{x} and {y} of (Selected Countries)")
            st.plotly_chart(line_selected_chart)

        elif chart_type == "Scatter Plot":
            st.subheader(f"Scatter Plot: {x} and {y}")
            scatter_selected_chart = px.scatter(country_info[country_info['country'].isin(selected_countries)], x=x,
                                                y=y,
                                                title=f"Scatter Plot: {x} vs. {y} (Selected Countries)")
            st.plotly_chart(scatter_selected_chart)

        elif chart_type == "Bar Chart":
            st.subheader(f"Grouped Bar Chart: {x} and {y}")
            grouped_bar_chart = px.bar(country_info[country_info['country'].isin(selected_countries)], x='country',
                                       y=[x, y],
                                       title=f"{x} and {y} for Selected Countries",
                                       color_discrete_map={'country': 'green'},
                                       barmode='group')
            st.plotly_chart(grouped_bar_chart)

        elif chart_type == "Pie Chart":
            for metric in selected_metrics:
                st.subheader(f"Pie Chart: {metric}")
                pie_chart = px.pie(df[df['country'].isin(selected_countries)], names='country', values=metric,
                                   title=f"Distribution of {metric} for Selected Countries")
                st.plotly_chart(pie_chart)

        # elif chart_type == "Heatmap":
        #     st.subheader("Heatmap for All Data")
        #     heatmap = px.imshow(df[df['country'].isin(selected_countries)][selected_metrics].corr(),
        #                         labels=dict(color="Correlation"),
        #                         x=selected_metrics, y=selected_metrics, color_continuous_scale='viridis')
        #     st.plotly_chart(heatmap)
    #
    # st.subheader(f"Details for Selected Countries")
    # st.write(country_info)
    #
    # st.subheader("Summary Statistics")
    # st.write(country_info[selected_metrics].describe())


def map_page():
    st.subheader("Map: High GDPP and Low Child Mortality")
    high_gdpp_low_mort_chart = px.scatter_geo(df[df['gdpp'] > df['gdpp'].mean()],  # Selecting countries with high GDPP
                                              locations="country",
                                              locationmode="country names",
                                              size="gdpp",
                                              color="child_mort",
                                              hover_name="country",
                                              title="High GDPP and Low Child Mortality",
                                              projection="natural earth",
                                              labels={'gdpp': 'GDP per Capita', 'child_mort': 'Child Mortality'},
                                              color_continuous_scale='viridis',  # Change to your preferred color scale
                                              )
    st.plotly_chart(high_gdpp_low_mort_chart)

    # Map with labels for low GDPP and high child mortality
    st.subheader("Map: Low GDPP and High Child Mortality")
    low_gdpp_high_mort_chart = px.scatter_geo(df[df['gdpp'] <= df['gdpp'].mean()],  # Selecting countries with low GDPP
                                              locations="country",
                                              locationmode="country names",
                                              size="gdpp",
                                              color="child_mort",
                                              hover_name="country",
                                              title="Low GDPP and High Child Mortality",
                                              projection="natural earth",
                                              labels={'gdpp': 'GDP per Capita', 'child_mort': 'Child Mortality'},
                                              color_continuous_scale='plasma',  # Change to your preferred color scale
                                              )
    st.plotly_chart(low_gdpp_high_mort_chart)


# Main Page

page = st.sidebar.radio("Select a Page", ("Information","Economic Indicator", "Health Indicator", "Inflation",
                                          "Trade and Economic Structure", "Maps"))
if page == "Information":
    info_page()
elif page == "Economic Indicator":
    economic_indicator_page()
elif page == "Health Indicator":
    health_indicator_page()
elif page == "Inflation":
    inflation()
elif page == "Trade and Economic Structure":
    trade_economic_structure_page()
elif page == "Maps":
    map_page()
