import pandas as pd
import streamlit as st
from plotly import graph_objects as go

st.set_page_config(page_title="Pakistan Education System Dashboard",
                   page_icon=":school:",
                   layout="wide"
                   )

st.title("Number of Teachers")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

df_teacher = pd.read_csv("D:/dash/Number of Teachers in Educational Institutions of Pakistan 1947-2018.csv")

selected_year = st.multiselect("Select Years", df_teacher["Year"].unique())

selected = {"select1":
                ["df_teacher['Primary']", "df_teacher['Middle']", "df_teacher['High']",
                 "df_teacher['Higher Secondary Colleges']", "df_teacher['Degree Colleges']",
                 "df_teacher['Technical Colleges']", "df_teacher['Universities']"],

            "plot_labels": ["Primary", "Middle", "High", "Higher Secondary Colleges",
                            "Degree Colleges", "Technical Institutes", "Universities"]
            }

fig2 = go.Figure()
for year in selected_year:
    fig2 = go.Figure()
    for idx, category in enumerate(selected["select1"]):
        fig2.add_trace(
            go.Bar(x=[selected["plot_labels"][idx]], y=[eval(category).loc[df_teacher['Year'] == year].values[0]],
                   name=selected["plot_labels"][idx])
        )

fig2.update_layout(title=f"Number of Teachers Available per Year",
                   xaxis_title="Types of Institutes",
                   yaxis_title="Number of Teachers Available",
                   barmode='group',
                   width=800,
                   height=600

                   )

st.plotly_chart(fig2)

