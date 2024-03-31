import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("agriculture.csv")


def plot_agriculture(selected_plot):
    st.title("🌾 Agricultural Data")
    if selected_plot == "Fertilizer Consumption":
        fig1 = px.line(df, x='Year', y='Fertilizer consumption (% of fertilizer production)',
                       title='Fertilizer Consumption', color_discrete_sequence=['#007bff'])
        st.plotly_chart(fig1, use_container_width=True)
    elif selected_plot == 'Agricultural land':
        fig2 = px.line(df, x='Year', y='Agricultural land (sq. km)', title='Agricultural Land')
        st.plotly_chart(fig2, use_container_width=True)
    elif selected_plot == 'Cereal Production':
        fig3 = px.line(df, x='Year', y='Cereal production (metric tons)', title='Cereal Production')
        st.plotly_chart(fig3, use_container_width=True)
    elif selected_plot == 'Arable Land':
        fig4 = px.line(df, x='Year', y='Arable land (hectares)', title='Arable Land (hectares)')
        st.plotly_chart(fig4, use_container_width=True)
    elif selected_plot == 'Forest Area':
        fig5 = px.line(df, x='Year', y='Forest area (sq. km)', title='Forest Area Over Time')
        st.plotly_chart(fig5, use_container_width=True)
    elif selected_plot == 'Cereal Yield':
        fig6 = px.line(df, x='Year', y='Cereal yield (kg per hectare)', title='Cereal Yield Over Time')
        st.plotly_chart(fig6, use_container_width=True)
    elif selected_plot == "permanent cropland":
        fig7 = px.line(df, x="Year", y='Permanent cropland (% of land area)', title='Permanent Cropland Area')
        st.plotly_chart(fig7, use_container_width=True)
    elif selected_plot == "Access to electricity":
        fig8 = px.bar(df, x='Year', y='Access to electricity, rural (% of rural population)',
                      title='Access to Electricity in Rural Areas')
        st.plotly_chart(fig8, use_container_width=True)
    elif selected_plot == "Value to GDP":
        fig9 = px.line(df, x='Year', y='Agriculture, forestry, and fishing, value added (% of GDP)',
                       title='Agriculture, Forestry, and Fishing Value Added')
        st.plotly_chart(fig9, use_container_width=True)
    elif selected_plot == "employment %":
        s = st.sidebar.selectbox("select", ["Total", "Gender based"])
        if s == "Total":
            fig10 = px.line(df, x='Year', y='Employment in agriculture (% of total employment)',
                        title='Employment in Agriculture Distribution by Year')
            st.plotly_chart(fig10, use_container_width=True)
        elif s == "Gender based":
            fig11 = px.line(df, x='Year', y=['Employment in agriculture, male (% of male employment)',
                                         "Employment in agriculture, female (% of female employment)"])
            st.plotly_chart(fig11, use_container_width=True)