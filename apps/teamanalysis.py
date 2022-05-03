import streamlit as st
import pandas as pd


from apps import utils

def app():
    utils.header(st)
    st.title('Team Records')    
    
    del_df = utils.return_df("data/IPL Ball-by-Ball 2008-2022.csv")
    match_df = utils.return_df("data/IPL Matches 2008-2022.csv")
    player_df = utils.return_df("data/Player Profile.csv")
    comb_df = pd.merge(del_df, match_df, on = 'id', how='left')
          
    comb_df=utils.replaceTeamNames(comb_df)

    #comb_df = comb_df[['id' , 'inning' , 'batting_team' , 'bowling_team' , 'over' , 'ball' , 'total_runs' , 'is_wicket' , 'player_dismissed' , 'venue']]
    #comb_df = comb_df.replace(np.NaN, 0)
    #st.write(comb_df.head(10))
    
    
    team_list = comb_df['team1'].unique()    
    venue_list = comb_df['venue'].unique()    
    
    team1 = st.selectbox('Select Team1',sorted(team_list))
    team2 = st.selectbox('Select Team2',sorted(team_list),index=1)
    
    DEFAULT = 'Pick a venue'
    venue = utils.selectbox_with_default(st,'Select Venue',sorted(venue_list),DEFAULT)
    
    if st.button('Show Stats'):
        if venue == DEFAULT:
            venue = None
        teamstats_df = utils.getTeamRecords(comb_df,team1,team2,venue)
        if not teamstats_df.empty: 
            hide_dataframe_row_index = """
                        <style>
                        .row_heading.level0 {display:none}
                        .blank {display:none}
                        </style>
                        """

            # Inject CSS with Markdown
            
            st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
            st.table(teamstats_df.style.format(precision=2))
        else:
            st.subheader('No Data Found!')