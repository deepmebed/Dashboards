import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("PakistanSurgerySpecialist.csv")
    return df

# Dashboard title and data loading
st.title("Pakistan Surgery Specialist Insights")
df = load_data()

# Sidebar with options
option = st.sidebar.selectbox(
    'Choose an option:',
    ('Data Overview', 'Average Satisfaction Histogram', 'Surgeries by Type', 'Distribution of Ratings', 'Surgeries Distribution')
)

# Display selected option
if option == 'Data Overview':
    st.header("Data Overview")
    #st.write(df)

    unique_values = {}
    for column in ['Medical Intervention', 'SURGERY TYPE', 'Name', 'AVAILABLE DOCTORS', 'QUALIFICATIONS', 'RATINGS', 'SATISFACTION']:
        unique_values[column] = df[column].nunique()

    # Create a DataFrame from unique values
    unique_values_df = pd.DataFrame.from_dict(unique_values, orient='index', columns=['Count'])

    # Plot pie chart
    fig = px.pie(unique_values_df, values='Count', names=unique_values_df.index, title='Distribution of Unique Values in Dataset')
    st.plotly_chart(fig)

elif option == 'Average Satisfaction Histogram'.strip():
    df['SATISFACTION'] = df['SATISFACTION'].str.replace('-', '0').str.rstrip('%').astype(int)

    # Plot histogram
    avg_satisfaction = df.groupby('SURGERY TYPE')['SATISFACTION'].mean().reset_index()

    # Normalize the average satisfaction levels between 0 and 100%
    avg_satisfaction['SATISFACTION'] = (avg_satisfaction['SATISFACTION'] / 100) * 100

    # Streamlit App
    st.title('Average Satisfaction Level by Surgery Type')

    # Plot histogram
    fig = px.bar(avg_satisfaction, x='SURGERY TYPE', y='SATISFACTION',
             title='Average Satisfaction Level by Surgery Type',
             labels={'SURGERY TYPE': 'Surgery Type', 'SATISFACTION': 'Average Satisfaction (%)'})
    st.plotly_chart(fig, use_container_width=True)
    
elif option == 'Surgeries by Type':
    st.header("Surgeries by Type")
    surgery_count = df['SURGERY TYPE'].value_counts()
    fig = px.bar(x=surgery_count.index, y=surgery_count.values, labels={'x': 'Surgery Type', 'y': 'Count'})
    st.plotly_chart(fig)
elif option == 'Distribution of Ratings':
    st.header("Distribution of Ratings")
    ratings_distribution = df['RATINGS'].value_counts()
    fig = px.bar(x=ratings_distribution.index, y=ratings_distribution.values, labels={'x': 'Ratings', 'y': 'Count'})
    st.plotly_chart(fig)

elif option == 'Surgeries Distribution':
    st.header("Surgeries Distribution")
    visualization_option = st.radio("Select Visualization:", ("Bar Chart", "Pie Chart"))
    
    surgery_count = df['SURGERY TYPE'].value_counts().reset_index()
    surgery_count.columns = ['SURGERY TYPE', 'Count']
    
    if visualization_option == "Bar Chart":
        st.subheader("Distribution of Surgical Types (Bar Chart)")
        fig = px.bar(surgery_count, x='SURGERY TYPE', y='Count', labels={'SURGERY TYPE': 'Surgery Type', 'Count': 'Number of Surgeries'})
        st.plotly_chart(fig)
        
        compare_doctors = st.checkbox("Compare with Available Doctors")
        if compare_doctors:
            st.subheader("Comparison with Available Doctors")
            availability = df.groupby('SURGERY TYPE')['AVAILABLE DOCTORS'].sum().reset_index()
            fig_availability = px.bar(availability, x='SURGERY TYPE', y='AVAILABLE DOCTORS', labels={'AVAILABLE DOCTORS': 'Available Doctors'})
            st.plotly_chart(fig_availability)
    
    elif visualization_option == "Pie Chart":
        st.subheader("Distribution of Surgical Types (Pie Chart)")
        fig = px.pie(surgery_count, values='Count', names='SURGERY TYPE', title='Surgical Types Distribution')
        st.plotly_chart(fig)

# More Insights
more_insights_button = st.checkbox('More Insights')
if more_insights_button:
    st.sidebar.title("Filters")
    selected_surgery_type = st.sidebar.selectbox("Select Surgery Type", ["All"] + list(df['SURGERY TYPE'].unique()))
    selected_qualification = st.sidebar.selectbox("Select Qualification", ["All"] + list(df['QUALIFICATIONS'].unique()))

    search_term = st.sidebar.text_input("Search by Doctor's Name")

    
    filtered_data = df.copy()
    if selected_surgery_type != "All":
        filtered_data = filtered_data[filtered_data['SURGERY TYPE'] == selected_surgery_type]
    if selected_qualification != "All":
        filtered_data = filtered_data[filtered_data['QUALIFICATIONS'] == selected_qualification]
    if search_term.strip():
        filtered_data = filtered_data[filtered_data['Name'].str.contains(search_term, case=False)]

    # Main 
    st.title("Surgical Specialists in Pakistan")

    
    st.write(f"Total Specialists: {len(filtered_data)}")

    
    if st.checkbox("Show Ratings and Satisfaction Scores"):
        ratings_min = st.slider("Minimum Rating", min_value=0, max_value=4592, value=0)
        

        filtered_data['RATINGS'] = filtered_data['RATINGS'].astype(str)
        filtered_data['SATISFACTION'] = filtered_data['SATISFACTION'].astype(str)

        filtered_data['RATINGS'] = pd.to_numeric(filtered_data['RATINGS'].str.replace(',', ''), errors='coerce')
        filtered_data['SATISFACTION'] = pd.to_numeric(filtered_data['SATISFACTION'].str.rstrip('%'), errors='coerce')


        filtered_data = filtered_data[(filtered_data['RATINGS'] >= ratings_min)]

        st.write(filtered_data[['Name', 'RATINGS', 'SATISFACTION','SURGERY TYPE','Medical Intervention','QUALIFICATIONS']])

    # Show data visualization
    if st.checkbox("Show Distribution of Specialists by Surgery Type"):
        surgery_type_counts = filtered_data['SURGERY TYPE'].value_counts()
        st.bar_chart(surgery_type_counts)

    # Compare qualifications and ratings
    if st.checkbox("Compare Qualifications and Ratings"):
        qualification_rating_chart = alt.Chart(filtered_data).mark_circle().encode(
            x='RATINGS:Q',
            y='QUALIFICATIONS:N',
            color='QUALIFICATIONS:N',
            tooltip=['Name', 'RATINGS', 'QUALIFICATIONS']
        ).properties(
            width=600,
            height=300
        ).interactive()
        st.altair_chart(qualification_rating_chart)

    # Show additional insights
    
    st.write("""
""")
    st.write("""
""")
    # Feedback Mechanism
    if st.button("Provide Feedback"):
        feedback = st.text_area("Share your feedback:", height=100)
        if st.button("Submit"):
            # Code to submit feedback (e.g., store it in a database)
            st.success("Thank you for your feedback!")
    