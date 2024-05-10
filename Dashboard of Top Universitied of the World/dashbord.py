import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import plotly.express as px
import country_converter as coco
import numpy as np







def pak_uni_read_data():
    file = pd.read_excel(r"C:\Users\samsaam\Downloads\pakuni.xlsx")
    df = pd.DataFrame(file)

    return df
def pak_uni_top10():
    file = pd.read_excel(r"C:\Users\samsaam\Downloads\top10pakuni.xlsx")
    df = pd.DataFrame(file)

    return df
def pak_uni_agri():
    file = pd.read_excel(r"C:\Users\samsaam\Downloads\agriculturetop_unipak.xlsx")
    df = pd.DataFrame(file)

    return df
def pak_uni_art():
    file = pd.read_excel(r"C:\Users\samsaam\Downloads\art_unipak.xlsx")
    df = pd.DataFrame(file)

    return df
def pak_uni_bussness():
    file = pd.read_excel(r"C:\Users\samsaam\Downloads\bussness_pakuni.xlsx")
    df = pd.DataFrame(file)

    return df
def pak_uni_cs():
    file = pd.read_excel(r"C:\Users\samsaam\Downloads\cs_unipak.xlsx")
    df = pd.DataFrame(file)

    return df

def pak_uni_engen():
    file = pd.read_excel(r"C:\Users\samsaam\Downloads\engenering_pakuni.xlsx")
    df = pd.DataFrame(file)

    return df
def pak_uni_med():
    file = pd.read_excel(r"C:\Users\samsaam\Downloads\medical_unipak.xlsx")
    df = pd.DataFrame(file)

    return df
def read_file():
    # Read the data
    df = pd.read_csv(r'C:\Users\samsaam\Downloads\cwurData (1).csv')
    df = df[df['year'] == 2015]
    df.set_index('world_rank', inplace=True)

    return df


def filter_data(df, options, start_rank, end_rank):
    filtered_df = df.loc[start_rank:end_rank, options]
    return filtered_df


# Read the data
df = read_file()

# Set the index to the 'Years' column
original_start_ranking = df.index.min()
original_end_ranking = df.index.max()

def render_page(page_name):
    if page_name == 'Publication and scores':
        st.header('Publication and scores')
        options = st.multiselect('Select Data',
                                 ['score', 'publications'])
        plot_type = st.selectbox('Select Plot Type', ['Table', 'Bar Plot'])

        start_rank = st.slider('Select start ranking ', min_value=original_start_ranking, max_value=original_end_ranking,
                               value=original_start_ranking, step=1)
        end_rank = st.slider('Select End ranking', min_value=original_start_ranking, max_value=original_end_ranking,
                             value=original_end_ranking, step=1)

        filtered_df = filter_data(df, options, start_rank, end_rank)

        # Plot
        fig = go.Figure()

        if plot_type == 'Table':
            for col in options:
                fig.add_trace(go.Table(
                    header=dict(values=["Rank", col,"Institution"]),  # Column headers
                    cells=dict(values=[filtered_df.index, filtered_df[col],df['institution']])  # Data values
                ))
        elif plot_type == 'Bar Plot':
            for col in options:
                fig.add_trace(go.Bar(x=filtered_df.index, y=filtered_df[col], name=col))

        fig.update_layout(
            title="Ranking  Plot",
            xaxis_title="Ranking",
            yaxis_title="Values",
            legend_title="Legend",
            hovermode='x unified',  # Show hover information for all traces
        )

        st.plotly_chart(fig)
    elif page_name == 'year data':
        st.header('Total number of universities in country')
        dfy = pd.read_csv(r'C:\Users\samsaam\Downloads\cwurData (1).csv')

        options = st.multiselect('Select Year',
                                 ['2012', '2013','2014','2015'])
        plot_type = st.selectbox('Select Plot Type', ['Table', 'Bar Plot', 'pie plot'])

        if '2012' in options:
            dfy = dfy[dfy['year'] == 2012]

        elif '2013' in options:
            dfy = dfy[dfy['year'] == 2013]
        elif '2014' in options:
            dfy = dfy[dfy['year'] == 2014]
        elif '2015' in options:
            dfy = dfy[dfy['year'] == 2015]
        dfy.set_index('world_rank', inplace=True)

        # original_start_rankingy = dfy.index.min()
        # original_end_rankingy = dfy.index.max()
        # start_rank = st.slider('Select start ranking ', min_value=original_start_rankingy,
        #                        max_value=original_end_rankingy,
        #                        value=original_start_rankingy, step=1)
        # end_rank = st.slider('Select End ranking', min_value=original_start_rankingy, max_value=original_end_rankingy,
        #                      value=original_end_rankingy, step=1)
        # filtered_df = df.loc[(dfy.index >= start_rank) & (df.index <= end_rank), options]
        fig = go.Figure()

        if plot_type == 'Table':
            for col in options:
                fig.add_trace(go.Table(
                    header=dict(values=["Rank", "Country", "institution"]),  # Column headers
                    cells=dict(values=[dfy.index, dfy['country'], dfy['institution']])  # Data values
                ))
        elif plot_type == 'Bar Plot':
            for col in options:
                institutes_count_by_country = dfy['country'].value_counts().reset_index()
                institutes_count_by_country.columns = ['country', 'institute_count']

                fig.add_trace(
                    go.Bar(x=institutes_count_by_country['country'], y=institutes_count_by_country['institute_count'],
                           marker_color='rgb(26, 118, 255)', name='Number of Institutes'))

                # Create a DataFrame from the series


        elif plot_type == 'pie plot':
            institutes_count_by_country = dfy['country'].value_counts().reset_index()
            institutes_count_by_country.columns = ['country', 'institute_count']
            fig = go.Figure(data=[go.Pie(labels=institutes_count_by_country['country'],
                                         values=institutes_count_by_country['institute_count']
                                         )])


        fig.update_layout(
            title="Ranking by country Plot",
            xaxis_title="Ranking",
            yaxis_title="Values",
            legend_title="Legend",
            hovermode='x unified',  # Show hover information for all traces
        )

        st.plotly_chart(fig)
    elif page_name=="world map":
        st.header('location of country on world map and number of universities and average score')
        dfy = pd.read_csv(r'C:\Users\samsaam\Downloads\cwurData (1).csv')

        options = st.multiselect('Select Year',
                                 ['2012', '2013', '2014', '2015','2024'])
        # plot_type = st.selectbox('Select Plot Type', ['Table', 'Bar Plot', 'py plot'])

        if '2012' in options:
            dfy = dfy[dfy['year'] == 2012]
            scoremapolddata(dfy)
            unirankolddata(dfy)

        elif '2013' in options:
            dfy = dfy[dfy['year'] == 2013]
            scoremapolddata(dfy)
            unirankolddata(dfy)
        elif '2014' in options:
            dfy = dfy[dfy['year'] == 2014]
            scoremapolddata(dfy)
            unirankolddata(dfy)
        elif '2015' in options:
            dfy = dfy[dfy['year'] == 2015]
            scoremapolddata(dfy)
            unirankolddata(dfy)
        elif '2024' in options:
            scoremap()
            rankmap()
    elif page_name =="QS ranking":
        st.header('Rank change form 2023 to 2024')
        options = st.multiselect('Select Year',
                                 ['top country rank shif', 'top university rank shif'])
        if 'top country rank shif' in options:
            updownuni()
        elif 'top university rank shif' in options:

            updown()
            updown_Rank()
    elif page_name == 'pie chart top uni analasis':
                dfy = pd.read_csv(r'C:\Users\samsaam\Downloads\cwurData (1).csv')
                options = st.multiselect('Select Year', ['2012', '2013', '2014', '2015', '2024'])

                if '2024' in options:
                    pienew()
                else:
                    for year in options:
                        dfy_year = dfy[dfy['year'] == int(year)]
                        pieold(dfy_year)
    elif page_name == 'Find your university':
        st.header('Find university rankng in QS')
        df_all=readqs()

        # Sidebar search bar
        search_query = st.sidebar.text_input('Search by name', '')
        fig = go.Figure()
        # Filter data based on search query
        filtered_df = df_all[df_all['Institution Name'].str.contains(search_query, case=False)]
        fig.add_trace(go.Table(
            header=dict(values=["2024 Rank",'2023 Rank', "International Research Network Rank", "Institution Name",'Country']),  # Column headers
            cells=dict(values=[filtered_df['2024 RANK'],filtered_df['2023 RANK'] ,filtered_df['International Research Network Rank'], filtered_df['Institution Name'],filtered_df['Country']])  # Data values
        ))
        st.plotly_chart(fig)
    elif page_name == 'Find pakistan university':
        st.header('Pakistan university data and best faculty')
        options = st.multiselect('Select Data',
                                 ['top 10', 'Medical','Engineering and technology','Computer science','Agriculture and veterinary science',
                                  'Business','arts'])
        if "top 10" in options:
            dfp=pak_uni_top10()
            fig = go.Figure()
            fig.add_trace(go.Table(
                header=dict(values=["Rank", "Institution Name",
                                    'Score']),  # Column headers
                cells=dict(values=[dfp['Ranking'],
                                   dfp['University'],
                                   dfp['Score']])  # Data values
            ))
            st.plotly_chart(fig)

        elif 'Medical' in options:
            dfp = pak_uni_med()
            fig = go.Figure()
            fig.add_trace(go.Table(
                header=dict(values=["Rank", "Institution Name",
                                    'Score']),  # Column headers
                cells=dict(values=[dfp['Ranking'],
                                   dfp['University'],
                                   dfp['Score']])  # Data values
            ))
            st.plotly_chart(fig)

        elif 'Engineering and technology' in options:
            dfp = pak_uni_engen()
            fig = go.Figure()
            fig.add_trace(go.Table(
                header=dict(values=["Rank", "Institution Name",
                                    'Score']),  # Column headers
                cells=dict(values=[dfp['Ranking'],
                                   dfp['University'],
                                   dfp['Score']])  # Data values
            ))
            st.plotly_chart(fig)

        elif  'Computer science' in options:
            dfp = pak_uni_cs()
            fig = go.Figure()
            fig.add_trace(go.Table(
                header=dict(values=["Rank", "Institution Name"
                                    ]),  # Column headers
                cells=dict(values=[dfp['Ranking'],
                                   dfp['University']
                                   ])  # Data values
            ))
            st.plotly_chart(fig)

        elif 'Agriculture and veterinary science' in options:
            dfp = pak_uni_agri()
            fig = go.Figure()
            fig.add_trace(go.Table(
                header=dict(values=["Rank", "Institution Name",
                                    'Score']),  # Column headers
                cells=dict(values=[dfp['Ranking'],
                                   dfp['University'],
                                   dfp['Score']])  # Data values
            ))
            st.plotly_chart(fig)

        elif 'Business' in options:
            dfp = pak_uni_bussness()
            fig = go.Figure()
            fig.add_trace(go.Table(
                header=dict(values=["Rank", "Institution Name"
                                    ]),  # Column headers
                cells=dict(values=[dfp['Ranking'],
                                   dfp['University']
                                   ])  # Data values
            ))
            st.plotly_chart(fig)

        elif 'arts' in options:
            dfp = pak_uni_art()
            fig = go.Figure()
            fig.add_trace(go.Table(
                header=dict(values=["Rank", "Institution Name",
                                    'Score']),  # Column headers
                cells=dict(values=[dfp['Ranking'],
                                   dfp['University'],
                                   dfp['Score']])  # Data values
            ))
            st.plotly_chart(fig)



    else:
        st.write("Invalid Page")

def readqs():
    file = pd.read_csv( r"C:\Users\samsaam\Downloads\2024 QS World University Rankings 1.1 (For qs.com).csv")
    df=pd.DataFrame(file)
    return df
def updown():
    df=readqs()
    df=clean_data(df)
    top20_df = df.iloc[:21]
    top20_rank_change = top20_df.groupby('Institution Name')['Rank Change'].mean().sort_values(ascending=True)

    updown = px.bar(x=top20_rank_change.index, y=top20_rank_change.values,
                 text=np.round(top20_rank_change.values),
                 color=top20_rank_change.values,
                 color_continuous_scale='YlOrRd')
    fig = go.Figure(data=updown.data)

    fig.update_layout(
        title="Top 20 university rank shift from 2023 to 2024",
        xaxis_title="Country",
        yaxis_title="Publication Count",
        legend_title="Country",
        hovermode='x unified'  # Show hover information for all traces
    )
    st.plotly_chart(fig)
def updown_Rank():
    df = readqs()  # Assuming this function reads the dataset
    df = clean_data(df)  # Assuming this function cleans the dataset

    search_query = st.sidebar.text_input('Search by name', '')
    if search_query!="":

    # Filter data based on search query
        filtered_df = df[df['Institution Name'].str.contains(search_query, case=False)]
        top20_rank_change = filtered_df.groupby('Institution Name')['Rank Change'].mean().sort_values(ascending=True)

    # Convert the series to DataFrame
        top20_rank_change_df = top20_rank_change.reset_index(name='Rank Change')

        fig = px.bar(top20_rank_change_df, x='Institution Name', y='Rank Change',
                 text=np.round(top20_rank_change_df['Rank Change']),
                 color='Rank Change',
                 color_continuous_scale='YlOrRd')

        fig.update_layout(
        title=f"Rank shift of {search_query}",
        xaxis_title="Institution",
        yaxis_title="Rank shift",
        legend_title="Rank shift",
        hovermode='x unified'  # Show hover information for all traces
        )
        st.plotly_chart(fig)

def clean_data(df):
        # drop first row of data
        df.drop(0, axis=0, inplace=True)

        # drop any NaN vaules and NaN Overall SCORE
        df = df.dropna()
        df = df.loc[df['Overall SCORE'] != '-']

        # concat rank, categorical, and score columns
        rank_df = df[['2024 RANK', '2023 RANK']]
        cat_df = df[['Institution Name', 'Country', 'SIZE', 'FOCUS', 'RES.', 'AGE']]
        score_cols = [col for col in df.columns if 'score' in col.lower()]
        score_df = df[score_cols]
        df = pd.concat([rank_df, cat_df, score_df], axis=1)

        # convert object types to int types
        df = convert_to_int(df)
        # create rank change column
        df['Rank Change'] = df['2023 RANK'] - df['2024 RANK']

        # times -1 value to RANK 2023 and RANK 2024 as lower ranking = better
        df['2023 RANK'] = -1 * df['2023 RANK']
        df['2024 RANK'] = -1 * df['2024 RANK']

        return df
categorical_cols = ['Institution Name', 'Country', 'SIZE', 'FOCUS', 'RES.']
def convert_to_int(df):
    for col in df.columns:
        if (col not in (categorical_cols)):
            df[col] = df[col].str.extract('(\d+)').astype(int)
    return df
def updownuni():
    df = readqs()
    df = clean_data(df)
    rank_change_down = df.groupby('Country')['Rank Change'].mean().sort_values(ascending=False)[:10]
    rank_change_up = df.groupby('Country')['Rank Change'].mean().sort_values(ascending=False)[-10:]
    rank_change = pd.concat([rank_change_down, rank_change_up])

    updown = px.bar(x=rank_change.index, y=rank_change.values,
                 text=np.round(rank_change.values),
                 color=rank_change.values,
                 color_continuous_scale='YlOrRd')
    fig = go.Figure(data=updown.data)
    fig.update_layout(
        title_text='Top 10 Countries Rank Up & Down From 2023 to 2024',
        template='simple_white',
        xaxis=dict(
            title='Country',
            titlefont_size=16
        ),
        yaxis=dict(
            title='Average Rank Change',
            titlefont_size=16
        ),
    )

    st.plotly_chart(fig)

def scoremap():
    df = readqs()
    df = clean_data(df)
    score_by_country = df.groupby('Country')['Overall SCORE'].mean()

    score_by_country.index = coco.convert(score_by_country.index, to='ISO3')
    scoremap = px.choropleth(locations=score_by_country.index,
                    color=score_by_country.values,
                    color_continuous_scale=px.colors.sequential.YlOrRd,
                    template='plotly_white',
                    title='University Average Overall Score Distributino')

    fig = go.Figure(data=scoremap.data)
    fig.update_layout(title_text='University Average Overall Score Distribution')  # Add title to layout
    st.plotly_chart(fig)

def rankmap():
    df = readqs()
    df = clean_data(df)

    country_codes = coco.convert(df['Country'], to='ISO3')
    country_codes = pd.Series(country_codes)
    university_location = country_codes.value_counts()
    fig = px.choropleth(locations=university_location.index,
                        color=university_location.values,
                        color_continuous_scale='YlOrRd',
                        template='plotly_white',
                        title='Number of Universities in country Location Distribution Map')
    fig = go.Figure(fig.data)
    fig.update_layout(title_text='University rank of country')  # Add title to layout
    st.plotly_chart(fig)
def scoremapolddata(df):
    # dfy = pd.read_csv(r'C:\Users\samsaam\Downloads\cwurData (1).csv')

    score_by_country = df.groupby('country')['score'].mean()

    score_by_country.index = coco.convert(score_by_country.index, to='ISO3')
    scoremap = px.choropleth(locations=score_by_country.index,
                    color=score_by_country.values,
                    color_continuous_scale=px.colors.sequential.YlOrRd,
                    template='plotly_white',
                    title='University Average Overall Score Distribution')

    fig = go.Figure(data=scoremap.data)
    fig.update_layout(title_text='University Average Overall Score Distribution')  # Add title to layout
    st.plotly_chart(fig)



def publicationmapolddata(df):
    # dfy = pd.read_csv(r'C:\Users\samsaam\Downloads\cwurData (1).csv')

    score_by_country = df.groupby('country')['publications'].mean()

    score_by_country.index = coco.convert(score_by_country.index, to='ISO3')
    scoremap = px.choropleth(locations=score_by_country.index,
                             color=score_by_country.values,
                             color_continuous_scale=px.colors.sequential.YlOrRd,
                             template='plotly_white',
                             title='University Average Overall Score Distributino')

    fig = go.Figure(data=updown.data)
    st.plotly_chart(fig)
def unirankolddata(dfy):
    country_codes = coco.convert(dfy['country'], to='ISO3')
    country_codes = pd.Series(country_codes)
    university_location = country_codes.value_counts()
    fig = px.choropleth(locations=university_location.index,
                        color=university_location.values,
                        color_continuous_scale=px.colors.sequential.YlOrRd,
                        template='plotly_white',
                        title='University rank Location Distribution Map')
    institutes_count_by_country = dfy['country'].value_counts()
    fig.update_layout(
        title="Ranked country  Plot",
        xaxis_title="Ranking",
        yaxis_title="Values",
        legend_title="Legend",
        hovermode='x unified',  # Show hover information for all traces
    )

    st.plotly_chart(fig)
def pieold(dfy):
    institutes_count_by_country = dfy['country'].value_counts()
    # Create a DataFrame from the series
    institutes_count_df = institutes_count_by_country.reset_index()
    institutes_count_df.columns = ['country', 'institute_count']
    top_countries_df = institutes_count_df.nlargest(3, 'institute_count')
    other_countries_df = institutes_count_df.nsmallest(len(institutes_count_df) - 3, 'institute_count')
    other_countries_total = other_countries_df['institute_count'].sum()

    # Add an "Other" row
    new_row = {'country': 'Other', 'institute_count': other_countries_total}  
    top_countries_df = pd.concat([top_countries_df, pd.DataFrame([new_row])], ignore_index=True)

    # Create the pie chart using Plotly Express
    circular_fig = px.pie(top_countries_df, values='institute_count', names='country',
                          title='Number of Institutes by Country')

    # Convert the Plotly Express figure to a Plotly graph object
    fig = go.Figure(data=[go.Pie(labels=top_countries_df['country'],
                                 values=top_countries_df['institute_count']
                                 )])

    circular_fig.update_layout(
        autosize=False,
        width=700,  # Set the desired width
        height=500  # Set the desired height
    )
    fig.update_layout(
        title="Ranking Plot",
        xaxis_title="Ranking",
        yaxis_title="Values",
        legend_title="Legend",
        hovermode='x unified',  # Show hover information for all traces
    )

    st.plotly_chart(fig)

    # Pie chart for publication count
    publications_count_by_country = dfy.groupby('country')['publications'].sum().reset_index()
    publications_count_by_country.columns = ['country', 'publication_count']
    top_countries_df = publications_count_by_country.nlargest(3, 'publication_count')
    other_countries_df = publications_count_by_country.nsmallest(len(publications_count_by_country) - 3,
                                                                 'publication_count')
    other_countries_total = other_countries_df['publication_count'].sum()
    new_row = {'country': 'Other', 'publication_count': other_countries_total}
    top_countries_df = pd.concat([top_countries_df, pd.DataFrame([new_row])], ignore_index=True)

    # Create the pie chart using Plotly Express
    circular_fig = px.pie(top_countries_df, values='publication_count', names='country',
                          title='Number of Publications by Country')

    # Convert the Plotly Express figure to a Plotly graph object
    fig = go.Figure(data=circular_fig.data)

    fig.update_layout(
        title="Number of Publications by Country",
        xaxis_title="Country",
        yaxis_title="Publication Count",
        legend_title="Country",
        hovermode='x unified'  # Show hover information for all traces
    )

    st.plotly_chart(fig)

    # Pie chart for score count
    score_count_by_country = dfy.groupby('country')['score'].sum().reset_index()
    score_count_by_country.columns = ['country', 'score_count']
    top_countries_df = score_count_by_country.nlargest(3, 'score_count')
    other_countries_df = score_count_by_country.nsmallest(len(score_count_by_country) - 3,
                                                          'score_count')
    other_countries_total = other_countries_df['score_count'].sum()
    new_row = {'country': 'Other', 'score_count': other_countries_total}
    top_countries_df = pd.concat([top_countries_df, pd.DataFrame([new_row])], ignore_index=True)

    # Create the pie chart using Plotly Express
    circular_fig = px.pie(top_countries_df, values='score_count', names='country',
                          title='Number of Score of Universities by Country')

    # Convert the Plotly Express figure to a Plotly graph object
    fig = go.Figure(data=circular_fig.data)

    fig.update_layout(
        title="Number of Score of Universities by Country",
        xaxis_title="Country",
        yaxis_title="Score Count",
        legend_title="Country",
        hovermode='x unified'  # Show hover information for all traces
    )

    st.plotly_chart(fig)


def pienew():
    dfy = readqs()
    dfy = clean_data(dfy)

    # Pie chart for institute count
    institutes_count_by_country = dfy['Country'].value_counts()
    institutes_count_df = institutes_count_by_country.reset_index()
    institutes_count_df.columns = ['Country', 'institute_count']
    top_countries_df = institutes_count_df.nlargest(3, 'institute_count')
    other_countries_df = institutes_count_df.nsmallest(len(institutes_count_df) - 3, 'institute_count')
    other_countries_total = other_countries_df['institute_count'].sum()
    new_row = {'Country': 'Other', 'institute_count': other_countries_total}
    top_countries_df = pd.concat([top_countries_df, pd.DataFrame([new_row])], ignore_index=True)

    st.subheader("Number of Institutes by Country")
    circular_fig = px.pie(top_countries_df, values='institute_count', names='Country')
    fig = go.Figure(data=[go.Pie(labels=top_countries_df['Country'], values=top_countries_df['institute_count'])])
    st.plotly_chart(fig)

    # Pie chart for Academic Reputation Score
    publications_count_by_country = dfy.groupby('Country')['Academic Reputation Score'].sum().reset_index()
    publications_count_by_country.columns = ['Country', 'Academic Reputation Score_count']
    top_countries_df = publications_count_by_country.nlargest(3, 'Academic Reputation Score_count')
    other_countries_df = publications_count_by_country.nsmallest(len(publications_count_by_country) - 3,
                                                                 'Academic Reputation Score_count')
    other_countries_total = other_countries_df['Academic Reputation Score_count'].sum()
    new_row = {'Country': 'Other', 'Academic Reputation Score_count': other_countries_total}
    top_countries_df = pd.concat([top_countries_df, pd.DataFrame([new_row])], ignore_index=True)

    st.subheader("Academic Reputation Score")
    circular_fig = px.pie(top_countries_df, values='Academic Reputation Score_count', names='Country')
    fig = go.Figure(data=circular_fig.data)
    st.plotly_chart(fig)

    # Pie chart for Overall SCORE
    publications_count_by_country = dfy.groupby('Country')['Overall SCORE'].sum().reset_index()
    publications_count_by_country.columns = ['Country', 'Overall SCORE_count']
    top_countries_df = publications_count_by_country.nlargest(3, 'Overall SCORE_count')
    other_countries_df = publications_count_by_country.nsmallest(len(publications_count_by_country) - 3,
                                                                 'Overall SCORE_count')
    other_countries_total = other_countries_df['Overall SCORE_count'].sum()
    new_row = {'Country': 'Other', 'Overall SCORE_count': other_countries_total}
    top_countries_df = pd.concat([top_countries_df, pd.DataFrame([new_row])], ignore_index=True)

    st.subheader("Overall SCORE")
    circular_fig = px.pie(top_countries_df, values='Overall SCORE_count', names='Country')
    fig = go.Figure(data=circular_fig.data)
    st.plotly_chart(fig)


# Display the page
page = st.sidebar.radio('Go to:', [ 'Publication and scores', 'year data',"world map", "QS ranking", 'pie chart top uni analasis','Find your university','Find pakistan university'])

render_page(page)
