import streamlit as st
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from apps import utils

def app():
    
    st.title('Venue Records')    
    
    deliveres = pd.read_csv("data/IPL Ball-by-Ball 2008-2022.csv")
    matches = pd.read_csv("data/IPL Matches 2008-2022.csv")
    player = pd.read_csv("data/Player Profile.csv")
    
    # Make a copy
    del_df = deliveres.copy()
    match_df = matches.copy()
    player_df = player.copy()
    
    comb_df = pd.merge(del_df, match_df, on = 'id', how='left')
          
    comb_df=utils.replaceTeamNames (comb_df)

    #comb_df = comb_df[['id' , 'inning' , 'batting_team' , 'bowling_team' , 'over' , 'ball' , 'total_runs' , 'is_wicket' , 'player_dismissed' , 'venue']]
    #comb_df = comb_df.replace(np.NaN, 0)
    #st.write(comb_df.head(10))
    
    
    venue_list = match_df['venue'].unique()
    
    venue = st.selectbox('Select Venue',sorted(venue_list))
    
    
    if st.button('Show Stats'):
        WinPercentageDF = utils.getWinPercentforaVenue(comb_df,venue)
        # CSS to inject contained in a string
        hide_dataframe_row_index = """
                    <style>
                    .row_heading.level0 {display:none}
                    .blank {display:none}
                    </style>
                    """

        # Inject CSS with Markdown
        
        st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
        st.table(WinPercentageDF)
        
        comb_df = pd.merge(comb_df, player_df[['Player_Name','bowling_style']], left_on='bowler', right_on='Player_Name', how='left')
        comb_df.drop(['Player_Name'], axis=1, inplace=True)
        
        bowlingstats_df = utils.getBowlingStatsforaVenue(comb_df,venue)
        st.subheader('Bowling Style Comparison')
        st.table(bowlingstats_df)
     
    