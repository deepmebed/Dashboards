import pandas as pd
import streamlit as st
from plotly import graph_objects as go

st.set_page_config(page_title="Pakistan Education System Dashboard",
                   page_icon=":school:",
                   layout="wide"
                   )

st.title("Available Facilities")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

df = pd.read_csv("D:/dash/education.csv")

col1, col2, col3 = st.columns(3)

with col1:
    province = st.selectbox("Select a Province", df["Province"].unique())

with col2:
    indicator = st.selectbox('Select a Facility',
                             ('Electricity', 'Drinking water', 'Boundary wall',
                              'Building condition satisfactory',
                              'Toilet'
                              ))

with col3:
    year = st.selectbox("Select a Year", df["Year"].unique())
    if not isinstance(year, list):
        year = [year]

filtered_df = df[(df["Province"] == province) & (df["Year"].isin(year))]

fig = go.Figure()

for y in year:
    subset_df = filtered_df[filtered_df["Year"] == y]
    fig.add_trace(go.Scatter(x=subset_df["City"], y=subset_df[indicator], mode='lines+markers', name=str(y)))

fig.update_layout(
    title=f"Percentage of Schools with {indicator} in {province} over the selected years",
    xaxis_title="City",
    yaxis_title=indicator,
    xaxis=dict(tickangle=-45),
    legend_title="Year"
)

# Display plot
st.plotly_chart(fig)
