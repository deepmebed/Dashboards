import pandas as pd
import streamlit as st
from plotly import graph_objects as go

st.set_page_config(page_title="Pakistan Education System Dashboard",
                   page_icon=":school:",
                   layout="wide"
                   )

st.title("Number of Students")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

df_enrolled = pd.read_csv("D:/dash/Enrolment of Students in Educational Institutes of Pakistan 1947-2018.csv")

selected_years = st.multiselect("Select Years", df_enrolled["Year"].unique())

select = {
    "select1": [
        df_enrolled['Primary'], df_enrolled['Middle'], df_enrolled['High'],
        df_enrolled['Higher Secondary Colleges'], df_enrolled['Degree Colleges'],
        df_enrolled['Technical Colleges'], df_enrolled['Universities']
    ],
    "plot_labels": ["Primary", "Middle", "High", "Higher Secondary Colleges",
                    "Degree Colleges", "Technical Institutes", "Universities"]
}

fig = go.Figure()
for year in selected_years:
    fig = go.Figure()
    for idx, category in enumerate(select["select1"]):
        fig.add_trace(
            go.Bar(
                x=[select["plot_labels"][idx]],
                y=[category[df_enrolled['Year'] == year].values[0]],
                name=select["plot_labels"][idx]
            )
        )

fig.update_layout(
    title="Enrollment Statistics per Year",
    xaxis_title="Category",
    yaxis_title="Number of Students",
    barmode='group',
    width=800,
    height=600
)

st.plotly_chart(fig)
