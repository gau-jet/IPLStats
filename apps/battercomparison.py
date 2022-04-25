import streamlit as st
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from apps import utils

def app():
    
    st.title('Batter Matchups')    
    
    deliveres = pd.read_csv("data/IPL Ball-by-Ball 2008-2022.csv")
    matches = pd.read_csv("data/IPL Matches 2008-2022.csv")
    player = pd.read_csv("data/Player Profile.csv")
    
    # Make a copy
    del_df = deliveres.copy()
    match_df = matches.copy()
    player_df = player.copy()

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
    
               
    def plotScatterGraph(df,key1,key2,xlabel,ylabel):        
        
        plt.figure(figsize = (9, 4))
        plt.style.use('dark_background')
        plt.scatter(df[key1], df[key2]+0.10,s=45)
        title = ylabel+' vs '+xlabel
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)


        annotations=list(df['batsman'])
        #selected_players = ['A Kumble', 'SL Malinga', 'A Mishra', 'Sohail Tanvir', 'DW Steyn']

        for i, label in enumerate(annotations):
            #if label in selected_players:
            plt.annotate(label, (df[key1][i], df[key2][i]))
        
        st.pyplot(plt)
    
    
           
    def getMinBallsFilteredDataFrame(df,min_balls):        
        df = df[df.balls >= min_balls]
        return df

    def getTopRecordsDF(df,key,maxrows):        
        df = df.sort_values(key,ascending = False).head(maxrows).reset_index()
        return df        
        
    #st.text(df.columns)    
    #st.text(df.head())
       
    bowling_type = comb_df['bowling_style'].dropna().unique()
    
    season_list = comb_df['Season'].unique()
    #st.write(comb_df)
    
    DEFAULT = 'Pick a bowler type'
    bowling_type = utils.selectbox_with_default(st,'Select bowler type',sorted(bowling_type),DEFAULT)
    start_year, end_year = st.select_slider('Season',options=season_list, value=(2008, 2022))
    min_balls = st.number_input('Min. Balls',min_value=50,format='%d')
        
    if bowling_type != DEFAULT:       
        
        filtered_df = utils.getSpecificDataFrame(comb_df,'bowling_style',bowling_type,start_year,end_year)      
        #st.write(filtered_df)
        #return
        if filtered_df.empty:
            st.subheader('No Data Found!')
        if not filtered_df.empty:  
            
           # st.write(filtered_df)
            grpbyList = 'batsman'
            player_df = utils.playerBattingStatistics(filtered_df,grpbyList)
            player_df = getMinBallsFilteredDataFrame(player_df,min_balls)
            player_df.reset_index(drop=True,inplace=True)
            topSRbatsman_df = getTopRecordsDF(player_df,'runs',20)
            #st.write(topSRbatsman_df)
            #return
            plotScatterGraph(topSRbatsman_df,'SR','RPI','StrikeRate','AVG Runs')
            topbatsman_df = getTopRecordsDF(player_df,'fours',20)
            plotScatterGraph(topbatsman_df,'BPD','BPB','Balls Per Dismissal','Balls per Boundary')
            
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
            st.subheader('Batsman Comparison Stats')
            st.dataframe(player_df.sort_values('runs',ascending = False))
            
    