import pandas as pd
import streamlit as st
from plotly import graph_objects as go

st.set_page_config(page_title="Pakistan Education System Dashboard",
                   page_icon=":school:",
                   layout="wide"
                   )

st.title("Number of Schools")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

df_school = pd.read_csv("D:/dash/population wise schools.csv")

col1, col2, col3 = st.columns(3)

with col1:
    province = st.selectbox("Select a Province", df_school["province"].unique())

with col2:
    divisions_for_province = df_school[df_school["province"] == province]["division"].unique()
    division = st.multiselect("Select Division", divisions_for_province)
with col3:
    districts_for_divisions = df_school[df_school["division"].isin(division)]["district"].unique()
    district = st.multiselect("Select a District", districts_for_divisions)

options = {"labels": ["filtered_df['primary_boys_schools']", "filtered_df['primary_girls_schools']",
                      "filtered_df['secondary_boys_schools']", "filtered_df['secondary_girls_schools']",
                      "filtered_df['high_boys_schools']", "filtered_df['high_girls_schools']",
                      "filtered_df['Intermediate_boys_schools']", "filtered_df['Intermediate_girls_schools']"],
           "plot_labels": [
               "Primary Boys Schools",
               "Primary Girls Schools",
               "Secondary Boys Schools",
               "Secondary Girls Schools",
               "High Boys Schools",
               "High Girls Schools",
               "Intermediate Boys Schools",
               "Intermediate Girls Schools"
           ]}

filtered_df = df_school[df_school["province"] == province]
if division:
    filtered_df = filtered_df[filtered_df["division"].isin(division)]
if district:
    filtered_df = filtered_df[filtered_df["district"].isin(district)]

values = []
for label in options["labels"]:
    values.append(eval(label).sum())

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#E8C872', '#FFD28F']
fig1 = go.Figure(go.Bar(x=options["plot_labels"], y=values, marker_color=colors))
fig1.update_layout(
    title="Total Schools by School Types",
    xaxis_title="School Types",
    yaxis_title="Total Schools",
    xaxis=dict(tickangle=45),
    barmode='group',
    width=800,
    height=600
)

st.plotly_chart(fig1)
