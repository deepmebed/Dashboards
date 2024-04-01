import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Read data
batting_records_path = "Batting records/"
bowling_records_path = "Bowling records/"
fielding_records_path = "Fielding records/"
team_records_path = "Team records/"

# Read datasets
highest_individual_score = pd.read_csv(batting_records_path + "Highest_individual_score_in_PSL.csv")
most_runs_by_player = pd.read_csv(batting_records_path + "Most_runs_by_a_player_in_PSL.csv")
most_sixes_in_an_innings = pd.read_csv(batting_records_path + "Most_sixes_in_an_innings_in_PSL.csv")
most_sixes_in_PSL_history = pd.read_csv(batting_records_path + "Most_sixes_in_PSL_history.csv")

best_bowling_figures_in_an_innings = pd.read_csv(bowling_records_path + "Best_bowling_figures_in_an_innings_in_PSL.csv")
most_wickets_in_PSL = pd.read_csv(bowling_records_path + "Most_wickets_in_PSL.csv")

most_catches_in_PSL = pd.read_csv(fielding_records_path + "most_catches_in_PSL.csv")
most_dismissals_by_keeper = pd.read_csv(fielding_records_path + "Most_dismissals_by_a_Wicket-keeper_in_PSL.csv")

Highest_totals_in_PSL = pd.read_csv(team_records_path + "Highest_totals_in_PSL.csv")
Lowest_totals_in_PSL = pd.read_csv(team_records_path + "Lowest_totals_in_PSL.csv")
Result_summary_of_teams_in_PSL = pd.read_csv(team_records_path + "Result_summary_of_teams_in_PSL.csv")

# Create Streamlit app
st.title("Pakistan Super League Dashboard")

# Sidebar menu
selected_record_category = st.sidebar.radio("Select Record Category", [
    'Batting Records',
    'Bowling Records',
    'Fielding Records',
    'Team Records'
])

# Filter data by match date or year
selected_year = st.sidebar.slider("Select Year", min_value=2016, max_value=2020, value=(2016, 2020))

# Apply year filter to highest_individual_score
highest_individual_score["Match Date"] = pd.to_datetime(highest_individual_score["Match Date"])
highest_individual_score = highest_individual_score[highest_individual_score["Match Date"].dt.year.isin(range(selected_year[0], selected_year[1] + 1))]

# Display records based on selected category
if selected_record_category == 'Batting Records':
    # Batting Records
    st.header("Batting Records")
    selected_batting_record = st.selectbox("Select Batting Record", [
        'Highest Individual Score',
        'Most Runs by a Player',
        'Most Sixes in an Innings',
        'Most Sixes in PSL History'
    ])
    if selected_batting_record == 'Highest Individual Score':
        # Additional visualizations selection
        selected_visualization = st.selectbox("Select Visualization", [
            'Scatter plot for Runs scored by players in PSL',
            'Histogram for Runs Scored by Players',
            'Histogram for Balls Faced by Players',
            'Bar chart for Number of Fours Hit by Players',
            'Bar chart for Number of Sixes Hit by Players',
            'Histogram for Strike Rates of Players',
            'Box plot for Strike Rate Distribution Across Teams'
        ])
        if selected_visualization == 'Bar chart for Number of Sixes Hit by Players':
            # Filter data by selected team
            selected_team = st.selectbox("Select Team", ['All'] + list(highest_individual_score['Team'].unique()))
            if selected_team != 'All':
                filtered_data = highest_individual_score[highest_individual_score['Team'] == selected_team]
            else:
                filtered_data = highest_individual_score
            
            fig_sixes = px.bar(filtered_data, x='Player', y='6s', title='Number of Sixes Hit by Players', color='Team')
            fig_sixes.update_layout(xaxis={'categoryorder':'total descending'})
            st.plotly_chart(fig_sixes)
        elif selected_visualization == 'Scatter plot for Runs scored by players in PSL':
            # Filter data by selected team
            selected_team = st.selectbox("Select Team", ['All'] + list(highest_individual_score['Team'].unique()))
            if selected_team != 'All':
                filtered_data = highest_individual_score[highest_individual_score['Team'] == selected_team]
            else:
                filtered_data = highest_individual_score
            
            # Create scatter plot
            fig = px.scatter(filtered_data, x='Player', y='Runs', color='Team', size='6s', 
                            hover_data=['Balls', '4s', '6s', 'SR'], title='Runs scored by players in PSL')
            fig.update_layout(xaxis={'categoryorder':'total descending'})
            st.plotly_chart(fig)
        elif selected_visualization == 'Histogram for Runs Scored by Players':
            # Filter data by selected team
            selected_team = st.selectbox("Select Team", ['All'] + list(highest_individual_score['Team'].unique()))
            if selected_team != 'All':
                filtered_data = highest_individual_score[highest_individual_score['Team'] == selected_team]
            else:
                filtered_data = highest_individual_score
            
            fig_runs_with_names = px.histogram(filtered_data, x='Runs', title='Distribution of Runs Scored by Players', hover_data={'Runs':True, 'Player':True}, labels={'Runs':'Runs', 'Player':'Player'})
            fig_runs_with_names.update_traces(text=filtered_data['Player'], hovertemplate='%{y} runs<br>%{text}')
            fig_runs_with_names.update_layout(xaxis_title='Runs', yaxis_title='Frequency')
            st.plotly_chart(fig_runs_with_names)
        elif selected_visualization == 'Histogram for Balls Faced by Players':
            # Filter data by selected team
            selected_team = st.selectbox("Select Team", ['All'] + list(highest_individual_score['Team'].unique()))
            if selected_team != 'All':
                filtered_data = highest_individual_score[highest_individual_score['Team'] == selected_team]
            else:
                filtered_data = highest_individual_score
            
            fig_balls_with_names = px.histogram(filtered_data, x='Balls', title='Distribution of Balls Faced by Players', histnorm='percent', labels={'Balls': 'Balls', 'Player': 'Player'})
            fig_balls_with_names.update_layout(xaxis_title='Balls', yaxis_title='Percentage of Players (%)', bargap=0.1, barmode='overlay')
            fig_balls_with_names.update_traces(text=filtered_data['Player'], textposition='inside')
            st.plotly_chart(fig_balls_with_names)
        elif selected_visualization == 'Bar chart for Number of Fours Hit by Players':
            # Filter data by selected team
            selected_team = st.selectbox("Select Team", ['All'] + list(highest_individual_score['Team'].unique()))
            if selected_team != 'All':
                filtered_data = highest_individual_score[highest_individual_score['Team'] == selected_team]
            else:
                filtered_data = highest_individual_score
            fig_fours = px.bar(filtered_data, x='Player', y='4s', title='Number of Fours Hit by Players', color='Team')
            fig_fours.update_layout(xaxis={'categoryorder':'total descending'})
            st.plotly_chart(fig_fours)
        elif selected_visualization == 'Histogram for Strike Rates of Players':
            selected_team = st.selectbox("Select Team", ['All'] + list(highest_individual_score['Team'].unique()))
            if selected_team != 'All':
                filtered_data = highest_individual_score[highest_individual_score['Team'] == selected_team]
            else:
                filtered_data = highest_individual_score
            fig_sr_hist_with_names = px.histogram(filtered_data, x='SR', title='Distribution of Strike Rates of Players', labels={'SR': 'Strike Rate', 'Player': 'Player'}, histnorm='percent')
            fig_sr_hist_with_names.update_layout(xaxis_title='Strike Rate', yaxis_title='Percentage of Players (%)', bargap=0.1, barmode='overlay')
            fig_sr_hist_with_names.update_traces(text=filtered_data['Player'], textposition='inside')
            st.plotly_chart(fig_sr_hist_with_names)
        elif selected_visualization == 'Box plot for Strike Rate Distribution Across Teams':
            selected_team = st.selectbox("Select Team", ['All'] + list(highest_individual_score['Team'].unique()))
            if selected_team != 'All':
                filtered_data = highest_individual_score[highest_individual_score['Team'] == selected_team]
            else:
                filtered_data = highest_individual_score
            
            fig_sr_box = px.box(filtered_data, x='Team', y='SR', title='Strike Rate Distribution Across Teams')
            st.plotly_chart(fig_sr_box)
    elif selected_batting_record == 'Most Runs by a Player':
        st.plotly_chart(px.bar(most_runs_by_player, x="Player", y="Runs", title="Most Runs by a Player in PSL", 
                               hover_data=['Span', 'Match', 'Inns', 'Not Outs', 'HS', 'Ave', 'BF', 'SR', '100', '50', '0', '4s']))
    elif selected_batting_record == 'Most Sixes in an Innings':
        st.plotly_chart(px.scatter(most_sixes_in_an_innings, x="Player", y="6s", color="Player", title="Most Sixes in an Innings in PSL",
                                hover_data=['Opposition','Ground','Match Date']  ))
    elif selected_batting_record == 'Most Sixes in PSL History':
        st.plotly_chart(px.bar(most_sixes_in_PSL_history, x="Player", y="6s", title="Most Sixes in PSL History",
                               hover_data=["Span","Mat","Inns","NO","Runs","HS","Ave","BF","SR","100","50","0","4s","6s"]))

elif selected_record_category == 'Bowling Records':
    # Bowling Records
    st.header("Bowling Records")
    selected_bowling_record = st.selectbox("Select Bowling Record", [
        'Best Bowling Figures in an Innings',
        'Most Wickets in PSL'
    ])
    if selected_bowling_record == 'Best Bowling Figures in an Innings':
        st.plotly_chart(px.bar(best_bowling_figures_in_an_innings, x="Player", y="Wkts", title="Best Bowling Figures in an Innings in PSL",
                               hover_data=['Overs', 'Mdns', 'Runs', 'Wkts', 'Econ', 'Team', 'Opposition', 'Ground', 'Match Date']))
    elif selected_bowling_record == 'Most Wickets in PSL':
        st.plotly_chart(px.bar(most_wickets_in_PSL, x="Player", y="Wkts", title="Most Wickets in PSL",
                               hover_data=['Span', 'Mat', 'Inns', 'Overs', 'Mdns', 'Runs', 'Wkts', 'BBI', 'Ave', 'Econ', 'SR', '4', '5']))

elif selected_record_category == 'Fielding Records':
    # Fielding Records
    st.header("Fielding Records")
    selected_fielding_record = st.selectbox("Select Fielding Record", [
        'Most Catches in PSL',
        'Most Dismissals by a Wicket-keeper in PSL'
    ])
    if selected_fielding_record == 'Most Catches in PSL':
        # Calculate catch-to-inning ratio
        most_catches_in_PSL['Catch/Inn Ratio'] = most_catches_in_PSL['Catches'] / most_catches_in_PSL['Inns']

        # Plot total catches by players with catch-to-inning ratio
        players = most_catches_in_PSL['Player']
        catches = most_catches_in_PSL['Catches']
        catch_ratio = most_catches_in_PSL['Catch/Inn Ratio']
        Span = most_catches_in_PSL["Span"]
        Mat = most_catches_in_PSL["Mat"]
        Inns = most_catches_in_PSL["Inns"]
        Max = most_catches_in_PSL["Max"]

        # Create trace
        trace = go.Bar(
            x=players,
            y=catches,
            text=[f"Ratio: {ratio:.2f}" for ratio in catch_ratio],  # Adding hover text with catch ratios
            marker=dict(color=catch_ratio, colorscale='Viridis', colorbar=dict(title='Catch/Inn Ratio')),  # Coloring based on ratio
        )

        # Layout
        layout = go.Layout(
            title="Total Catches by Players with Catch/Inn Ratio",
            xaxis=dict(title="Players"),
            yaxis=dict(title="Total Catches"),
        )

        # Create figure
        fig = go.Figure(data=[trace], layout=layout)

        # Display the figure
        st.plotly_chart(fig)

    elif selected_fielding_record == 'Most Dismissals by a Wicket-keeper in PSL':
        # Create figure
        fig = go.Figure()

        # Add bar trace
        fig.add_trace(go.Bar(
            x=most_dismissals_by_keeper["Player"],
            y=most_dismissals_by_keeper["Dis"],
            marker=dict(color='rgba(50, 171, 96, 0.6)'),
        ))

        # Update layout
        fig.update_layout(
            title='Total Dismissals (Catches and Stumpings) by Player',
            xaxis=dict(title='Player'),
            yaxis=dict(title='Total Dismissals'),
        )

        # Show plot
        st.plotly_chart(fig)

elif selected_record_category == 'Team Records':
    # Team Records
    st.header("Team Records")
    selected_team_record = st.selectbox("Select Team Record", [
        'Plot team scores over time',
        'Plot score distribution by team',
        'Plot distribution of scores across matches by team',
        'Plot matches won by each team'
    ])
    if selected_team_record == 'Plot team scores over time':
        # Plot team scores over time
        fig_scores_over_time = px.scatter(Highest_totals_in_PSL, x='Match Date', y='Score', color='Team', hover_data=['Overs', 'RR'], 
                                    title='Team Scores Over Time', labels={'Match Date': 'Date', 'Score': 'Score'})
        fig_scores_over_time.update_layout(xaxis={'title':'Date'}, yaxis={'title':'Score'})
        st.plotly_chart(fig_scores_over_time)

    elif selected_team_record == 'Plot score distribution by team':       
        # Plot score distribution by team
        fig_score_distribution = px.box(Highest_totals_in_PSL, x='Team', y='Score', title='Score Distribution by Team',
                                        labels={'Team': 'Team', 'Score': 'Score'})
        fig_score_distribution.update_layout(yaxis={'title':'Score'})
        st.plotly_chart(fig_score_distribution)

    elif selected_team_record == 'Plot distribution of scores across matches by team':
        # Plot distribution of scores across matches by team
        fig_score_distribution_across_matches = px.histogram(Lowest_totals_in_PSL, x='Score', color='Team', nbins=20, 
                                                            title='Distribution of Scores Across Matches by Team',
                                                            labels={'Score': 'Score', 'count': 'Frequency', 'Team': 'Team'})
        st.plotly_chart(fig_score_distribution_across_matches)

    elif selected_team_record == 'Plot matches won by each team':
        # Plot matches won by each team
        fig_matches_won_by_team = go.Figure(go.Bar(
            x=Result_summary_of_teams_in_PSL['Won'],
            y=Result_summary_of_teams_in_PSL['Team'],
            orientation='h',
            marker=dict(color='rgba(50, 171, 96, 0.6)'),
        ))
        fig_matches_won_by_team.update_layout(title='Matches Won by Each Team',
                                            xaxis_title='Number of Matches Won',
                                            yaxis_title='Team')
        st.plotly_chart(fig_matches_won_by_team)

