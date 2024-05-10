import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

# Load the dataset
@st.cache_data()
def load_data(filename):
    df = pd.read_csv(filename)
    return df.copy()  # Make a copy of the dataframe to prevent mutation

filename = "GenderBasedEmploymentInPakistan2023.csv"
df = load_data(filename)

# Clean the data: Convert non-numeric values to NaN and then convert the columns to float
numeric_cols = ['Total', 'Male', 'Female']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Drop rows with NaN values in numeric columns
df.dropna(subset=numeric_cols, inplace=True)

# Sidebar for filtering options
st.sidebar.title('Filter Options')
selected_province = st.sidebar.selectbox('Select Province', [None] + list(df['Province'].unique()))
if selected_province:
    districts_in_province = df[df['Province'] == selected_province]['District'].unique()
    selected_district = st.sidebar.selectbox('Select District', [None] + list(districts_in_province))
else:
    selected_district = None
    
selected_indicator = st.sidebar.selectbox('Select Job Title', [None] + list(df['Indicator'].unique()))
selected_employment_graph = st.sidebar.selectbox('Select Employment Graph', [None, 'Total Employment by Division', 'Male vs Female Employment', 'Trend Analysis by Region'])
if (selected_employment_graph != 'Male vs Female Employment') & (selected_employment_graph != 'Total Employment by Division'):
    selected_plot_type = st.sidebar.selectbox('Select Plot Type', [None, 'Bar Plot','Pie Chart'])
    
# Filter the data based on user selection
if selected_province:
    filtered_data = df[df['Province'] == selected_province]
    if selected_district:
        filtered_data = filtered_data[filtered_data['District'] == selected_district]
    if selected_indicator:
        filtered_data = filtered_data[filtered_data['Indicator'] == selected_indicator]

# Display the dataset and filter options
st.title("Gender-Based Employment Analysis in Pakistan (2023)")
st.write("""
    Welcome to the Gender-Based Employment Analysis Dashboard for Pakistan (2023). 
    Explore the dynamics of employment across different provinces, divisions, and districts, 
    dissecting the job title with a focus on gender. Delve into the data to uncover insights 
    into the distribution of employment between males and females in various areas. 
    Gain a comprehensive understanding of the employment landscape and disparities, 
    empowering informed decision-making and policy formulation. Let the data guide you 
    through the intricacies of gender-based employment in Pakistan.
""")

# Display filtered data if selected
if selected_province:
    st.write('## Employment Data')
    st.write(filtered_data)

    # Display selected employment graph
    if selected_employment_graph == 'Total Employment by Division':
        selected_plot_type = st.sidebar.selectbox('Select Plot Type', [None,'Bar Plot'])
        st.write('## Total Employment by Division')
        if selected_plot_type == 'Bar Plot':
            
            fig_trend_selected = px.bar(filtered_data, x='Division', y='Total', color='Area Type', barmode='group', title=f"Total Employent by Division in {selected_province}")
            st.plotly_chart(fig_trend_selected, use_container_width=True)

            colors = ['blue', 'orange']

# Create a stacked bar chart
            fig = go.Figure(data=[
            go.Bar(name='Male', x=filtered_data['Division'], y=filtered_data['Male'], marker_color=colors[0]),
            go.Bar(name='Female', x=filtered_data['Division'], y=filtered_data['Female'], marker_color=colors[1])
            ]) 

# Update layout
            fig.update_layout(barmode='stack', xaxis_title='Province', yaxis_title='Number of Employees')

# Plot the chart
            st.plotly_chart(fig, use_container_width=True)
           

    elif selected_employment_graph == 'Trend Analysis by Region':
        st.write('## Trend Analysis by Region')
        if selected_province and selected_indicator:
            st.write(f"### Trend Analysis for {selected_indicator}")
            if selected_plot_type:
                if selected_province:
                    st.write(f"#### Selected Province: {selected_province}")
                    filtered_data_selected = df[(df['Indicator'] == selected_indicator) & (df['Province'] == selected_province)]
                    if not filtered_data_selected.empty:
                        if selected_plot_type == 'Bar Plot':
                            fig_trend_selected = px.bar(filtered_data_selected, x='Division', y='Total', color='Division', barmode='group', title=f"Trend Analysis for {selected_indicator} in {selected_province}")
                            st.plotly_chart(fig_trend_selected, use_container_width=True)
                        elif selected_plot_type == 'Pie Chart':
                            fig_trend_selected = px.pie(filtered_data_selected, names='Division', values='Total', color='Division', title=f"Trend Analysis for {selected_indicator} in {selected_province}")
                            st.plotly_chart(fig_trend_selected, use_container_width=True)
                        elif selected_plot_type == 'Scatter Plot':
                            fig_trend_selected = px.scatter(filtered_data_selected, x='Division', y='Total', color='Division', title=f"Trend Analysis for {selected_indicator} in {selected_province}")
                            st.plotly_chart(fig_trend_selected, use_container_width=True)
                        else:
                                st.write("No data available for the selected province.")
                    st.write('#### Compare with Other Provinces:')
                #    selected_region = st.text_input('Enter Province Name:')
                #     if st.button('Search'):
                #         if selected_region:
                #             filtered_data = df[(df['Indicator'] == selected_indicator) & (df['Province'] == selected_region)]
                            
                #             if not filtered_data.empty:
                #                 if selected_plot_type == 'Bar Plot':
                #                     fig_trend_selected = px.bar(filtered_data, x='Division', y='Total', color='Division', barmode='group', title=f"Trend Analysis for {selected_indicator} in {selected_region}")
                #                     st.plotly_chart(fig_trend_selected, use_container_width=True)
                #                 elif selected_plot_type == 'Line Plot':
                #                     fig_trend_selected = px.line(filtered_data_selected, x='Division', y='Total', color='Division', title=f"Trend Analysis for {selected_indicator} in {selected_region}")
                #                     st.plotly_chart(fig_trend_selected, use_container_width=True)
                #                 elif selected_plot_type == 'Pie Chart':
                #                     fig_trend_selected = px.pie(filtered_data, names='Division', values='Total', color='Division', title=f"Trend Analysis for {selected_indicator} in {selected_region}")
                #                     st.plotly_chart(fig_trend_selected, use_container_width=True)
                #                 elif selected_plot_type == 'Scatter Plot':
                #                     fig_trend_selected = px.scatter(filtered_data_selected, x='Division', y='Total', color='Division', title=f"Trend Analysis for {selected_indicator} in {selected_region}")
                #                     st.plotly_chart(fig_trend_selected, use_container_width=True)
                #                 else:
                #                     st.write("No data available for the selected province.")
                #             else:
                #                 st.write("Please enter a province name.")
                # else:
                #     st.write("Please select a province.")
                    selected_provinces = st.multiselect('Select Provinces', [x for x in df['Province'].unique() if x != selected_province], default=[])
                    for province in selected_provinces:
                        filtered_data_selected = df[(df['Indicator'] == selected_indicator) & (df['Province'] == province)]
                        if not filtered_data_selected.empty:
                            if selected_plot_type == 'Bar Plot':
                                fig_trend_selected = px.bar(filtered_data_selected, x='Division', y='Total', color='Division', barmode='group', title=f"Trend Analysis for {selected_indicator} in {province}")
                                st.plotly_chart(fig_trend_selected, use_container_width=True)
                            elif selected_plot_type == 'Line Plot':
                                fig_trend_selected = px.line(filtered_data_selected, x='Division', y='Total', color='Division', title=f"Trend Analysis for {selected_indicator} in {province}")
                                st.plotly_chart(fig_trend_selected, use_container_width=True)
                            elif selected_plot_type == 'Pie Chart':
                                fig_trend_selected = px.pie(filtered_data_selected, names='Division', values='Total', color='Division', title=f"Trend Analysis for {selected_indicator} in {province}")
                                st.plotly_chart(fig_trend_selected, use_container_width=True)
                            elif selected_plot_type == 'Scatter Plot':
                                fig_trend_selected = px.scatter(filtered_data_selected, x='Division', y='Total', color='Division', title=f"Trend Analysis for {selected_indicator} in {province}")
                                st.plotly_chart(fig_trend_selected, use_container_width=True)
                            else:
                                st.write("No data available for the selected province.")
                else:
                    st.write("Please select a province.")
            else:
                st.write("Please select a plot type.")
        else:
            st.write("Please select both province and an indicator for trend analysis.")
            
    elif selected_employment_graph == 'Male vs Female Employment':
        st.write('## Male vs Female Employment')
        selected_plot_type = st.sidebar.selectbox('Select Plot Type', [None,'Bar Plot'])
        filtered_data = filtered_data[['Division', 'Male', 'Female', 'Total', 'Area Type']][(filtered_data['Area Type'] == 'Urban') | (filtered_data['Area Type'] == 'Rural')]
        if selected_plot_type == 'Bar Plot':
            filtered_data = filtered_data[(filtered_data['Area Type'] == 'Urban') | (filtered_data['Area Type'] == 'Rural')]
            fig = px.bar(filtered_data, x='Area Type', y=['Male', 'Female'],
            title=f"Male vs Female employment by in Urabn and Rural areas of {selected_province}",
            barmode='group')
            st.plotly_chart(fig, use_container_width=True)

            
if st.sidebar.button("Provide Feedback"):
            feedback = st.sidebar.text_area("Share your feedback:", height=100)
            if st.sidebar.button("Submit"):
            # Code to submit feedback (e.g., store it in a database)
                st.success("Thank you for your feedback!")

        
      


    
            
