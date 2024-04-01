import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import plotly.graph_objects as go
import streamlit as st


def read_file():
    file = pd.read_csv(r"C:\Users\PMLS\Desktop\Programming for ML CAI\heart_failure_clinical_records_dataset.csv")
    df = pd.DataFrame(file)
    return df


def filter_data(df, start_age, end_age):
    # Filter the DataFrame based on the age range
    filtered_df = df[(df['age'] >= start_age) & (df['age'] <= end_age)]
    return filtered_df


def render_page(page):
    if page == 'Age wise data':
        st.header('Age wise distribution')


        # Read data
        df = read_file()
        original_start_age = df['age'].min()
        original_end_age = df['age'].max()

        # Select age range
        start_age, end_age = st.slider('Select Age Range', min_value=int(original_start_age),
                                       max_value=int(original_end_age),
                                       value=(int(original_start_age), int(original_end_age)), step=1)
        plot_type_bar_graph = st.checkbox('Bar Plot')
        plot_type_pie_graph= st.checkbox('pie Plot')
        options_1 = st.multiselect('Select case', ['Anaemia', 'Blood pressure','Smoking','diabetes','platelets'])
        # Filter data
        filtered_df = filter_data(df, start_age, end_age)
        if plot_type_bar_graph:
            if 'Anaemia' in options_1:
                anaemia_counts = filtered_df.groupby('anaemia').size()
                fig = go.Figure(go.Bar(
                    x=anaemia_counts.index,
                    y=anaemia_counts.values,
                    text=anaemia_counts.values,
                    textposition='auto',
                    marker_color=['blue', 'lightblue'],  # Blue for non-anaemia, orange for anaemia
                ))

                fig.update_layout(
                    title="Population by Anaemia Status",
                    xaxis_title="Anaemia Status",
                    yaxis_title="Number of People",
                    hovermode='x unified',  # Show hover information for all traces
                )

                st.plotly_chart(fig)
            elif 'Blood pressure' in options_1:
                high_blood_pressure_counts = filtered_df.groupby('high_blood_pressure').size()
                fig = go.Figure(go.Bar(
                    x=high_blood_pressure_counts.index,
                    y=high_blood_pressure_counts.values,
                    text=high_blood_pressure_counts.values,
                    textposition='auto',
                    marker_color=['blue', 'lightblue'],  # Blue for no high blood pressure, orange for high blood pressure
                ))

                fig.update_layout(
                    title="Population by High Blood Pressure Status",
                    xaxis_title="High Blood Pressure Status",
                    yaxis_title="Number of People",
                    hovermode='x unified',  # Show hover information for all traces
                )

                st.plotly_chart(fig)
            elif 'Smoking' in options_1:
                smoking_counts = filtered_df.groupby('smoking').size()
                # Plot
                fig = go.Figure(go.Bar(
                    x=smoking_counts.index,
                    y=smoking_counts.values,
                    text=smoking_counts.values,
                    textposition='auto',
                    marker_color=['blue', 'lightblue'],  # Blue for non-smokers, orange for smokers
                ))

                fig.update_layout(
                    title="Population by Smoking Status",
                    xaxis_title="Smoking Status",
                    yaxis_title="Number of People",
                    hovermode='x unified',  # Show hover information for all traces
                )

                st.plotly_chart(fig)

            elif 'diabetes' in options_1:
                diabetes_counts = filtered_df.groupby('diabetes').size()
                fig = go.Figure(go.Bar(
                    x=diabetes_counts.index,
                    y=diabetes_counts.values,
                    text=diabetes_counts.values,
                    textposition='auto',
                    marker_color=['blue', 'lightblue'],  # Blue for non-diabetes, orange for diabetes
                ))

                fig.update_layout(
                    title="Population by Diabetes Status",
                    xaxis_title="Diabetes Status",
                    yaxis_title="Number of People",
                    hovermode='x unified',  # Show hover information for all traces
                )

                st.plotly_chart(fig)
            elif 'platelets' in options_1:
                # Grouping by age and calculating the sum of platelet values
                platelets_sum_by_age = filtered_df.groupby('age')['platelets'].mean()

                # Creating traces for bar plot and line plot
                bar_trace = go.Bar(x=platelets_sum_by_age.index, y=platelets_sum_by_age.values, name='Bar Plot',
                                   marker=dict(color='purple'))
                line_trace = go.Scatter(x=platelets_sum_by_age.index, y=platelets_sum_by_age.values,
                                        mode='lines+markers',
                                        name='Line Plot', line=dict(color='pink'))

                # Creating the figure
                fig = go.Figure(data=[bar_trace, line_trace])

                # Setting layout
                fig.update_layout(
                    xaxis_title='Age',
                    yaxis_title='Total Platelet Values',
                    title='Total Platelet Values by Age',
                    showlegend=True
                )

                # Show the plot
                st.plotly_chart(fig)
        elif plot_type_pie_graph:
            if "Anaemia" in options_1:
                # Population by Anaemia Status
                anaemia_counts = filtered_df.groupby('anaemia').size()
                fig = go.Figure(go.Pie(
                    labels=anaemia_counts.index,
                    values=anaemia_counts.values,
                    textinfo='label+percent',
                    marker=dict(colors=['blue', 'lightblue']),  # Blue for non-anaemia, orange for anaemia
                ))

                fig.update_layout(
                    title="Population by Anaemia Status",
                )
                st.plotly_chart(fig)
            elif "Smoking" in options_1:
                # Population by Anaemia Status
                smoking_counts = filtered_df.groupby('smoking').size()
                fig = go.Figure(go.Pie(
                    labels=smoking_counts.index,
                    values=smoking_counts.values,
                    textinfo='label+percent',
                    marker=dict(colors=['blue', 'lightblue']),  # Blue for non-anaemia, orange for anaemia
                ))

                fig.update_layout(
                    title="Population by Smoking Status",
                )
                st.plotly_chart(fig)
            elif 'Blood pressure' in options_1:
                # Population by High Blood Pressure Status
                high_blood_pressure_counts = filtered_df.groupby('high_blood_pressure').size()
                fig = go.Figure(go.Pie(
                    labels=high_blood_pressure_counts.index,
                    values=high_blood_pressure_counts.values,
                    textinfo='label+percent',
                    marker=dict(colors=['blue', 'lightblue']),
                    # Blue for no high blood pressure, orange for high blood pressure
                ))

                fig.update_layout(
                    title="Population by High Blood Pressure Status",
                )
                st.plotly_chart(fig)
            elif 'diabetes' in options_1:
                # Population by Diabetes Status
                diabetes_counts = filtered_df.groupby('diabetes').size()
                fig = go.Figure(go.Pie(
                    labels=diabetes_counts.index,
                    values=diabetes_counts.values,
                    textinfo='label+percent',
                    marker=dict(colors=['blue', 'lightblue']),
                    # Blue for no diabetes, orange for diabetes
                ))

                fig.update_layout(
                    title="Population by Diabetes Status",
                )
                st.plotly_chart(fig)
            elif "platelets" in options_1:
                age_ranges = [(0, 20), (21, 40), (41, 60), (61, 80), (81, 100)]

                # Initialize counters for platelet values in each age range
                platelets_counts = [0] * len(age_ranges)

                # Iterate through data and count platelet values in each age range
                for index, (start, end) in enumerate(age_ranges):
                    platelets_counts[index] = filtered_df[(filtered_df['age'] >= start) & (filtered_df['age'] <= end)][
                        'platelets'].mean()

                # Labels for the pie chart
                labels = [f'{start}-{end}' for (start, end) in age_ranges]

                # Create the pie plot
                fig = go.Figure(data=[go.Pie(labels=labels, values=platelets_counts, hole=0.3)])

                # Set layout
                fig.update_layout(title='Average Platelet Values by Age Range')

                # Show the plot
                st.plotly_chart(fig)

    elif page == 'Gender':
        st.header('Gender wise disease distribution')

        df = read_file()
        options = st.multiselect('Select Gender', ['Male', 'Female'])
        plot_type_bar = st.checkbox('Bar Plot')
        plot_type_pie = st.checkbox('pie Plot')
        options_2 = st.multiselect('Select case', ['Anaemia', 'Smoking','Blood pressure','diabetes'])



        if 'Male' in options:
            dfm_count = df['sex'].value_counts()

            fig = go.Figure(go.Bar(
                x=dfm_count.index,
                y=dfm_count.values,
                text=dfm_count.values,
                textposition='auto',
                marker_color=['blue', 'lightblue'],  # Blue for male, orange for female
            ))

            fig.update_layout(
                title="Total Male and Female Counts",
                xaxis_title="Gender",
                yaxis_title="Number of People",
                hovermode='x unified',  # Show hover information for all traces
            )

            st.plotly_chart(fig)
            filtered_df = df[df["sex"] == 1]
            if plot_type_bar :
                if 'Anaemia' in options_2:
                    anaemia_counts = filtered_df.groupby('anaemia').size()
                    fig = go.Figure(go.Bar(
                        x=anaemia_counts.index,
                        y=anaemia_counts.values,
                        text=anaemia_counts.values,
                        textposition='auto',
                        marker_color=['blue', 'lightblue'],  # Blue for non-anaemia, orange for anaemia
                ))

                    fig.update_layout(
                        title="Population by Anaemia Status",
                        xaxis_title="Anaemia Status",
                        yaxis_title="Number of People",
                        hovermode='x unified',  # Show hover information for all traces
                )

                    st.plotly_chart(fig)
                elif 'Smoking' in options_2:
                    smoking_counts = filtered_df.groupby('smoking').size()
                    # Plot
                    fig = go.Figure(go.Bar(
                        x=smoking_counts.index,
                        y=smoking_counts.values,
                        text=smoking_counts.values,
                        textposition='auto',
                        marker_color=['blue', 'lightblue'],  # Blue for non-smokers, orange for smokers
                ))

                    fig.update_layout(
                        title="Population by Smoking Status",
                        xaxis_title="Smoking Status",
                        yaxis_title="Number of People",
                        hovermode='x unified',  # Show hover information for all traces
                )


                    st.plotly_chart(fig)
                elif 'Blood pressure'in options_2:
                    high_blood_pressure_counts = filtered_df.groupby('high_blood_pressure').size()
                    fig = go.Figure(go.Bar(
                        x=high_blood_pressure_counts.index,
                        y=high_blood_pressure_counts.values,
                        text=high_blood_pressure_counts.values,
                        textposition='auto',
                        marker_color=['blue', 'lightblue'],  # Blue for no high blood pressure, orange for high blood pressure
                    ))

                    fig.update_layout(
                        title="Population by High Blood Pressure Status",
                        xaxis_title="High Blood Pressure Status",
                        yaxis_title="Number of People",
                        hovermode='x unified',  # Show hover information for all traces
                    )

                    st.plotly_chart(fig)
                elif  'diabetes' in options_2:
                    diabetes_counts = filtered_df.groupby('diabetes').size()
                    fig = go.Figure(go.Bar(
                        x=diabetes_counts.index,
                        y=diabetes_counts.values,
                        text=diabetes_counts.values,
                        textposition='auto',
                        marker_color=['blue', 'lightblue'],  # Blue for non-diabetes, orange for diabetes
                    ))

                    fig.update_layout(
                        title="Population by Diabetes Status",
                        xaxis_title="Diabetes Status",
                        yaxis_title="Number of People",
                        hovermode='x unified',  # Show hover information for all traces
                    )

                    st.plotly_chart(fig)

            elif plot_type_pie:
                if  "Anaemia" in options_2:
                    # Population by Anaemia Status
                    anaemia_counts = filtered_df.groupby('anaemia').size()
                    fig = go.Figure(go.Pie(
                        labels=anaemia_counts.index,
                        values=anaemia_counts.values,
                        textinfo='label+percent',
                        marker=dict(colors=['blue', 'lightblue']),  # Blue for non-anaemia, orange for anaemia
                    ))

                    fig.update_layout(
                        title="Population by Anaemia Status",
                    )
                    st.plotly_chart(fig)
                elif "Smoking" in options_2:
                    # Population by Anaemia Status
                    smoking_counts = filtered_df.groupby('smoking').size()
                    fig = go.Figure(go.Pie(
                        labels=smoking_counts.index,
                        values=smoking_counts.values,
                        textinfo='label+percent',
                        marker=dict(colors=['blue', 'lightblue']),  # Blue for non-anaemia, orange for anaemia
                    ))

                    fig.update_layout(
                        title="Population by Smoking Status",
                    )
                    st.plotly_chart(fig)
                elif 'Blood pressure' in options_2:
                    # Population by High Blood Pressure Status
                    high_blood_pressure_counts = filtered_df.groupby('high_blood_pressure').size()
                    fig = go.Figure(go.Pie(
                        labels=high_blood_pressure_counts.index,
                        values=high_blood_pressure_counts.values,
                        textinfo='label+percent',
                        marker=dict(colors=['blue', 'lightblue']),
                    # Blue for no high blood pressure, orange for high blood pressure
                    ))

                    fig.update_layout(
                        title="Population by High Blood Pressure Status",
                    )
                    st.plotly_chart(fig)
                elif 'diabetes' in options_2:
                 # Population by Diabetes Status
                    diabetes_counts = filtered_df.groupby('diabetes').size()
                    fig = go.Figure(go.Pie(
                        labels=diabetes_counts.index,
                        values=diabetes_counts.values,
                        textinfo='label+percent',
                        marker=dict(colors=['blue', 'lightblue']),  # Blue for non-diabetes, orange for diabetes
                    ))

                    fig.update_layout(
                        title="Population by Diabetes Status",
                    )
                    st.plotly_chart(fig)

        elif 'Female' in options:
            dfm_count = df['sex'].value_counts()

            fig = go.Figure(go.Bar(
                x=dfm_count.index,
                y=dfm_count.values,
                text=dfm_count.values,
                textposition='auto',
                marker_color=['blue', 'lightblue'],  # Blue for male, orange for female
            ))

            fig.update_layout(
                title="Total Male and Female Counts",
                xaxis_title="Gender",
                yaxis_title="Number of People",
                hovermode='x unified',  # Show hover information for all traces
            )

            st.plotly_chart(fig)

            filtered_df = df[df["sex"] == 0]

            if plot_type_bar:
                if 'Anaemia' in options_2:
                    anaemia_counts = filtered_df.groupby('anaemia').size()
                    fig = go.Figure(go.Bar(
                        x=anaemia_counts.index,
                        y=anaemia_counts.values,
                        text=anaemia_counts.values,
                        textposition='auto',
                        marker_color=['blue', 'lightblue'],  # Blue for non-anaemia, orange for anaemia
                    ))

                    fig.update_layout(
                        title="Population by Anaemia Status",
                        xaxis_title="Anaemia Status",
                        yaxis_title="Number of People",
                        hovermode='x unified',  # Show hover information for all traces
                    )
                    st.plotly_chart(fig)
                elif 'Smoking' in options_2:
                    smoking_counts = filtered_df.groupby('smoking').size()
                    # Plot
                    fig = go.Figure(go.Bar(
                        x=smoking_counts.index,
                        y=smoking_counts.values,
                        text=smoking_counts.values,
                        textposition='auto',
                        marker_color=['blue', 'lightblue'],  # Blue for non-smokers, orange for smokers
                ))

                    fig.update_layout(
                        title="Population by Smoking Status",
                        xaxis_title="Smoking Status",
                        yaxis_title="Number of People",
                        hovermode='x unified',  # Show hover information for all traces
                )


                    st.plotly_chart(fig)
                elif 'Blood pressure' in options_2 :
                    high_blood_pressure_counts = filtered_df.groupby('high_blood_pressure').size()
                    fig = go.Figure(go.Bar(
                        x=high_blood_pressure_counts.index,
                        y=high_blood_pressure_counts.values,
                        text=high_blood_pressure_counts.values,
                        textposition='auto',
                        marker_color=['blue', 'lightblue'],
                        # Blue for no high blood pressure, orange for high blood pressure
                    ))

                    fig.update_layout(
                        title="Population by High Blood Pressure Status",
                        xaxis_title="High Blood Pressure Status",
                        yaxis_title="Number of People",
                        hovermode='x unified',  # Show hover information for all traces
                    )

                    st.plotly_chart(fig)
                elif 'diabetes' in options_2:
                    diabetes_counts = filtered_df.groupby('diabetes').size()
                    fig = go.Figure(go.Bar(
                        x=diabetes_counts.index,
                        y=diabetes_counts.values,
                        text=diabetes_counts.values,
                        textposition='auto',
                        marker_color=['blue', 'lightblue'],  # Blue for non-diabetes, orange for diabetes
                    ))

                    fig.update_layout(
                        title="Population by Diabetes Status",
                        xaxis_title="Diabetes Status",
                        yaxis_title="Number of People",
                        hovermode='x unified',  # Show hover information for all traces
                    )

                    st.plotly_chart(fig)
                elif 'platelets' in options_2:
                    # Grouping by age and calculating the sum of platelet values
                    platelets_sum_by_age = filtered_df.groupby('age')['platelets'].sum()

                    # Creating traces for bar plot and line plot
                    bar_trace = go.Bar(x=platelets_sum_by_age.index, y=platelets_sum_by_age.values, name='Bar Plot',
                                       marker=dict(color='purple'))
                    line_trace = go.Scatter(x=platelets_sum_by_age.index, y=platelets_sum_by_age.values,
                                            mode='lines+markers',
                                            name='Line Plot', line=dict(color='pink'))

                    # Creating the figure
                    fig = go.Figure(data=[bar_trace, line_trace])

                    # Setting layout
                    fig.update_layout(
                        xaxis_title='Age',
                        yaxis_title='Total Platelet Values',
                        title='Total Platelet Values by Age',
                        showlegend=True
                    )

                    # Show the plot
                    st.plotly_chart(fig)
            elif plot_type_pie:
                if "Anaemia" in options_2:
                    # Population by Anaemia Status
                    anaemia_counts = filtered_df.groupby('anaemia').size()
                    fig = go.Figure(go.Pie(
                        labels=anaemia_counts.index,
                        values=anaemia_counts.values,
                        textinfo='label+percent',
                        marker=dict(colors=['blue', 'lightblue']),  # Blue for non-anaemia, orange for anaemia
                    ))

                    fig.update_layout(
                        title="Population by Anaemia Status",
                    )
                    st.plotly_chart(fig)
                elif "Smoking" in options_2:
                    # Population by Anaemia Status
                    smoking_counts = filtered_df.groupby('smoking').size()
                    fig = go.Figure(go.Pie(
                        labels=smoking_counts.index,
                        values=smoking_counts.values,
                        textinfo='label+percent',
                        marker=dict(colors=['blue', 'lightblue']),  # Blue for non-anaemia, orange for anaemia
                    ))

                    fig.update_layout(
                        title="Population by Smoking Status",
                    )
                    st.plotly_chart(fig)
                elif 'Blood pressure' in options_2:
                    # Population by High Blood Pressure Status
                    high_blood_pressure_counts = filtered_df.groupby('high_blood_pressure').size()
                    fig = go.Figure(go.Pie(
                        labels=high_blood_pressure_counts.index,
                        values=high_blood_pressure_counts.values,
                        textinfo='label+percent',
                        marker=dict(colors=['blue', 'lightblue']),
                        # Blue for no high blood pressure, orange for high blood pressure
                    ))

                    fig.update_layout(
                        title="Population by High Blood Pressure Status",
                    )
                    st.plotly_chart(fig)
                elif 'diabetes' in options_2:
                    # Population by Diabetes Status
                    diabetes_counts = filtered_df.groupby('diabetes').size()
                    fig = go.Figure(go.Pie(
                        labels=diabetes_counts.index,
                        values=diabetes_counts.values,
                        textinfo='label+percent',
                        marker=dict(colors=['blue', 'lightblue']),  # Blue for non-diabetes, orange for diabetes
                    ))

                    fig.update_layout(
                        title="Population by Diabetes Status",
                    )
                    st.plotly_chart(fig)

    elif page == 'probability':
        st.header('Probability of having diseases ')

        options_3 = st.multiselect('Select case', ['Anaemia', 'Blood pressure','Smoking','diabetes'])
        if "Anaemia" in options_3:

            # Assuming read_file() is a function that reads data and returns a DataFrame
            df = read_file()

            # Filter DataFrame for males
            male_df = df[df["sex"] == 1]
            female_df = df[df["sex"] == 0]
            # Calculate the count of males with anemia and without anemia
            male_anemia_count = male_df[male_df['anaemia'] == 1].shape[0]
            female_anemia_count = female_df[female_df['anaemia'] == 1].shape[0]
            male_non_anemia_count = male_df[male_df['anaemia'] == 0].shape[0]
            female_non_anemia_count = female_df[female_df['anaemia'] == 0].shape[0]
            # Calculate total count of males
            total_male_count = male_df.shape[0]
            total_female_count=female_df.shape[0]

            # Calculate probabilities
            male_anemia_prob = male_anemia_count / total_male_count
            female_anemia_prob = female_anemia_count / total_female_count
            male_non_anemia_prob = male_non_anemia_count/ total_male_count
            female_non_anemia_prob = female_non_anemia_count/ total_female_count
            # Plotting
            fig = go.Figure(go.Bar(
                x=['Anaemia male','Non-anaemia male', 'Anaemia female','Non-anaemia female'],
                y=[male_anemia_prob, male_non_anemia_prob, female_anemia_prob, female_non_anemia_prob],
                textposition='auto',
                marker_color=['blue', 'lightblue','blue','lightblue'],  # Blue for anemia, orange for non-anemia
            ))

            fig.update_layout(
                title="Probability of Anaemia in Males and females",
                xaxis_title="Anaemia Status",
                yaxis_title="Probability",
                hovermode='x unified',  # Show hover information for all traces
            )

            st.plotly_chart(fig)
        elif 'Blood pressure' in options_3:
            # Assuming read_file() is a function that reads data and returns a DataFrame
            df = read_file()

            # Filter DataFrame for males
            male_df = df[df["sex"] == 1]
            female_df = df[df["sex"] == 0]
            # Calculate the count of males with anemia and without anemia
            male_bp_count = male_df[male_df['high_blood_pressure'] == 1].shape[0]
            female_bp_count = female_df[female_df['high_blood_pressure'] == 1].shape[0]
            male_non_bp_count = male_df[male_df['high_blood_pressure'] == 0].shape[0]
            female_non_bp_count = female_df[female_df['high_blood_pressure'] == 0].shape[0]
            # Calculate total count of males
            total_male_count = male_df.shape[0]
            total_female_count = female_df.shape[0]

            # Calculate probabilities
            male_bp_prob = male_bp_count / total_male_count
            female_bp_prob = female_bp_count / total_female_count
            male_non_bp_prob = male_non_bp_count / total_male_count
            female_non_bp_prob = female_non_bp_count / total_female_count
            # Plotting
            fig = go.Figure(go.Bar(
                x=['high bp male', 'Non-high bp male', 'High bp female', 'Non-high bp female'],
                y=[male_bp_prob,male_non_bp_prob, female_bp_prob,female_non_bp_prob],
                textposition='auto',
                marker_color=['blue', 'lightblue', 'blue', 'lightblue'],  # Blue for anemia, orange for non-anemia
            ))

            fig.update_layout(
                title="Probability of High blood pressure in Males and females",
                xaxis_title="Blood pressure Status",
                yaxis_title="Probability",
                hovermode='x unified',  # Show hover information for all traces
            )

            st.plotly_chart(fig)
        elif 'Smoking' in options_3:
            # Assuming read_file() is a function that reads data and returns a DataFrame
            df = read_file()

            # Filter DataFrame for males
            male_df = df[df["sex"] == 1]
            female_df = df[df["sex"] == 0]
            # Calculate the count of males with anemia and without anemia
            male_smoker_count = male_df[male_df['smoking'] == 1].shape[0]
            female_smoker_count = female_df[female_df['smoking'] == 1].shape[0]
            male_non_smoker_count = male_df[male_df['smoking'] == 0].shape[0]
            female_non_smoker_count = female_df[female_df['smoking'] == 0].shape[0]
            # Calculate total count of males
            total_male_count = male_df.shape[0]
            total_female_count = female_df.shape[0]

            # Calculate probabilities
            male_smoker_prob = male_smoker_count / total_male_count
            female_smoker_prob = female_smoker_count / total_female_count
            male_non_smoker_prob = male_non_smoker_count / total_male_count
            female_non_smoker_prob = female_non_smoker_count / total_female_count
            # Plotting
            fig = go.Figure(go.Bar(
                x=['Smoker male', 'Non-Smoker male', 'Smoker female', 'Non-Smoker female'],
                y=[male_smoker_prob,male_non_smoker_prob, female_smoker_prob, female_non_smoker_prob],
                textposition='auto',
                marker_color=['blue', 'lightblue', 'blue', 'lightblue'],  # Blue for anemia, orange for non-anemia
            ))

            fig.update_layout(
                title="Probability of Smoker in Males and females",
                xaxis_title="Smoking Status",
                yaxis_title="Probability",
                hovermode='x unified',  # Show hover information for all traces
            )

            st.plotly_chart(fig)
        elif 'diabetes' in options_3:
            # Assuming read_file() is a function that reads data and returns a DataFrame
            df = read_file()

            # Filter DataFrame for males
            male_df = df[df["sex"] == 1]
            female_df = df[df["sex"] == 0]
            # Calculate the count of males with anemia and without anemia
            male_diabetes_count = male_df[male_df['diabetes'] == 1].shape[0]
            female_diabetes_count = female_df[female_df['diabetes'] == 1].shape[0]
            male_non_diabetes_count = male_df[male_df['diabetes'] == 0].shape[0]
            female_non_diabetes_count = female_df[female_df['diabetes'] == 0].shape[0]
            # Calculate total count of males
            total_male_count = male_df.shape[0]
            total_female_count = female_df.shape[0]

            # Calculate probabilities
            male_diabetes_prob = male_diabetes_count / total_male_count
            female_diabetes_prob = female_diabetes_count / total_female_count
            male_non_diabetes_prob = male_non_diabetes_count / total_male_count
            female_non_diabetes_prob = female_non_diabetes_count / total_female_count
            # Plotting
            fig = go.Figure(go.Bar(
                x=['diabetes male', 'Non-diabetes male', 'diabetes female', 'Non-diabetes female'],
                y=[male_diabetes_prob,male_non_diabetes_prob, female_diabetes_prob, female_non_diabetes_prob],
                textposition='auto',
                marker_color=['blue', 'lightblue', 'blue', 'lightblue'],  # Blue for anemia, orange for non-anemia
            ))

            fig.update_layout(
                title="Probability of diabetes in Males and females",
                xaxis_title="diabetes Status",
                yaxis_title="Probability",
                hovermode='x unified',  # Show hover information for all traces
            )

            st.plotly_chart(fig)
    elif page == 'Death':
        st.header('Death of people having diseases ')

        df = read_file()
        option=st.multiselect("Select graph:", ['pie','bar'])
        if 'bar' in option:
            df = df[['DEATH_EVENT', 'high_blood_pressure', 'smoking', 'diabetes', 'anaemia']]

            selected_columns = st.multiselect("Select columns to filter on:", df.columns)

            # Apply filters based on user-selected columns
            filtered_df = df.copy()
            for column in selected_columns:
                value = st.selectbox(f"Select value for '{column}':", df[column].unique())
                filtered_df = filtered_df[filtered_df[column] == value]

            # Calculate total number of people matching the filtered conditions
            total_people = len(filtered_df)

            # Calculate total number of deaths among people matching the filtered conditions
            total_deaths = len(filtered_df[filtered_df['DEATH_EVENT'] == 1])

            # Create the bar graph
            fig = go.Figure(go.Bar(
                x=['Total People', 'Deaths Among Selected People'],
                y=[total_people, total_deaths],
                text=[total_people, total_deaths],
                textposition='auto',
                marker_color=['blue', 'lightblue'],  # Blue for total people, orange for deaths
            ))

            fig.update_layout(
                title="Total Number of Selected People and Deaths",
                xaxis_title="Category",
                yaxis_title="Number of People",
                hovermode='x unified',  # Show hover information for all traces
            )

            st.plotly_chart(fig)
            if total_people > 0:
                death_probability = total_deaths / total_people
            else:
                death_probability = 0
            # Create the bar graph for probability of death
            fig2 = go.Figure(go.Bar(
                x=['Probability of Death'],
                y=[death_probability],
                text=[f'{death_probability:.2%}'],
                textposition='auto',
                marker_color=['red'],  # Red color for probability of death
            ))

            fig2.update_layout(
                title="Probability of Death Among Selected People",
                xaxis_title="",
                yaxis_title="Probability",
                hovermode='x unified',  # Show hover information for all traces
            )

            st.plotly_chart(fig2)
        # df = df[['DEATH_EVENT', 'high_blood_pressure', 'smoking', 'diabetes', 'anaemia']]
        #
        # selected_columns = st.multiselect("Select columns to filter on:", df.columns)

        # Apply filters based on user-selected columns
        if 'pie' in option:
            df = df[['DEATH_EVENT', 'high_blood_pressure', 'smoking', 'diabetes', 'anaemia']]

            selected_columns = st.multiselect("Select columns to filter on:", df.columns)

            filtered_df = df.copy()
            for column in selected_columns:
                value = st.selectbox(f"Select value for '{column}':", df[column].unique())
                filtered_df = filtered_df[filtered_df[column] == value]

            # Calculate total number of people matching the filtered conditions
            total_people = len(filtered_df)

            # Calculate total number of deaths among people matching the filtered conditions
            total_deaths = len(filtered_df[filtered_df['DEATH_EVENT'] == 1])

            # Create the pie chart for total people and deaths
            fig1 = go.Figure(go.Pie(
                labels=['Total People', 'Deaths Among Selected People'],
                values=[total_people, total_deaths],
                text=[total_people, total_deaths],
                textinfo='label+percent',
                marker_colors=['blue', 'lightblue'],  # Blue for total people, orange for deaths
            ))

            fig1.update_layout(
                title="Total Number of Selected People and Deaths",
            )

            st.plotly_chart(fig1)

            # Calculate the probability of death given the filtered conditions
            if total_people > 0:
                death_probability = total_deaths / total_people
            else:
                death_probability = 0

            # Create the pie chart for probability of death
            fig2 = go.Figure(go.Pie(
                labels=['Survived', 'Died'],
                values=[total_people - total_deaths, total_deaths],
                text=[f'Survived: {total_people - total_deaths}', f'Died: {total_deaths}'],
                textinfo='label+percent',
                marker_colors=['blue', 'red'],  # Blue for survived, red for died
            ))

            fig2.update_layout(
                title="Probability of Death Among Selected People",
            )

            st.plotly_chart(fig2)
    elif page == 'death prediction':
        st.header('Check the percentage of survival')

        df=read_file()
        label_encoder = LabelEncoder()

        df['sex'] = label_encoder.fit_transform(df['sex'])
        df['smoking'] = label_encoder.fit_transform(df['smoking'])
        df['anaemia'] = label_encoder.fit_transform(df['anaemia'])
        df['high_blood_pressure'] = label_encoder.fit_transform(df['high_blood_pressure'])
        df['DEATH_EVENT'] = label_encoder.fit_transform(df['DEATH_EVENT'])

        # Split the data into features (X) and target variable (y)
        X = df[['age', 'smoking', 'anaemia', 'high_blood_pressure']]
        y = df['DEATH_EVENT']

        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train a multinomial logistic regression model
        model = LogisticRegression(multi_class='multinomial', solver='lbfgs')
        model.fit(X_train, y_train)

        # Input fields for user data
        age = st.slider("Age", min_value=0, max_value=120)
        smoking = st.selectbox("Do you smoke?", ("No", "Yes"))
        smoking = 1 if smoking == "Yes" else 0
        anaemia = st.selectbox("Do you have anemia?", ("No", "Yes"))
        anaemia = 1 if anaemia == "Yes" else 0
        high_blood_pressure = st.selectbox("Do you have high blood pressure?", ("No", "Yes"))
        high_blood_pressure = 1 if high_blood_pressure == "Yes" else 0

        # Predict the probability of death for the given input
        person_data = [[age, smoking, anaemia, high_blood_pressure]]
        death_probability = model.predict_proba(person_data)[0][1]

        st.write(f"Predicted Probability of Death: {death_probability:.2f}")

        # Visualize the prediction
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=death_probability,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Probability of Death"},
            gauge={'axis': {'range': [0, 1]},
                   'bar': {'color': "red"},
                   'steps': [
                       {'range': [0, 0.5], 'color': "lightgreen"},
                       {'range': [0.5, 0.75], 'color': "yellow"},
                       {'range': [0.75, 1], 'color': "red"}],
                   'threshold': {'line': {'color': "black", 'width': 4}, 'thickness': 0.75, 'value': 0.75}}))

        fig.update_layout(height=300)
        st.plotly_chart(fig)





st.sidebar.title("Navigation Bar")
page = st.sidebar.radio("Choose a page", ['Age wise data', 'Gender','probability','Death','death prediction'])
render_page(page)