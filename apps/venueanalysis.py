import streamlit as st
#import math
import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt

from apps import utils

def app():
    utils.header(st)
    st.title('Venue Records')    
    
    del_df = utils.return_df("data/deliveries.csv")
    match_df = utils.return_df("data/matches.csv")
    player_df = utils.return_df("data/Player Profile.csv")
    comb_df = pd.merge(del_df, match_df, on = 'id', how='left')
          
    comb_df=utils.replaceTeamNames (comb_df)

    #comb_df = comb_df[['id' , 'inning' , 'batting_team' , 'bowling_team' , 'over' , 'ball' , 'total_runs' , 'is_wicket' , 'player_dismissed' , 'venue']]
    #comb_df = comb_df.replace(np.NaN, 0)
    #st.write(comb_df.head(10))
    
    DEFAULT = 'Pick a venue'
    
    venue_list = utils.getVenueList(comb_df)
    season_list = utils.getSeasonList(comb_df)
    venue = utils.selectbox_with_default(st,'Select venue',venue_list,DEFAULT)
    start_year, end_year = st.select_slider('Season',options=season_list, value=(2008, 2022))
    
    if venue != DEFAULT:
    
        filtered_df = utils.getSeasonDataFrame(comb_df,start_year,end_year)
        if not filtered_df.empty:
            InningsWinDF = utils.getPerInningsWinCount(match_df,venue)        
            VenueStatsDF = utils.getVenueStats(comb_df,venue)
                    
            final_df = pd.merge(VenueStatsDF , InningsWinDF, on = 'venue')
            final_df.drop(['venue'], axis=1, inplace=True) 
            
            # CSS to inject contained in a string
            hide_dataframe_row_index = """
                        <style>
                        .row_heading.level0 {display:none}
                        .blank {display:none}
                        </style>
                        """

            # Inject CSS with Markdown
            
            st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
            st.table(final_df.style.format(precision=2))
            
            comb_df = pd.merge(comb_df, player_df[['Player_Name','bowling_style']], left_on='bowler', right_on='Player_Name', how='left')
            comb_df.drop(['Player_Name'], axis=1, inplace=True)
            
            bowlingstats_df = utils.getBowlingStatsforaVenue(comb_df,venue)        
            st.subheader('Bowling Style Comparison')
            
            st.table(bowlingstats_df.style.format(precision=2))
        else:
                st.subheader('No Data Found!')
        