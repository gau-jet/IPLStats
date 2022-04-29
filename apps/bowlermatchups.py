import streamlit as st
#import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from apps import utils

def app():
    utils.header(st)
    st.title('Bowler Matchups')    
    
    del_df = utils.return_df("data/IPL Ball-by-Ball 2008-2022.csv")
    match_df = utils.return_df("data/IPL Matches 2008-2022.csv")
    player_df = utils.return_df("data/Player Profile.csv")

    merged_df = pd.merge(del_df, match_df, on = 'id', how='left')
    merged_df.rename(columns = {'id':'match_id'}, inplace = True)    
    batting_merged_df = pd.merge(merged_df, player_df[['Player_Name','batting_style']], left_on='batsman', right_on='Player_Name', how='left')
    batting_merged_df.drop(['Player_Name'], axis=1, inplace=True)       
    comb_df = pd.merge(batting_merged_df, player_df[['Player_Name','bowling_style']], left_on='bowler', right_on='Player_Name', how='left')
    comb_df.drop(['Player_Name'], axis=1, inplace=True)
    
    comb_df=utils.replaceTeamNames (comb_df)

    #comb_df = comb_df[['id' , 'inning' , 'batting_team' , 'bowling_team' , 'over' , 'ball' , 'total_runs' , 'is_wicket' , 'player_dismissed' , 'venue']]
    #comb_df = comb_df.replace(np.NaN, 0)
    #st.write(comb_df.head(10))
    
          
        
    #st.text(df.columns)    
    #st.text(df.head())
       
    batting_type = comb_df['batting_style'].dropna().unique()
    bowler_list = comb_df['bowler'].unique()
    season_list = comb_df['Season'].unique()
    #st.write(comb_df)
    
    DEFAULT_BOWLER = 'Pick a player'
    bowler = utils.selectbox_with_default(st,'Select bowler',sorted(bowler_list),DEFAULT_BOWLER)
    DEFAULT = 'Pick a batting type'
    batting_type = utils.selectbox_with_default(st,'Select batting type',sorted(batting_type),DEFAULT)
    col1, col2 = st.columns(2)
    with col1:
        start_year, end_year = st.select_slider('Season',options=season_list, value=(2008, 2022))
    with col2:    
        min_balls = st.number_input('Min. Balls',min_value=10,value=20,format='%d')
        
    if bowler != DEFAULT_BOWLER:       
        
        filtered_df = utils.getSpecificDataFrame(comb_df,'bowler',bowler,start_year,end_year)
        
        if batting_type != DEFAULT:
            filtered_df = utils.getSpecificDataFrame(filtered_df,'batting_style',batting_type,start_year,end_year)
        if not filtered_df.empty:
            filtered_df = utils.getMinBallsFilteredDataFrame(filtered_df,min_balls)      
        #st.write(filtered_df)
        #return
        if filtered_df.empty:
            st.subheader('No Data Found!')
        if not filtered_df.empty:  
            filtered_df['isBowlerWk'] = filtered_df.apply(lambda x: utils.is_wicket(x['player_dismissed'], x['dismissal_kind']), axis = 1)    
            #st.write(filtered_df)
            #return
            #player_df = utils.playerBattingComparisonStatistics(filtered_df)
            player_df = utils.getPlayerStatistics(filtered_df,['batsman'])
            player_df.reset_index(drop=True,inplace=True)
            
            sort_by_list = ['Dismissals','Runs']
            sort_asc_order = [False,False]
            topSRbowlers_df = utils.getTopRecordsDF(player_df,sort_by_list,sort_asc_order,20)
            
            #plotScatterGraph(topSRbowlers_df,'SR','Eco','StrikeRate','EconomyRate')
            #topbowlers_df = getTopRecordsDF(player_df,'dismissals',15)
            utils.plotScatterGraph(topSRbowlers_df,'Boundary%','Dot%','Boundary Ball %','Dot Ball %')
            
            #player_df.drop(['batsman'], axis=1, inplace=True)       
            # CSS to inject contained in a string
            hide_dataframe_row_index = """
                        <style>
                        .row_heading.level0 {display:none}
                        .blank {display:none}
                        </style>
                        """

            # Inject CSS with Markdown
            
            st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
            #st.subheader('Bowler Comparison Stats')
            topSRbowlers_df.drop(['index','fours','sixes'], axis=1, inplace=True)
            st.subheader('Batsman dimissed most by bowler')
            st.table(topSRbowlers_df.head(10))
            sort_by_list = ['Runs']
            sort_asc_order = [False]
            st.subheader('Players who have scored most runs against bowler')
            topRunsbatsman_df = utils.getTopRecordsDF(player_df,sort_by_list,sort_asc_order,10)
            topRunsbatsman_df.drop(['index','fours','sixes'], axis=1, inplace=True)
            st.table(topRunsbatsman_df)
    