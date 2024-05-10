import streamlit as st
import pandas as pd
import plotly.express as px
st.title("Kidney Disease Dashboard")
data = pd.read_csv('kidney_disease.csv')
data

st.sidebar.title("Filters the  Visualizations")

age_min = int(data['age'].min())
age_max = int(data['age'].max())
age_default = (age_min, age_max)
age_range = st.sidebar.slider("Age Range", age_min, age_max, age_default)
visualization = st.sidebar.selectbox("Select Visualization", ['Histogram', 'Scatter Plot','barchart','linechart'])
 
pc_options = ['normal', 'abnormal']
selected_pc = st.sidebar.selectbox("Select pc", pc_options)

    # Select box for 'pcc'
pcc_options = ['present', 'notpresent']
selected_pcc = st.sidebar.selectbox("Select pcc", pcc_options)

    # Select box for 'appet'
appet_options = ['good', 'poor']
selected_appet = st.sidebar.selectbox("Select appet", appet_options)
filtered_data = data[
    (data['age'] >= age_range[0]) & (data['age'] <= age_range[1]) &
    (data['pc'] == selected_pc) & 
    (data['pcc'] == selected_pcc) &
    (data['appet'] == selected_appet)
]

if visualization == 'Histogram':
        st.write("### Histogram of Age")
        fig = px.histogram(filtered_data, x='age', nbins=40, title="Histogram of Age")
        st.plotly_chart(fig)

elif visualization == 'Scatter Plot':
        st.write("### Scatter Plot of Age vs. Blood Pressure")
        fig = px.scatter(filtered_data, x='age', y='bp', title="Scatter Plot of Age vs. Blood Pressure")
        st.plotly_chart(fig)
        
 #Display graphs for even-numbered features
selected_features = st.multiselect("Select Features", data.columns)
even_features = [col for col in selected_features if data.columns.get_loc(col) % 2 == 0]
if even_features:
        st.write("### Graphs for Even Selection Features")
        for feature in even_features:
            fig = px.histogram(data, x=feature, title=f"Histogram of {feature}")
            st.plotly_chart(fig)
else:
        st.write("### No Even Selection Features chosen.")


if visualization == 'Histogram':
    st.write("### Histogram of Age")
    fig = px.histogram(filtered_data, x='age', nbins=30, title="Histogram of Age")
    st.plotly_chart(fig)

elif visualization == 'Scatter Plot':
    st.write("### Scatter Plot of Age vs. Blood Pressure")
    fig = px.scatter(filtered_data, x='age', y='bp', title="Scatter Plot of Age vs. Blood Pressure")
    st.plotly_chart(fig)

elif visualization == 'Line Plot':
    st.write("### Line Plot of Selected Features")
    selected_features = st.multiselect("Select Features", data.columns)
    for feature in selected_features:
        fig = px.line(data, x='age', y=feature, title=f"Line Plot of {feature}")
        st.plotly_chart(fig)
        
fig_age_bmi = px.bar(data, x='age', y='sc', barmode='group', title='Age wise sc')
fig_age_bmi.update_layout(xaxis_title='Serum Cretinine', yaxis_title='Age')
st.plotly_chart(fig_age_bmi, use_container_width=True)


selected_features = st.multiselect('Select features', data.columns[1:])
selected_chart_type = st.selectbox('Select Chart Type', ['Line Chart', 'Bar Graph', 'Pie Chart', 'Boxplot'])

# Prepare data for selected features
if selected_features:
    selected_df = data[selected_features]

    # Display chart based on selected type
    if selected_chart_type == 'Line Chart':
        st.write('### Line Chart')
        fig_line_chart = px.line(selected_df, x=selected_df.index, y=selected_df.columns)
        st.plotly_chart(fig_line_chart, use_container_width=True)

# Bubble chart
fig = px.scatter(filtered_data, x='bp', y='al', size='bp', color='id', hover_name='id',
                 labels={'bp': 'blood pressure', 'al': 'al Level'},
                 title='Bubble Chart: BP vs Albumin')
fig.update_traces(marker=dict(line=dict(width=2, color='DarkSlateGrey')))
fig.update_layout(autosize=False, width=800, height=600)
st.plotly_chart(fig)