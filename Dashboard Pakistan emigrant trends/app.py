import streamlit as st
from home import home_page
from by_region import by_region
from by_country import by_country
from report import report_
# Set page title and favicon
st.set_page_config(
    page_title="PED(Pakistan Emigrants Dashboard)",
    page_icon=":bar_chart:",
    layout="wide"
)
def main():
    st.title(":small_airplane: Pakistan Emigration Trends(1981-2023)")
    st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
    st.sidebar.title("Navigation")
    st.sidebar.write("")
    st.sidebar.write("")
    page = st.sidebar.radio("Select Page", ["Home", "Region wise", "Country wise", "Report"])

    if page == "Home":
        home_page()
    elif page == "Region wise":
        by_region()
    elif page == "Country wise":
        by_country()
    elif page == "Report":
        report_()

if __name__ == "__main__":
    main()
