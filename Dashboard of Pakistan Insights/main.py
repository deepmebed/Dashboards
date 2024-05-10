import streamlit as st
from demography import plot_demography
from filters import show_sidebar
from Agriculture import plot_agriculture
from LU_rate import plot_LU_rate
from GDP import plot_GDP
st.set_page_config(page_title="Pakistan Insights Dashboard", page_icon="📊")

def main():
    st.title("Pakistan Insights Dashboard")
    st.markdown("### Unlock the Insights. Empower Your Decisions.")
    st.image("Pakistan.PNG", use_column_width=True)
    selected_option, selected_plot = show_sidebar()
    if selected_option == "Population":
        plot_demography(selected_plot)
    elif selected_option == "Literacy & Unemployment Rate":
        plot_LU_rate(selected_plot)
    elif selected_option == "Agricultural Data":
        plot_agriculture(selected_plot)
    elif selected_option == "GDP":
        plot_GDP(selected_plot)



if __name__ == "__main__":
    main()
