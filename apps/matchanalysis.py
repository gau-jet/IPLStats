import streamlit as st
import pandas as pd
from apps import utils


def app():
    utils.header()
    
    del_df = utils.load_deliveries_data()
    match_df = utils.load_match_data()
    player_df = utils.return_df("data/Player Profile.csv")
    comb_df=utils.return_combined_matchdf(del_df,match_df)
    comb_df.rename(columns = {'id':'match_id'}, inplace = True)
    #comb_df = comb_df[['id' , 'inning' , 'batting_team' , 'bowling_team' , 'over' , 'ball' , 'total_runs' , 'is_wicket' , 'player_dismissed' , 'venue']]
    #comb_df = comb_df.replace(np.NaN, 0)
    #st.write(comb_df.head(10))
    
    
    venue_list = utils.getVenueList(comb_df)    
    season_list = utils.getSeasonList(comb_df)#.sort_values(by=0,ascending=False) 
    
    
    st.markdown("<h3 style='text-align: center; color: white;'>Match Analysis</h3>", unsafe_allow_html=True)
    DEFAULT = 'ALL'
    year = st.selectbox('Select Season *',sorted(season_list,reverse=True))
    venue = utils.selectbox_with_default(st,'Select Venue',venue_list,DEFAULT)
    match_list = utils.getMatchList(match_df,year,venue)
    #st.write(match_list)
    match_string = st.selectbox('Select Match *',match_list)
    submitted = st.button("Show Stats")
    
    if submitted:
        filtered_df = utils.getSeasonDataFrame(comb_df,year,year)
        if venue != DEFAULT:
            filtered_df = utils.getSpecificDataFrame(filtered_df,'venue',venue) 
        
        match_id = utils.getMatchid(match_string)
                
        matchstats_df = utils.getMatchAnanlysis(comb_df,match_id)
        utils.getMatchSummaryChart(del_df,match_df,match_id)