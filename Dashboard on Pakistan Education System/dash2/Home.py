import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Pakistan Education System Dashboard",
                   page_icon=":school:",
                   layout="wide"
                   )
st.title(":school: Pakistan Education System")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

df_school = pd.read_csv("D:/dash/population wise schools.csv")

col1, col2, col3 = st.columns(3)

with col1:
    province = st.selectbox("Select a Province", df_school["province"].unique())

with col2:
    divisions_for_province = df_school[df_school["province"] == province]["division"].unique()
    division = st.multiselect("Select a Division", divisions_for_province)

with col3:
    indicator = st.selectbox('Select',
                             ('Population', 'Growth Rate',
                              'Area(km²)', 'Density(people/km²)'))

filtered_df = df_school[df_school["province"] == province]
if division:
    filtered_df = filtered_df[filtered_df["division"].isin(division)]


fig = go.Figure()

for div in filtered_df['division'].unique():
    div_df = filtered_df[filtered_df['division'] == div]
    fig.add_trace(go.Bar(x=div_df["district"], y=div_df[indicator], name=div))

fig.update_layout(
    title=f"{indicator} in {province} over the selected divisions",
    xaxis_title="District",
    yaxis_title=indicator,
    xaxis=dict(tickangle=45),
    barmode='group',
    width=800,
    height=600
)

# Display plot
st.plotly_chart(fig)
