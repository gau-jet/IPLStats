import streamlit as st
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from apps import utils

def app():
    
    st.title('Batsman Records')    
    
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
                
    def playerStatistics(df):    
        
        df['isDot'] = df['batsman_runs'].apply(lambda x: 1 if x == 0 else 0)
        df['isOne'] = df['batsman_runs'].apply(lambda x: 1 if x == 1 else 0)
        df['isTwo'] = df['batsman_runs'].apply(lambda x: 1 if x == 2 else 0)
        df['isThree'] = df['batsman_runs'].apply(lambda x: 1 if x == 3 else 0)
        df['isFour'] = df['batsman_runs'].apply(lambda x: 1 if x == 4 else 0)
        df['isSix'] = df['batsman_runs'].apply(lambda x: 1 if x == 6 else 0)
        df['phase'] = df['over'].apply(lambda x: utils.phase(x))
        
        runs = pd.DataFrame(df.groupby(['batsman','phase'])['batsman_runs'].sum().reset_index()).groupby(['batsman','phase'])['batsman_runs'].sum().reset_index().rename(columns={'batsman_runs':'runs'})
        innings = pd.DataFrame(df.groupby(['batsman','phase'])['match_id'].apply(lambda x: len(list(np.unique(x)))).reset_index()).rename(columns = {'match_id':'innings'})
        balls = pd.DataFrame(df.groupby(['batsman','phase'])['match_id'].count()).reset_index().rename(columns = {'match_id':'balls'})
        dismissals = pd.DataFrame(df.groupby(['batsman','phase'])['player_dismissed'].count()).reset_index().rename(columns = {'player_dismissed':'dismissals'})
        
        dots = pd.DataFrame(df.groupby(['batsman','phase'])['isDot'].sum()).reset_index().rename(columns = {'isDot':'dots'})
        ones = pd.DataFrame(df.groupby(['batsman','phase'])['isOne'].sum()).reset_index().rename(columns = {'isOne':'ones'})
        twos = pd.DataFrame(df.groupby(['batsman','phase'])['isTwo'].sum()).reset_index().rename(columns = {'isTwo':'twos'})
        threes = pd.DataFrame(df.groupby(['batsman','phase'])['isThree'].sum()).reset_index().rename(columns = {'isThree':'threes'})
        fours = pd.DataFrame(df.groupby(['batsman','phase'])['isFour'].sum()).reset_index().rename(columns = {'isFour':'fours'})
        sixes = pd.DataFrame(df.groupby(['batsman','phase'])['isSix'].sum()).reset_index().rename(columns = {'isSix':'sixes'})
        
               
        df = pd.merge(innings, runs, on = ['batsman','phase']).merge(balls, on = ['batsman','phase']).merge(dismissals, on = ['batsman','phase']).merge(dots, on = ['batsman','phase']).merge(ones, on = ['batsman','phase']).merge(twos, on = ['batsman','phase']).merge(threes, on = ['batsman','phase']).merge(fours, on = ['batsman','phase']).merge(sixes, on = ['batsman','phase'])
        
        #StrikeRate
        df['SR'] = df.apply(lambda x: 100*(x['runs']/x['balls']), axis = 1)

        #runs per innings
        #df['RPI'] = df.apply(lambda x: x['runs']/x['innings'], axis = 1)

        #balls per dismissals
        df['BPD'] = df.apply(lambda x: utils.balls_per_dismissal(x['balls'], x['dismissals']), axis = 1)

        #balls per boundary
        df['BPB'] = df.apply(lambda x: utils.balls_per_boundary(x['balls'], (x['fours'] + x['sixes'])), axis = 1)
        
        return df        
    
    def plotPerformanceGraph(df,selected_player):        
        
        plt.figure(figsize = (12, 4))    
        df.groupby(['bowling_team'])['batsman_runs'].sum().sort_values().plot(kind = 'barh', color = 'g')
              
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
        filtered_df = getSpecificDataFrame(comb_df,batsman,start_year,end_year)       
        if filtered_df.empty:
            st.subheader('No Data Found!')
        if not filtered_df.empty:  
            plotPerformanceGraph(filtered_df,batsman)
           # st.write(filtered_df)
            player_df = playerStatistics(filtered_df)
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
    