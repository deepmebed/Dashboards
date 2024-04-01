import pandas as pd
import seaborn as sns
import streamlit as st
import altair as alt
from matplotlib import pyplot as plt
from pygments.lexers import go
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import plotly.express as px
import plotly.graph_objects as go
# Load the data
# @st.cache
def load_data(file_path):
    return pd.read_csv(file_path)

file_path = "Job_Placement_Data.csv"
job = load_data(file_path)

numerical_columns = ['ssc_percentage', 'hsc_percentage', 'degree_percentage', 'mba_percent']
for col in numerical_columns:
    job[col] = pd.to_numeric(job[col], errors='coerce')

# Convert categorical variables to factors
categorical_columns = ['gender', 'ssc_board', 'hsc_board', 'hsc_subject', 'undergrad_degree', 'work_experience', 'specialisation', 'status']
for col in categorical_columns:
    job[col] = job[col].astype('category')

# Set up the title and description
st.title('Interactive Job Placement Dashboard')
st.markdown("""
This dashboard provides insights into job placement data.
""")

# Sidebar - User Input
st.sidebar.header('Analysis Options')
analysis_option = st.sidebar.selectbox('Select an Analysis', ['Data Overview', 'Histograms', 'Boxplot', 'Bar Plots', 'Summary Statistics', 'Data Filtering', 'Comparative Analysis', 'Export Data', 'Data Insights and Recommendations'])

# Main content based on user selection
if analysis_option == 'Data Overview':
    st.subheader('Data Overview')
    st.write(job)


elif analysis_option == 'Histograms':
    st.subheader('Histograms')
    selected_column = st.selectbox('Select a column for histogram:', job.columns)

    # Allow users to customize histogram parameters
    # num_bins = st.slider('Number of bins:', min_value=5, max_value=50, value=20)
    # kde_enabled = st.checkbox('Enable Kernel Density Estimation (KDE)', value=True)

    # Create histogram using Plotly Express

    # fig = px.histogram(job, x=selected_column, nbins=40)
    # fig.update_layout(title=f'Histogram of {selected_column}', xaxis_title=selected_column, yaxis_title='Count')
    # st.plotly_chart(fig)

    fig = px.histogram(job, x=selected_column, nbins=40)
    fig.update_traces(marker_color='#F0F2F6', marker_line_color='#F0F2F6', marker_line_width=1.5)
    fig.update_layout(title=f'Histogram of {selected_column}', xaxis_title=selected_column, yaxis_title='Count')
    
    st.plotly_chart(fig)




elif analysis_option == 'Boxplot':
    # st.subheader('Boxplot')
    # numerical_columns = job.select_dtypes(include=['float64', 'int64']).columns
    # selected_column = st.selectbox('Select a column for boxplot:', numerical_columns)
    # fig = sns.boxplot(data=job[selected_column])
    # st.pyplot(fig.figure)
    st.subheader('Boxplot')
    numerical_columns = job.select_dtypes(include=['float64', 'int64']).columns
    selected_column = st.selectbox('Select a column for boxplot:', numerical_columns)
    # fig = go.Figure(data=[go.Box(y=job[selected_column], name=selected_column)])
    # st.plotly_chart(fig)
    fig = go.Figure(data=[go.Box(y=job[selected_column], name=selected_column, marker_color='#F0F2F6')])
    st.plotly_chart(fig)


elif analysis_option == 'Bar Plots':
    st.subheader('Bar Plots')
    categorical_columns = ['work_experience', 'status', 'ssc_board', 'hsc_board', 'undergrad_degree', 'specialisation']
    selected_column = st.selectbox('Select a categorical column:', categorical_columns)
    if selected_column:
        if selected_column in job.columns:
            chart = alt.Chart(job).mark_bar().encode(
                x=alt.X(selected_column),
                y='count()',
                color='gender'
            ).properties(
                title=f'{selected_column} by Gender',
                width=600,
                height=400
            )
            st.altair_chart(chart)
        else:
            st.warning('Please select a valid categorical column.')

elif analysis_option == 'Summary Statistics':
    st.subheader('Summary Statistics')
    numerical_summary = job.describe()
    st.write(numerical_summary)


elif analysis_option == 'Data Filtering':
    st.subheader('Data Filtering')
    filter_criteria = st.multiselect('Select filter criteria:', categorical_columns)
    filtered_data = job.copy()
    for col in filter_criteria:
        selected_values = st.sidebar.multiselect(f'Select {col} values:', job[col].cat.categories.tolist())
        filtered_data = filtered_data[filtered_data[col].isin(selected_values)]

    # Display filtered data
    st.write(filtered_data)

    # Generate bar plots based on filtered data for selected categorical columns
    if len(filtered_data) > 0:
        st.subheader('Bar Plots (Based on Filtered Data)')
        selected_categorical_columns = st.multiselect('Select categorical columns for bar plots:', categorical_columns)
        for col in selected_categorical_columns:
            chart = px.bar(filtered_data, x=col, color='gender', barmode='group', title=f'{col} by Gender')
            st.plotly_chart(chart)
    else:
        st.warning('No data available after filtering.')



elif analysis_option == "Comparative Analysis":
    st.subheader('Comparative Analysis')
    numerical_columns = job.select_dtypes(include=['float64', 'int64']).columns
    selected_columns = st.multiselect('Select two numerical columns for comparison:', numerical_columns)
    if len(selected_columns) == 2:
        plot_type = st.radio("Select plot type:", ["Scatter Plot", "Pair Plot", "Joint Plot"])
        if plot_type == "Scatter Plot":
            st.subheader('Scatter Plot')
            fig = px.scatter(job, x=selected_columns[0], y=selected_columns[1])
            fig.update_layout(title=f'Scatter plot of {selected_columns[0]} vs {selected_columns[1]}',
                              xaxis_title=selected_columns[0], yaxis_title=selected_columns[1])
            st.plotly_chart(fig)
        elif plot_type == "Pair Plot":
            # Alternatively, you can use Plotly to create an interactive pair plot
            fig = px.scatter_matrix(job[selected_columns])
            st.plotly_chart(fig)
        elif plot_type == "Joint Plot":
            # Create a Plotly joint plot
            fig = px.scatter(job, x=selected_columns[0], y=selected_columns[1], marginal_x="histogram", marginal_y="histogram")
            st.plotly_chart(fig)


elif analysis_option == 'Machine Learning Model':
    st.subheader('Machine Learning Model')
    st.write('Predict one of the numerical columns based on selected features.')

    # Select features and target variable
    features = st.multiselect('Select features:', numerical_columns)
    target_variable = st.selectbox('Select target variable:', numerical_columns)

    if st.button('Train Model'):
        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(job[features], job[target_variable], test_size=0.2,
                                                            random_state=42)

        # Train linear regression model
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Make predictions
        y_pred = model.predict(X_test)

        # Display evaluation metrics
        st.write('Evaluation Metrics:')
        st.write(f'R-squared: {model.score(X_test, y_test):.2f}')

        # Display feature importance
        if len(features) > 1:
            feature_importance = pd.Series(model.coef_, index=features).sort_values(ascending=False)
            st.write('Feature Importance:')
            st.write(feature_importance)

        # Allow users to input values for prediction
        prediction_input = {}
        for feature in features:
            prediction_input[feature] = st.number_input(f'Enter {feature}:')
        if st.button('Predict'):
            input_data = pd.DataFrame(prediction_input, index=[0])
            prediction = model.predict(input_data)
            st.write(f'Predicted {target_variable}: {prediction[0]}')

elif analysis_option == 'Export Data':
    st.subheader('Export Data')
    export_format = st.radio('Select export format:', ['CSV', 'Excel'])
    if st.button('Export Data'):
        if export_format == 'CSV':
            job.to_csv('exported_data.csv', index=False)
            st.success('Data exported to CSV file.')
        elif export_format == 'Excel':
            job.to_excel('exported_data.xlsx', index=False)
            st.success('Data exported to Excel file.')



elif analysis_option == 'Data Insights and Recommendations':
    st.subheader('Data Insights and Recommendations')

    if st.checkbox('Show Insights'):
        st.write("""
        Provide some insights based on the selected analysis option.
        For example:
        - If 'Histograms' was selected, you can provide insights about the distribution of data.
        - If 'Summary Statistics' was selected, you can summarize the key statistics of the dataset.
        - If 'Comparative Analysis' was selected, you can compare different variables and highlight any correlations.
        """)

    if st.checkbox('Show Recommendations'):
        st.write("""
        Offer recommendations based on the insights provided above.
        For example:
        - Recommend focusing on areas with high frequency in the histograms for improvement.
        - Suggest exploring relationships between variables further to uncover insights.
        - Provide suggestions for potential machine learning models based on the dataset characteristics.
        """)


else:
    st.warning('Please select an analysis option.')
