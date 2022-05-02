import streamlit as st
#import math
import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt
from apps import utils

def app():
    utils.header(st)
    st.title('Batting Records')    
    
    del_df = utils.return_df("data/IPL Ball-by-Ball 2008-2022.csv")
    match_df = utils.return_df("data/IPL Matches 2008-2022.csv")
    
    comb_df = pd.merge(del_df, match_df, on = 'id', how='left')
    comb_df.rename(columns = {'id':'match_id'}, inplace = True)    
          
    comb_df=utils.replaceTeamNames (comb_df)

         
    batsman_list = comb_df['batsman'].unique()
    season_list = comb_df['Season'].unique()
    #st.write(comb_df)
    DEFAULT = 'Pick a player'
    batsman = utils.selectbox_with_default(st,'Select batsman',sorted(batsman_list),DEFAULT)
    start_year, end_year = st.select_slider('Season',options=season_list, value=(2008, 2022))
    
    if batsman != DEFAULT:                
        filtered_df = utils.getSpecificDataFrame(comb_df,'batsman',batsman,start_year,end_year)       
        if filtered_df.empty:
            st.subheader('No Data Found!')
        if not filtered_df.empty:  
           
            grpbyList=['bowling_team']
            title = batsman+ ' - against all teams'
            xKey = 'batsman_runs'
            xlabel = 'Runs scored'
            ylabel = 'Opposition Teams'
            
            utils.plotBarGraph(filtered_df,grpbyList,title,xKey,xlabel,ylabel)
           # st.write(filtered_df)
            
            grpbyList = ['batsman','phase']
            playerphase_df = utils.getPlayerStatistics(filtered_df,grpbyList)
            player_df = utils.getPlayerStatistics(filtered_df,['batsman'])
            
            highestscore = utils.getHighestScore(filtered_df)
            noof30s = utils.getNoofThirties(filtered_df)
            noof50s = utils.getNoofFifties(filtered_df)
            noof100s = utils.getNoofHundreds(filtered_df)
            #return
            # CSS to inject contained in a string
            hide_dataframe_row_index = """
                        <style>
                        .row_heading.level0 {display:none}
                        .blank {display:none}
                        </style>
                        """

            # Inject CSS with Markdown
            
            st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
            st.write("Innings:",player_df['Innings'][0],"| Balls:",player_df['Balls'][0],'| Runs:',player_df['Runs'][0],'| Outs:',player_df['Dismissals'][0],"| SR:",player_df['SR'][0],"| HS:",highestscore,"| 30s:",noof30s,"| 50s:",noof50s,"| 100s:",noof100s)
            st.subheader('Perfomance across different phases of a game')
           
            #st.write(playerphase_df['SR'])
            #return
            playerphase_df.drop(['batsman'], axis=1, inplace=True)
            st.table(playerphase_df.astype(str))
            st.write('* BPD -> Balls per dismissal \r\n * BPB -> Balls per boundary')
            
    