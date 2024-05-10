import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import os

st.set_page_config(page_title="",page_icon=":bar_chart",layout="wide")
st.title("Sleep Health and Life Style🏃‍♂️ ")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)
fl = st.file_uploader(":fl =st.file_uploader :file_folder, Upload a file",type=(["xls","csv","xlsx","xls"]))
if fl is not None:
    filename = fl.name
    st.write("filename")
    df = pd.read_csv("Sleep_health_and_lifestyle_dataset.csv")
else:
    os.chdir(r"C:\Users\pakcomp\OneDrive\Desktop\project1")
    df = pd.read_csv("Sleep_health_and_lifestyle_dataset.csv")


# Create sidebar filters
st.sidebar.header("Choose your filter: ")
Gender = st.sidebar.multiselect("pick your Gender", df["Gender"].unique())

# Define filter function
def filter_by_gender(df, Gender):
    if 'Male' in Gender:
        filtered_df = df[df['Gender'] == 'Male']
    elif 'Female' in Gender:
        filtered_df = df[df['Gender'] == 'Female']
    else:
        filtered_df = df
    return filtered_df

# Apply gender filter
filtered_data = filter_by_gender(df, Gender)

# Age wise slider
age_min = int(filtered_data['Age'].min())
age_max = int(filtered_data['Age'].max())
age_default = (age_min, age_max)
selected_age_range = st.sidebar.slider("Age Range", age_min, age_max, age_default)
filtered_df = df[(df['Age'] >= selected_age_range[0]) & (df['Age'] <= selected_age_range[1])]

 # Creating the Plotly bar chart
#fig_sleep_duration = px.bar(filtered_df, x='Sleep Duration', y='Age', color='Gender', barmode='group',title='Sleep Duration 😴')
#fig_sleep_duration.update_layout(xaxis_title='Sleep Duration', yaxis_title='Age count', 
#                              yaxis={'tickmode': 'linear', 'dtick': 10})
filtered_df_filtered = filtered_df[(filtered_df['Age'] >= 27) & (filtered_df['Age'] <= 59)]
print(filtered_df_filtered)
fig_sleep_duration = px.bar(filtered_df, 
                            x='Sleep Duration', 
                            y='Age', 
                            title='Sleep Duration 😴',
                            color_discrete_sequence=px.colors.qualitative.Set1)  # Customize color palette if needed

fig_sleep_duration.update_layout(xaxis_title='Sleep Duration', 
                                 yaxis_title='Age count')
                                
# Assuming filtered_df contains your filtered DataFrame
 # Update y-axis settings

#fig_sleep_duration.show()

                                

# Displaying the chart using Streamlit
st.plotly_chart(fig_sleep_duration, use_container_width=True)
st.write("Selected Age Range:",selected_age_range)
# Create filters for sleep disorder, occupation, BMI
st.sidebar.header("Choose your filter: ")
sleep_disorder = st.sidebar.multiselect("Pick your sleep disorder", df["Sleep Disorder"].unique())
Occupation = st.sidebar.multiselect("Pick your Occupation", df["Occupation"].unique())
Bmi_Category = st.sidebar.multiselect("Pick your BMI", df["BMI Category"].unique())
if sleep_disorder:
    df = df[df["Sleep Disorder"].isin(sleep_disorder)]
if Occupation:
    df = df[df["Occupation"].isin(Occupation)]
if Bmi_Category:
    df = df[df["BMI Category"].isin(Bmi_Category)]
fig_age_bmi = px.bar(df, x='Age', y='BMI Category', color='Gender', barmode='group', title='Age wise BMI')
# Update layout to adjust x-axis range and tick interval
fig_age_bmi.update_layout(xaxis_title='Age', yaxis_title='BMI Category')
fig_age_bmi.update_xaxes(title='Age', tickvals=list(df['Age'][::5]), dtick=5)
fig_age_bmi.update_yaxes(title='BMI Category')
st.plotly_chart(fig_age_bmi, use_container_width=200)
# Create bar graph for occupation wise BMI
fig_occupation_bmi = px.bar(df, x='Occupation', y='BMI Category', color='Gender', barmode='group',
                            title="Occupation wise BMI ")
fig_occupation_bmi.update_layout(xaxis_title='Occupation', yaxis_title='BMI Category')
st.plotly_chart(fig_occupation_bmi, use_container_width=200)


st.title(' Selection Demo')

selected_features = st.multiselect('Select features', df.columns[1:])
selected_chart_type = st.selectbox('Select Chart Type', ['Line Chart', 'Bar Graph', 'Pie Chart', 'Boxplot'])

if selected_features:
    selected_df = df[selected_features]

    if selected_chart_type == 'Line Chart':
        st.write('### Line Chart')
        fig_line_chart = px.line(selected_df, x=selected_df.index, y=selected_df.columns)
        st.plotly_chart(fig_line_chart, use_container_width=True)

    elif selected_chart_type == 'Bar Graph':
        st.write('### Bar Graph')
        fig_bar_chart = px.bar(selected_df, x=selected_df.index, y=selected_df.columns)
        st.plotly_chart(fig_bar_chart, use_container_width=True)

    elif selected_chart_type == 'Pie Chart' and len(selected_features) == 1:
        st.write('### Pie Chart')
        fig_pie_chart = px.pie(df, values=selected_features[0], names=df['Category'],
                               title=f'{selected_features[0]} Distribution')
        st.plotly_chart(fig_pie_chart, use_container_width=True)

    elif selected_chart_type == 'Boxplot':
        st.write('### Boxplot')
        fig_boxplot = px.box(selected_df, x='Gender', y=selected_df.columns[0])
        st.plotly_chart(fig_boxplot, use_container_width=True)
    else:
        st.write('Please select only one feature for Pie Chart.')

else:
    st.write('Please select features.')