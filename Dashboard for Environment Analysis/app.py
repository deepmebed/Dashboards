import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Pakistan Environment Analysis Dashboard")
st.write("The Pakistan Environment Analysis Dashboard provides a comprehensive overview of environmental trends and indicators across various sectors in Pakistan. This interactive dashboard offers users the opportunity to explore and analyze key environmental data, ranging from agricultural production to energy consumption, in an intuitive and accessible manner.")
st.sidebar.header("Select the data you want to see:")
main_option=st.sidebar.radio('Select', [""]+["Agricultural production","Density & urbanization", "Emissions", "Energy production & use", "Freshwater"])
def main(path, main_options_list):
    df = pd.read_csv(path)
    #st.write(df)
    
    #st.sidebar.header("Select the data you want to see:")
    #main_option = st.sidebar.radio("Select", ["" ] + [option["name"] for option in main_options_list])
    
    #st.write(main_option)
    selected_variables = None
    if main_option:  # Check if a main option is selected
        for option in main_options_list:
            if option["name"] == main_option:
                selected_variables = option["variables"]
                break

    if selected_variables:
        st.sidebar.subheader("Select variable")
        variable = st.sidebar.selectbox("Variable", ["" ] + selected_variables)
        if variable:
            plot = st.selectbox("In which way you want to plot data", ["Line", "Bar", "Histogram", "Scatter", "Area"])
            if plot == "Line":
                color="black"
                st.line_chart(df.set_index("Year")[variable])
            elif plot == "Bar":
                st.bar_chart(df.set_index("Year")[variable])
            elif plot == "Histogram":
                fig, ax = plt.subplots()
                ax.hist(df.set_index("Year")[variable], bins=10, edgecolor="black")
                st.pyplot(fig)
                #st.bar_chart(df.set_index("Year")[variable])  # Change to st.histogram() if needed
            elif plot == "Scatter":
                st.scatter_chart(df.set_index("Year")[variable])  # Change to st.scatter_chart() if needed
            elif plot == "Area":
                st.area_chart(df.set_index("Year")[variable])

            st.header("Do you want to see statistical information?")
            stats_options = st.multiselect("Select", ["Maximum", "Minimum", "Average"])
                
            
            if "Maximum" in stats_options:
                df1=df.set_index("Year")
                max_value = df1[variable].max()
                max_year_index = df1[df1[variable] == max_value].index[0]
                st.write(f"Maximum value for {variable}: {max_value} (Year: {max_year_index})")
                        
            if "Minimum" in stats_options:
                df1=df.set_index("Year")
                min_value = df1[variable].min()
                min_year_index = df1[df1[variable] == min_value].index[0]
                st.write(f"Minimum value for {variable}: {min_value} (Year: {min_year_index})")
                    
            if "Average" in stats_options:
                df1=df.set_index("Year")
                mean_value = df1[variable].mean()
                st.write(f"Average value for {variable}: {mean_value}")

            
            st.header("Select Analysis")
            analysis_choice = st.radio("Choose Analysis", [""]+["Correlation Matrix Heatmap", "Scatter Plot"])
            
            if analysis_choice == "Correlation Matrix Heatmap":

                st.subheader("Correlation Matrix Heatmap")
                selected_columns = df.columns[3:]
                df_selected = df[selected_columns]
                # Select the variables to compare with
                variables_to_compare_with = st.multiselect("Select Variables to Compare with", df_selected.columns)

                # Filter the DataFrame to include only the selected variables
                selected_variables = variables_to_compare_with + [variable]
                df_selected = df[selected_variables]

                # Compute the correlation matrix
                correlation_matrix = df_selected.corr()

                # Plot correlation matrix heatmap
                st.write("This heatmap visualizes the correlation between the selected variable and other variables.")
                fig, ax = plt.subplots(figsize=(12, 8))
                sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
                st.pyplot(fig)

                
            
            if analysis_choice == "Scatter Plot":
                st.subheader("Scatter Plot")
                df = df.iloc[:, 1:]
                # Select numerical columns for scatter plot
                numerical_columns = df.select_dtypes(include=["int", "float"]).columns.tolist()
                variable_to_compare_with = st.multiselect("Select Variables to Compare with", numerical_columns)

                # Plot scatter plots for each combination of the selected variables
                for variable_to_compare in variable_to_compare_with:
                    st.subheader(f"Scatter Plot of {variable} vs {variable_to_compare}")
                    fig, ax = plt.subplots(figsize=(10, 6))
                    sns.scatterplot(x=variable, y=variable_to_compare, data=df, s=50, ax=ax)
                    ax.set_xlabel(variable)
                    ax.set_ylabel(variable_to_compare)
                    ax.grid(True)
                    st.pyplot(fig)





    return main_option



#file_paths = [r"C:\Users\LAIBA\Downloads\Projects\Pak1.csv", r"C:\Users\LAIBA\Downloads\Projects\Pak2.csv"]





main(path=r"C:\Users\LAIBA\OneDrive\Desktop\streamlit_Dashboards\App Dataset\Pak1.csv", main_options_list=[{"name": "Agricultural production", "variables":["Agricultural machinery, tractors", 
"Aquaculture production (metric tons)",
"Capture fisheries production (metric tons)",
"Cereal production (metric tons)",
"Cereal yield (kg per hectare)",
"Crop production index (2014-2016 = 100)",
"Fertilizer consumption (% of fertilizer production)",
"Fertilizer consumption (kilograms per hectare of arable land)",
"Food production index (2014-2016 = 100)",
"Land under cereal production (hectares)",
"Livestock production index (2014-2016 = 100)",
"Total fisheries production (metric tons)"]},
])
main(path=r"C:\Users\LAIBA\OneDrive\Desktop\streamlit_Dashboards\App Dataset\Pak2.csv", main_options_list=[{"name": "Density & urbanization",
"variables": ["Population density(Per km of land area)", "Population in largest city",
"Population in the largest city (Per of urban population)",
"Population in urban agglomerations of more than 1 million",
"Population in urban agglomerations of more than 1 million (Per of total population)",
"Rural population",
"Rural population (Per of total population)",
"Rural population growth (annual %)",
"Urban population",
"Urban population (Per of total population)",
"Urban population growth (annual %)"
]}
])


main(path=r"C:\Users\LAIBA\OneDrive\Desktop\streamlit_Dashboards\App Dataset\Pak3.csv", main_options_list=[{"name":"Emissions",
"variables": ["Agricultural methane emissions (Per of total)","Agricultural nitrous oxide emissions (Per of total)",
"CO2 emissions from electricity and heat production, total (Per of total fuel combustion)",
"CO2 emissions from gaseous fuel consumption (Per of total)",
"CO2 emissions from gaseous fuel consumption (kt)",
"CO2 emissions from liquid fuel consumption (Per of total)",
"CO2 emissions from liquid fuel consumption (kt)",
"CO2 emissions from manufacturing industries and construction (Per of total fuel combustion)",
"CO2 emissions from other sectors, excluding residential buildings and commercial and public services (Per of total fuel combustion)",
"CO2 emissions from residential buildings and commercial and public services (Per of total fuel combustion)",
"CO2 emissions from solid fuel consumption (Per of total)",
"CO2 emissions from solid fuel consumption (kt)",
"CO2 emissions from transport (Per of total fuel combustion)",
"CO2 intensity (kg per kg of oil equivalent energy use)",
"Energy related methane emissions (Per of total)",
"Nitrous oxide emissions in energy sector (Per of total)",
"Total greenhouse gas emissions (kt of CO2 equivalent)"
]}])

main(path=r"C:\Users\LAIBA\OneDrive\Desktop\streamlit_Dashboards\App Dataset\Pak40.csv" , main_options_list=[{"name":"Energy production & use",
"variables": ["Access to clean fuels and technologies for cooking (Per of population)",
"Access to clean fuels and technologies for cooking, rural (Per of rural population)",
"Access to clean fuels and technologies for cooking, urban (Per of urban population)",
"Access to electricity (Per of population)",
"Access to electricity, rural (Per of rural population)",
"Access to electricity, urban (Per of urban population)",
"Alternative and nuclear energy (Per of total energy use)",
"Combustible renewables and waste (Per of total energy)",
"Electric power consumption (kWh per capita)",
"Electric power transmission and distribution losses (Per of output)",
"Electricity production from coal sources (Per of total)",
"Electricity production from hydroelectric sources (Per of total)",
"Electricity production from natural gas sources (Per of total)",
"Electricity production from nuclear sources (Per of total)",
"Electricity production from oil sources (Per of total)",
"Electricity production from oil, gas and coal sources (Per of total)",
"Energy imports, net (Per of energy use)",
"Energy use (kg of oil equivalent per capita)",
"Energy use (kg of oil equivalent) per $1,000 GDP (constant 2017 PPP)",
"Fossil fuel energy consumption (Per of total)",
"Renewable electricity output (Per of total electricity output)",
"Renewable energy consumption (Per of total final energy consumption)"

]}])

main(path=r"C:\Users\LAIBA\OneDrive\Desktop\streamlit_Dashboards\App Dataset\Pak5.csv", main_options_list=[{"name": "Freshwater",
"variables": ["Annual freshwater withdrawals, agriculture (Per of total freshwater withdrawal)",
"Annual freshwater withdrawals, domestic (Per of total freshwater withdrawal)",
"Annual freshwater withdrawals, industry (Per of total freshwater withdrawal)",
"Annual freshwater withdrawals, total (Per of internal resources)",
"Annual freshwater withdrawals, total (billion cubic meters)",
"Level of water stress: freshwater withdrawal as a proportion of available freshwater resources",
"Renewable internal freshwater resources per capita (cubic meters)",
"Renewable internal freshwater resources, total (billion cubic meters)",
"Water productivity, total (constant 2015 US$ GDP per cubic meter of total freshwater withdrawal)"]
}])