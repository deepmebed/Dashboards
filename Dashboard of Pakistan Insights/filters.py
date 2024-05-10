import streamlit as st
def show_sidebar():
    st.sidebar.title("🔎 Filters")
    selected_option = st.sidebar.selectbox("Select", ["Population", "Literacy & Unemployment Rate",
                                                      "Agricultural Data", "GDP"], index=0)
    if selected_option == "Population":
        selected_plot = st.sidebar.selectbox("Select Plot", ["Population Over Time", "Annual Percentage Change",
                                                             "Future Population", "Migration Trend",
                                                             "Globally", "Suicide Rate"], index=0)
    elif selected_option == "Literacy & Unemployment Rate":
        selected_plot = st.sidebar.selectbox("Select Plot", ["Literacy Rate", "Unemployment Rate",
                                                             "Annual Unemployment Change"])
    elif selected_option == "Agricultural Data":
        selected_plot = st.sidebar.selectbox("Select Plot", ["Fertilizer Consumption", "Agricultural land",
                                                             "Arable Land", "Cereal Production", "Forest Area",
                                                             "Cereal Yield", "permanent cropland",
                                                             "Access to electricity",
                                                             "Value to GDP", "employment %"])
    elif selected_option == "GDP":
        selected_plot = st.sidebar.selectbox("Select", ['GDP over Time', "Net Primary Income",
                                                        'Contribution to GDP Over Time',
                                                        'GDP vs Taxes Over Time','GDP vs Gross National Income',
                                                        'Distribution of GDP Across Sectors',
                                                        'GDP vs. Taxes vs. Subsidies',
                                                        "GDP at Current Market Prices"])

    return selected_option, selected_plot
