import streamlit as st
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from apps import utils

def app():
    
    st.title('Batting Records')    
    
    deliveres = pd.read_csv("data/IPL Ball-by-Ball 2008-2022.csv")
    matches = pd.read_csv("data/IPL Matches 2008-2022.csv")

    # Make a copy
    del_df = deliveres.copy()
    match_df = matches.copy()

    comb_df = pd.merge(del_df, match_df, on = 'id', how='left')
    comb_df.rename(columns = {'id':'match_id'}, inplace = True)    
    
          
    comb_df=utils.replaceTeamNames (comb_df)

    #comb_df = comb_df[['id' , 'inning' , 'batting_team' , 'bowling_team' , 'over' , 'ball' , 'total_runs' , 'is_wicket' , 'player_dismissed' , 'venue']]
    #comb_df = comb_df.replace(np.NaN, 0)
    #st.write(comb_df.head(10))
                
    
    def plotPerformanceGraph(df,selected_player):        
        
        plt.figure(figsize = (12, 4))    
        plt.style.use('dark_background')
        plt.tight_layout()
        df.groupby(['bowling_team'])['batsman_runs'].sum().sort_values().plot(kind = 'barh')
              
        title = selected_player+ ' - against all teams'
        plt.title(title)
        plt.xlabel('Runs scored')
        plt.ylabel('Opposition Teams')
        
        for i, v in enumerate(df.groupby(['bowling_team'])['batsman_runs'].sum().sort_values()):
            plt.text(v+1 , i-.15 , str(v),
                    color = 'blue', fontweight = 'bold')
        st.pyplot(plt)
    
    
    def getSpecificDataFrame(df,batsman,start_year,end_year):
        df = df[df['Season'].between(start_year, end_year)]
        df = df[df.batsman == batsman]
        return df 
    
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
            plotPerformanceGraph(filtered_df,batsman)
           # st.write(filtered_df)
            grpbyList = ['batsman','phase']
            player_df = utils.playerBattingStatistics(filtered_df,grpbyList)
            player_df.drop(['batsman'], axis=1, inplace=True)       
            # CSS to inject contained in a string
            hide_dataframe_row_index = """
                        <style>
                        .row_heading.level0 {display:none}
                        .blank {display:none}
                        </style>
                        """

            # Inject CSS with Markdown
            
            st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
            st.subheader('Perfomance across different phases of a game')
            st.table(player_df)
            st.text('* BPD -> Balls per dismissal')
            st.text('* BPB -> Balls per boundary')
    