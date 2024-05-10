import streamlit as st
import pandas as pd
import plotly.express as px

df1 = pd.read_csv("pakistan-population-2024-03-15.csv")
df2 = pd.read_excel("pakistan-population-2025-2100.xlsx")
df3 = pd.read_excel("pop_pak.xlsx")
df4 = pd.read_excel("suicide_rate.xlsx")

def plot_demography(selected_plot):
    st.title("🧑‍🤝‍🧑 Population Facts")

    if selected_plot == "Population Over Time":
        fig = px.line(df1, x='date', y='Population', title='Population Over Time')
        st.plotly_chart(fig, use_container_width=True)
    elif selected_plot == "Annual Percentage Change":
        fig = px.line(df1, x='date', y='Annual % Change', title='Annual Percentage Change')
        st.plotly_chart(fig, use_container_width=True)
    elif selected_plot == "Future Population":
        fig = px.line(df2, x='Date', y='Population', title='Future Population')
        st.plotly_chart(fig, use_container_width=True)
    elif selected_plot == "Migration Trend":
        fig = px.line(df3, x='Year', y='Migrants', title='Migration trend')
        st.plotly_chart(fig, use_container_width=True)
    elif selected_plot == "Globally":
        fig = px.bar(df3, x="Year", y="Global Rank", color="Year", title="Global Rank")
        st.plotly_chart(fig, use_container_width=True)
    elif selected_plot == "Suicide Rate":
        s = st.sidebar.selectbox("select",["Female","Male","Comparison"])
        if s == "Female":
            fig = px.bar(df4, x="Age Group", y="Female", title="Female suicide rate per 100k", color="Age Group")
            st.plotly_chart(fig, use_container_width=True)
        elif s == "Male":
            fig1 = px.bar(df4, x="Age Group", y="Male", title="Male suicide rate per 100k", color="Age Group")
            st.plotly_chart(fig1, use_container_width=True)
        elif s == "Comparison":
            fig = px.line(df4, x="Age Group", y=["Female","Male"])
            st.plotly_chart(fig, use_container_width=True)
