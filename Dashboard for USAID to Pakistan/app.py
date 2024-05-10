import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
file_path = 'USAID.csv'
data_cleaned = pd.read_csv(file_path)

# Data Cleaning Function without outlier handling
def clean_data(df):
    for column in df.columns:
        if df[column].dtype == 'float64':
            df[column] = pd.to_numeric(df[column], errors='coerce')

    df.drop_duplicates(inplace=True)

    for column in df.columns:
        if df[column].dtype == 'object':
            df[column] = df[column].fillna(df[column].mode().iloc[0]) 

    return df

# Clean the data
data_cleaned = clean_data(data_cleaned)

# Set page configuration
st.set_page_config(
    page_title="USAID 2001-23 Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main title
st.title('USAID Dashboard')

# Data Management and User Input Handling
st.sidebar.subheader('Data Management and User Input')
year_option = data_cleaned['Fiscal Year'].unique().tolist()
selected_year = st.sidebar.selectbox("Which year should we plot?", year_option, 0, key="select-year")

# Filter data based on user input
df_selected_year = data_cleaned[data_cleaned['Fiscal Year'] == selected_year]

# Clean the 'Constant Dollar Amount' column
df_selected_year['Constant Dollar Amount'] = pd.to_numeric(df_selected_year['Constant Dollar Amount'], errors='coerce')
df_selected_year = df_selected_year.dropna(subset=['Constant Dollar Amount'])
df_selected_year['Constant Dollar Amount'] = df_selected_year['Constant Dollar Amount'].apply(lambda x: max(0, x))

# Create columns layout
col1, col2, col3, col4, col5 = st.columns(5)

# Function to plot selected chart
def plot_chart(chart_type, data):
    if chart_type == "Total Aid Disbursement Over Fiscal Years":
        aid_over_time_chart = px.line(data, x='Fiscal Year', y='Current Dollar Amount',
                                      labels={'Current Dollar Amount': 'Amount (in billions)'},
                                      title='Total Aid Disbursement Over Fiscal Years',
                                      color_discrete_sequence=['#FF5733'])  # Specify the color you want
        st.plotly_chart(aid_over_time_chart)

    elif chart_type == "Top 10 Managing Agencies by Aid Amount":
        def get_top_agencies(selected_year):
            df_selected_year = data[data['Fiscal Year'] == selected_year]
            aid_by_agency = df_selected_year.groupby('Managing Agency Acronym')['Current Dollar Amount'].sum().reset_index()
            top_agencies = aid_by_agency.nlargest(10, 'Current Dollar Amount')
            return px.bar(top_agencies, x='Managing Agency Acronym', y='Current Dollar Amount',
                          color='Managing Agency Acronym',
                          labels={'Current Dollar Amount': 'Amount (in billions)'},
                          title='Top 10 Managing Agencies by Aid Amount')

        # Call the function and display the chart
        top_agencies_chart = get_top_agencies(selected_year)
        st.plotly_chart(top_agencies_chart)

    elif chart_type == "Aid Distribution by Category, Including Military Assistance":
        def get_aid_by_category(selected_year):
            df_selected_year = data[data['Fiscal Year'] == selected_year]
            aid_by_category = df_selected_year.groupby('US Category Name')['Current Dollar Amount'].sum().reset_index()
            aid_by_category_sorted = aid_by_category.nlargest(10, 'Current Dollar Amount')
            return px.bar(aid_by_category_sorted, x='US Category Name', y='Current Dollar Amount',
                          color='US Category Name',
                          labels={'Current Dollar Amount': 'Amount (in billions)'},
                          title='Aid Distribution by Category, Including Military Assistance')

        # Call the function and display the chart
        aid_by_category_chart = get_aid_by_category(selected_year)
        st.plotly_chart(aid_by_category_chart)

    elif chart_type == "Display Aid Distribution in the Selected Year":
        fig_selected_year = px.scatter(data, x='Fiscal Year', y='Constant Dollar Amount',
                                       size='Constant Dollar Amount', color='Region Name', hover_name='Country Name',
                                       labels={'Constant Dollar Amount': 'Amount (in billions)'},
                                       title=f'Aid Distribution in {selected_year}')
        st.plotly_chart(fig_selected_year)

    elif chart_type == "Aid Distribution: Military Assistance vs Other Sectors":
        military_assistance_total = data[data['US Category Name'] == 'Military Assistance']['Current Dollar Amount'].sum()
        total_other_categories_total = data[data['US Category Name'] != 'Military Assistance']['Current Dollar Amount'].sum()

        comparison_data = pd.DataFrame({
            'Category': ['Military Assistance', 'Other Sectors'],
            'Total Aid Amount': [military_assistance_total, total_other_categories_total]
        })

        bar_chart = px.bar(comparison_data, x='Category', y='Total Aid Amount', text='Total Aid Amount',
                           labels={'Total Aid Amount': 'Amount (in billions)'},
                           title='Total Aid Distribution: Military Assistance vs Other Sectors',
                           color='Category')  # Ensuring Military Assistance is displayed with a different color
        st.plotly_chart(bar_chart)

# Radio button for selecting chart type
chart_type = st.sidebar.radio("Select Chart Type",
                               ["Total Aid Disbursement Over Fiscal Years",
                                "Top 10 Managing Agencies by Aid Amount",
                                "Aid Distribution by Category, Including Military Assistance",
                                "Display Aid Distribution in the Selected Year",
                                "Aid Distribution: Military Assistance vs Other Sectors"])

# Display selected chart
plot_chart(chart_type, df_selected_year)

# Dashboard Summary
st.title('Dashboard Summary')

# Data Preview
st.subheader('Data Preview:')
st.write(data_cleaned.head())

# Summary Statistics
st.subheader('Summary Statistics:')
summary_statistics = data_cleaned.describe().transpose()
st.write(summary_statistics)

# Column Comparison
st.sidebar.subheader('Column Comparison')
column_options = data_cleaned.select_dtypes(include=['float64']).columns.tolist()
selected_columns1 = st.sidebar.multiselect("Select first set of columns to compare:", column_options, default=column_options[:2])
selected_columns2 = st.sidebar.multiselect("Select second set of columns to compare:", column_options, default=column_options[2:4])

if selected_columns1 and selected_columns2:
    comparison_data1 = data_cleaned[selected_columns1]
    comparison_data2 = data_cleaned[selected_columns2]
    
    st.write("### Comparison of Selected Columns (Set 1)")
    st.write(comparison_data1.head())

    st.write("### Comparison of Selected Columns (Set 2)")
    st.write(comparison_data2.head())

    for col1 in selected_columns1:
        for col2 in selected_columns2:
            col1, col2 = st.columns(2)
            scatter_plot = px.scatter(data_cleaned, x=col1, y=col2, title=f"{col1} vs {col2}")
            col1.plotly_chart(scatter_plot)






