import streamlit as st
import pandas as pd
import plotly.graph_objects as go





# Read the data
data_path = r'C:\Users\HP 840 G4\OneDrive\Documents\wb eda data.xlsx'
df = pd.read_excel(data_path)

st.title('Pakistan Statistic Dashboard')

# Set the index to the 'Years' column
df.set_index('Years', inplace=True)

original_start_year = df.index.min()
original_end_year = df.index.max()

# Function to filter data based on selected options
def filter_data(df, options, start_year, end_year):
    filtered_df = df.loc[start_year:end_year, options]
    return filtered_df

# Function to group consecutive years a government was in power
def group_consecutive_years(years):
    groups = []
    consecutive_years = []
    for i in range(len(years)):
        if i == 0 or years[i] == years[i-1] + 1:
            consecutive_years.append(years[i])
        else:
            groups.append(consecutive_years)
            consecutive_years = [years[i]]
    groups.append(consecutive_years)
    return groups

# Function to render page
def render_page(page_name):
    if page_name == 'Population':
        st.header('Population')
        options = st.multiselect('Select Data',
                                 ['Population, total', 'Population, female', 'Population, male', 'Urban population',
                                  'Rural population'])
        plot_type = st.selectbox('Select Plot Type', ['Line Plot', 'Bar Plot'])

        start_year = st.slider('Select Start Year', min_value=original_start_year, max_value=original_end_year,
                               value=original_start_year, step=1)
        end_year = st.slider('Select End Year', min_value=original_start_year, max_value=original_end_year,
                             value=original_end_year, step=1)

        filtered_df = filter_data(df, options, start_year, end_year)

        # Plot
        fig = go.Figure()

        if plot_type == 'Line Plot':
            for col in options:
                fig.add_trace(go.Scatter(x=filtered_df.index, y=filtered_df[col], mode='lines+markers', name=col))
        elif plot_type == 'Bar Plot':
            for col in options:
                fig.add_trace(go.Bar(x=filtered_df.index, y=filtered_df[col], name=col))

        fig.update_layout(
            title="Population Plot",
            xaxis_title="Years",
            yaxis_title="Values",
            legend_title="Legend",
            hovermode='x unified',  # Show hover information for all traces
        )

        st.plotly_chart(fig)

        st.header('Growth rate')
        selected_loan_options = st.multiselect('Select Data',
                                               ['Population growth (annual %)',
                                                'Life expectancy at birth, total (years)'])
        plot_type_trade = st.selectbox('Select Plot Type ', ['Line Plot', 'Bar Plot'], key='loan_plot_type')

        start_year_trade = st.slider('Select Start Year ', min_value=original_start_year,
                                     max_value=original_end_year,
                                     value=original_start_year, step=1, key='loan_start_year')
        end_year_trade = st.slider('Select End Year ', min_value=original_start_year,
                                   max_value=original_end_year,
                                   value=original_end_year, step=1, key='loan_end_year')

        if selected_loan_options:
            filtered_trade_df = filter_data(df, selected_loan_options, start_year_trade, end_year_trade)
            trade_fig = go.Figure()
            for col in selected_loan_options:
                if plot_type_trade == 'Line Plot':
                    trade_fig.add_trace(go.Scatter(x=filtered_trade_df.index, y=filtered_trade_df[col],
                                                   mode='lines+markers', name=col))
                elif plot_type_trade == 'Bar Plot':
                    trade_fig.add_trace(go.Bar(x=filtered_trade_df.index, y=filtered_trade_df[col], name=col))

            trade_fig.update_layout(
                title="Growth Plot",
                xaxis_title="Years",
                yaxis_title="Values",
                legend_title="Legend",
                hovermode='x unified',  # Show hover information for all traces
            )

            st.plotly_chart(trade_fig)
        return

    elif page_name == 'GDP Growth':
        st.header('GDP Growth')
        selected_options = st.multiselect('Select Data',
                                          ['GDP growth (annual %)', 'Inflation, GDP deflator (annual %)'])
        plot_type = st.selectbox('Select Plot Type', ['Line Plot', 'Bar Plot'])

        start_year = st.slider('Select Start Year', min_value=original_start_year, max_value=original_end_year,
                               value=original_start_year, step=1)
        end_year = st.slider('Select End Year', min_value=original_start_year, max_value=original_end_year,
                             value=original_end_year, step=1)

        filtered_df = filter_data(df, selected_options, start_year, end_year)

        # Plot
        fig = go.Figure()

        if plot_type == 'Line Plot':
            for col in selected_options:
                fig.add_trace(go.Scatter(x=filtered_df.index, y=filtered_df[col], mode='lines+markers', name=col))
        elif plot_type == 'Bar Plot':
            for col in selected_options:
                fig.add_trace(go.Bar(x=filtered_df.index, y=filtered_df[col], name=col))

        fig.update_layout(
            title="GDP Growth Plot",
            xaxis_title="Years",
            yaxis_title="Values",
            legend_title="Legend",
            hovermode='x unified',  # Show hover information for all traces
        )

        st.plotly_chart(fig)

        st.header('Imports and Exports (% of GDP)')
        selected_trade_options = st.multiselect('Select  Data',
                                                ['Imports of goods and services (% of GDP)',
                                                 'Exports of goods and services (% of GDP)'])
        plot_type_trade = st.selectbox('Select Plot Type ', ['Line Plot', 'Bar Plot'], key='trade_plot_type')

        start_year_trade = st.slider('Select Start Year ', min_value=original_start_year,
                                     max_value=original_end_year,
                                     value=original_start_year, step=1, key='trade_start_year')
        end_year_trade = st.slider('Select End Year ', min_value=original_start_year,
                                   max_value=original_end_year,
                                   value=original_end_year, step=1, key='trade_end_year')

        if selected_trade_options:
            filtered_trade_df = filter_data(df, selected_trade_options, start_year_trade, end_year_trade)
            trade_fig = go.Figure()
            for col in selected_trade_options:
                if plot_type_trade == 'Line Plot':
                    trade_fig.add_trace(go.Scatter(x=filtered_trade_df.index, y=filtered_trade_df[col],
                                                   mode='lines+markers', name=col))
                elif plot_type_trade == 'Bar Plot':
                    trade_fig.add_trace(go.Bar(x=filtered_trade_df.index, y=filtered_trade_df[col], name=col))

            trade_fig.update_layout(
                title="Trade Plot",
                xaxis_title="Years",
                yaxis_title="Values",
                legend_title="Legend",
                hovermode='x unified',  # Show hover information for all traces
            )

            st.plotly_chart(trade_fig)
        return

    elif page_name == 'Government Expenditure':
        st.header('Government Expenditure')
        options = ['General government total expenditure(% of GDP)', 'Military expenditure (% of GDP)',
                   'Government expenditure on education, total (% of GDP)', 'Current health expenditure (% of GDP)', 'Total Investment']
        selected_options = st.multiselect('Select Expenditure Data', options)
        plot_type = st.selectbox('Select Plot Type', ['Line Plot', 'Bar Plot'])

        start_year = st.slider('Select Start Year', min_value=original_start_year, max_value=original_end_year,
                               value=original_start_year, step=1)
        end_year = st.slider('Select End Year', min_value=original_start_year, max_value=original_end_year,
                             value=original_end_year, step=1)

        filtered_df = filter_data(df, selected_options, start_year, end_year)

        # Plot
        fig = go.Figure()

        if plot_type == 'Line Plot':
            for col in selected_options:
                fig.add_trace(go.Scatter(x=filtered_df.index, y=filtered_df[col], mode='lines+markers', name=col))
        elif plot_type == 'Bar Plot':
            for col in selected_options:
                fig.add_trace(go.Bar(x=filtered_df.index, y=filtered_df[col], name=col))

        fig.update_layout(
            title="Government Expenditure Plot",
            xaxis_title="Years",
            yaxis_title="Values",
            legend_title="Legend",
            hovermode='x unified',  # Show hover information for all traces
        )

        st.plotly_chart(fig)

    elif page_name == 'Tax and Debt':
        st.header('Revenue and Remittance')
        options = ['Tax revenue (% of GDP)', 'Revenue, excluding grants (% of GDP)', 'Personal remittances, received (% of GDP)']
        selected_options = st.multiselect('Select Data', options)
        plot_type = st.selectbox('Select Plot Type', ['Line Plot', 'Bar Plot'])

        start_year = st.slider('Select Start Year', min_value=original_start_year, max_value=original_end_year,
                               value=original_start_year, step=1)
        end_year = st.slider('Select End Year', min_value=original_start_year, max_value=original_end_year,
                             value=original_end_year, step=1)

        filtered_df = filter_data(df, selected_options, start_year, end_year)

        # Plot
        fig = go.Figure()

        if plot_type == 'Line Plot':
            for col in selected_options:
                fig.add_trace(go.Scatter(x=filtered_df.index, y=filtered_df[col], mode='lines+markers', name=col))
        elif plot_type == 'Bar Plot':
            for col in selected_options:
                fig.add_trace(go.Bar(x=filtered_df.index, y=filtered_df[col], name=col))

        fig.update_layout(
            title="Tax and remittance Plot",
            xaxis_title="Years",
            yaxis_title="Values",
            legend_title="Legend",
            hovermode='x unified',  # Show hover information for all traces
        )

        st.plotly_chart(fig)

        st.header('Debt')
        selected_loan_options = st.multiselect('Select Data',
                                                ['External debt stocks, total (DOD, current US$)', 'Total Disbursements'])
        plot_type_trade = st.selectbox('Select Plot Type ', ['Line Plot', 'Bar Plot'], key='loan_plot_type')

        start_year_trade = st.slider('Select Start Year ', min_value=original_start_year,
                                     max_value=original_end_year,
                                     value=original_start_year, step=1, key='loan_start_year')
        end_year_trade = st.slider('Select End Year ', min_value=original_start_year,
                                   max_value=original_end_year,
                                   value=original_end_year, step=1, key='loan_end_year')

        if selected_loan_options:
            filtered_trade_df = filter_data(df, selected_loan_options, start_year_trade, end_year_trade)
            trade_fig = go.Figure()
            for col in selected_loan_options:
                if plot_type_trade == 'Line Plot':
                    trade_fig.add_trace(go.Scatter(x=filtered_trade_df.index, y=filtered_trade_df[col],
                                                   mode='lines+markers', name=col))
                elif plot_type_trade == 'Bar Plot':
                    trade_fig.add_trace(go.Bar(x=filtered_trade_df.index, y=filtered_trade_df[col], name=col))

            trade_fig.update_layout(
                title="Debt Plot",
                xaxis_title="Years",
                yaxis_title="Values",
                legend_title="Legend",
                hovermode='x unified',  # Show hover information for all traces
            )

            st.plotly_chart(trade_fig)
        return


    elif page_name == 'Internet and Electricity':
        st.header('Internet and Electricity')
        options = ['Individuals using the Internet (% of population)','People using at least basic drinking water services (% of population)', 'Access to electricity (% of population)', 'Electricity production from oil, gas and coal sources (% of total)']
        selected_options = st.multiselect('Select Data', options)
        plot_type = st.selectbox('Select Plot Type', ['Line Plot', 'Bar Plot'])

        start_year = st.slider('Select Start Year', min_value=original_start_year, max_value=original_end_year,
                               value=original_start_year, step=1)
        end_year = st.slider('Select End Year', min_value=original_start_year, max_value=original_end_year,
                             value=original_end_year, step=1)

        filtered_df = filter_data(df, selected_options, start_year, end_year)

        # Plot
        fig = go.Figure()

        if plot_type == 'Line Plot':
            for col in selected_options:
                fig.add_trace(go.Scatter(x=filtered_df.index, y=filtered_df[col], mode='lines+markers', name=col))
        elif plot_type == 'Bar Plot':
            for col in selected_options:
                fig.add_trace(go.Bar(x=filtered_df.index, y=filtered_df[col], name=col))

        fig.update_layout(
            title="Internet and Electricity Plot",
            xaxis_title="Years",
            yaxis_title="Values",
            legend_title="Legend",
            hovermode='x unified',  # Show hover information for all traces
        )

        st.plotly_chart(fig)

        st.header('Unemployment')
        selected_loan_options = st.multiselect('Select Data',
                                               [
                                                'Unemployment, total (% of total labor force)'])
        plot_type_trade = st.selectbox('Select Plot Type ', ['Line Plot', 'Bar Plot'], key='loan_plot_type')

        start_year_trade = st.slider('Select Start Year ', min_value=original_start_year,
                                     max_value=original_end_year,
                                     value=original_start_year, step=1, key='loan_start_year')
        end_year_trade = st.slider('Select End Year ', min_value=original_start_year,
                                   max_value=original_end_year,
                                   value=original_end_year, step=1, key='loan_end_year')

        if selected_loan_options:
            filtered_trade_df = filter_data(df, selected_loan_options, start_year_trade, end_year_trade)
            trade_fig = go.Figure()
            for col in selected_loan_options:
                if plot_type_trade == 'Line Plot':
                    trade_fig.add_trace(go.Scatter(x=filtered_trade_df.index, y=filtered_trade_df[col],
                                                   mode='lines+markers', name=col))
                elif plot_type_trade == 'Bar Plot':
                    trade_fig.add_trace(go.Bar(x=filtered_trade_df.index, y=filtered_trade_df[col], name=col))

            trade_fig.update_layout(
                title="Unemployment Plot",
                xaxis_title="Years",
                yaxis_title="Values",
                legend_title="Legend",
                hovermode='x unified',  # Show hover information for all traces
            )

            st.plotly_chart(trade_fig)

        return

    elif page_name == 'Resources':
        st.header('Agriculture and Industry')
        options = ['Agriculture, forestry, and fishing, value added (% of GDP)',
                   'Industry, value added (% of GDP)']
        selected_options = st.multiselect('Select Data', options)
        plot_type = st.selectbox('Select Plot Type', ['Line Plot', 'Bar Plot'])

        start_year = st.slider('Select Start Year', min_value=original_start_year, max_value=original_end_year,
                               value=original_start_year, step=1)
        end_year = st.slider('Select End Year', min_value=original_start_year, max_value=original_end_year,
                             value=original_end_year, step=1)

        filtered_df = filter_data(df, selected_options, start_year, end_year)

        # Plot
        fig = go.Figure()

        if plot_type == 'Line Plot':
            for col in selected_options:
                fig.add_trace(go.Scatter(x=filtered_df.index, y=filtered_df[col], mode='lines+markers', name=col))
        elif plot_type == 'Bar Plot':
            for col in selected_options:
                fig.add_trace(go.Bar(x=filtered_df.index, y=filtered_df[col], name=col))

        fig.update_layout(
            title="Agriculture and Industry Plot",
            xaxis_title="Years",
            yaxis_title="Values",
            legend_title="Legend",
            hovermode='x unified',  # Show hover information for all traces
        )

        st.plotly_chart(fig)

        st.header('Land')
        selected_trade_options = st.multiselect('Select Data',
                                                [
                                                    'Forest area (% of land area)',
                                                    'Agricultural land (% of land area)'])
        plot_type_trade = st.selectbox('Select Plot Type ', ['Line Plot', 'Bar Plot'],
                                       key='trade_plot_type')

        start_year_trade = st.slider('Select Start Year ', min_value=original_start_year,
                                     max_value=original_end_year,
                                     value=original_start_year, step=1, key='trade_start_year')
        end_year_trade = st.slider('Select End Year ', min_value=original_start_year,
                                   max_value=original_end_year,
                                   value=original_end_year, step=1, key='trade_end_year')

        if selected_trade_options:
            filtered_trade_df = filter_data(df, selected_trade_options, start_year_trade, end_year_trade)
            trade_fig = go.Figure()
            for col in selected_trade_options:
                if plot_type_trade == 'Line Plot':
                    trade_fig.add_trace(go.Scatter(x=filtered_trade_df.index, y=filtered_trade_df[col],
                                                   mode='lines+markers', name=col))
                elif plot_type_trade == 'Bar Plot':
                    trade_fig.add_trace(go.Bar(x=filtered_trade_df.index, y=filtered_trade_df[col], name=col))

            trade_fig.update_layout(
                title="Land Plot",
                xaxis_title="Years",
                yaxis_title="Values",
                legend_title="Legend",
                hovermode='x unified',  # Show hover information for all traces
            )

            st.plotly_chart(trade_fig)

        return

    elif page_name == "Government":
        government = st.selectbox('Select Government', df['Governments'].unique())

        # Get years when the selected government was in power
        government_years = df[df['Governments'] == government].index.tolist()

        # Group consecutive years
        government_periods = group_consecutive_years(government_years)

        # Display government periods
        government_options = [f'{period[0]}-{period[-1]}' for period in government_periods]

        # Allow the user to select multiple government periods
        selected_government_periods = st.multiselect('Select Government Period', government_options)

        options = [
            'Current health expenditure (% of GDP)',
            'General government total expenditure(% of GDP)',
            'General government revenue(% of GDP)',
            'Industry, value added (% of GDP)',
            'Access to electricity (% of population)',
            'Total Investment',
            'General government total expenditure(% of GDP)',
            'Exports of goods and services (% of GDP)',
            'Imports of goods and services (% of GDP)',
            'Unemployment, total (% of total labor force)',
            'External debt stocks, total (DOD, current US$)',
            'Military expenditure (% of GDP)',
            'Government expenditure on education, total (% of GDP)',
            'GDP growth (annual %)',
            'Inflation, GDP deflator (annual %)',
            'Total Disbursements'
        ]

        selected_options = st.multiselect('Select Data', options)

        plot_type = st.selectbox('Select Plot Type', ['Line Plot', 'Bar Plot'])

        start_year = st.slider('Select Start Year', min_value=original_start_year, max_value=original_end_year,
                               value=original_start_year, step=1)
        end_year = st.slider('Select End Year', min_value=original_start_year, max_value=original_end_year,
                             value=original_end_year, step=1)

        # Plot
        fig = go.Figure()

        for period in selected_government_periods:
            start, end = map(int, period.split('-'))
            filtered_data = df.loc[start:end]
            filtered_df = filter_data(filtered_data, selected_options, start_year, end_year)

            if plot_type == 'Line Plot':
                for col in selected_options:
                    fig.add_trace(go.Scatter(x=filtered_df.index, y=filtered_df[col], mode='lines+markers',
                                             name=f'{col} ({period})'))
            elif plot_type == 'Bar Plot':
                for col in selected_options:
                    fig.add_trace(go.Bar(x=filtered_df.index, y=filtered_df[col], name=f'{col} ({period})'))

        fig.update_layout(
            title="Government Statistics Plot",
            xaxis_title="Years",
            yaxis_title="Values",
            legend_title="Legend"
        )

        st.plotly_chart(fig)

    else:
        st.write("Invalid Page")
        return

# Sidebar navigation
st.sidebar.title('Next Page')
page = st.sidebar.radio('Go to:', ['Population', 'GDP Growth', 'Government Expenditure', 'Tax and Debt', 'Internet and Electricity', 'Resources', 'Government'])

st.sidebar.button('Generate Report')
# Render selected page
render_page(page)
