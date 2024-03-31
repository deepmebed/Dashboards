import streamlit as st
import pandas as pd
import plotly.express as px

df1 = pd.read_csv("literacy rate.csv")
df2 = pd.read_csv("pakistan-unemployment-rate.csv")

def plot_LU_rate(selected_plot):
    st.title("📈 Literacy & Unemployment Rate")

    if selected_plot == "Literacy Rate":
        fig1 =px.line(df1, x="year", y="Literacy rate", title="Literacy Rate")
        st.plotly_chart(fig1, use_container_width=True)
    elif selected_plot == "Unemployment Rate":
        fig2 =px.line(df2, x="date", y=" Unemployment Rate (%)", title="Unemployment %")
        st.plotly_chart(fig2, use_container_width=True)
    elif selected_plot == "Annual Unemployment Change":
        fig3 =px.line(df2, x="date", y=" Annual Change", title="Annual Unemployment Change")
        st.plotly_chart(fig3, use_container_width=True)