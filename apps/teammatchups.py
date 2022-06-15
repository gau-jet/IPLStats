import streamlit as st
import pandas as pd
from apps import utils


def app():
    utils.header()
    series = utils.getSeries()
    table_header_str = f"""<h3 style='text-align: center; color: white;'>{series} - Team Matchups</h3>"""
    del_df = utils.load_deliveries_data()
    match_df = utils.load_match_data()
    player_df = utils.return_df("data/Player Profile.csv")
    comb_df=utils.return_combined_matchdf(del_df,match_df)

    #comb_df = comb_df[['id' , 'inning' , 'batting_team' , 'bowling_team' , 'over' , 'ball' , 'total_runs' , 'is_wicket' , 'player_dismissed' , 'venue']]
    #comb_df = comb_df.replace(np.NaN, 0)
    #st.write(comb_df.head(10))
    
    
    team_list = sorted(comb_df['team1'].unique())
    venue_list = utils.getVenueList(comb_df)    
    season_list = utils.getSeasonList(comb_df)
    start_season = min(season_list)
    with st.form("my_form"):
        #st.title('Team Matchups')
        st.markdown(table_header_str, unsafe_allow_html=True)
        team1 = st.selectbox('Select Team 1 *',team_list)
        team2 = st.selectbox('Select Team 2 *',team_list,index=1)
        
        DEFAULT = 'ALL'
        venue = utils.selectbox_with_default(st,'Select Venue',venue_list,DEFAULT)
        start_year, end_year = st.select_slider('Season',options=season_list, value=(start_season, 2022))
        submitted = st.form_submit_button("Show Stats")
        title_alignment= """   <style>  .css-1p05t8e {   border-width : 0    }    </style>   """
        st.markdown(title_alignment, unsafe_allow_html=True)
    if submitted:
        filtered_df = utils.getSeasonDataFrame(comb_df,start_year,end_year)
        if venue == DEFAULT:
            venue = None
        teamstats_df = utils.getTeamMatchupRecords(filtered_df,team1,team2,venue)
        if not teamstats_df.empty: 
            hide_dataframe_row_index = """
                        <style>
                        .row_heading.level0 {display:none}
                        .blank {display:none}
                        </style>
                        """

            # Inject CSS with Markdown
            st.subheader('Head to Head Stats')
            st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
            st.table(teamstats_df.style.format(precision=2))
        else:
            st.subheader('No Data Found!')