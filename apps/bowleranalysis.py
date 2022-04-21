import streamlit as st
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from apps import utils

def app():
    
    st.title('Bowling Records')    
    
    deliveres = pd.read_csv("C:/Personal/Tutorials/Cricket Analytics using Python/IPL Dataset and Code/IPL Ball-by-Ball 2008-2022.csv")
    matches = pd.read_csv("C:/Personal/Tutorials/Cricket Analytics using Python/IPL Dataset and Code/IPL Matches 2008-2022.csv")

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
        #df['isOne'] = df['batsman_runs'].apply(lambda x: 1 if x == 1 else 0)
        #df['isTwo'] = df['batsman_runs'].apply(lambda x: 1 if x == 2 else 0)
        #df['isThree'] = df['batsman_runs'].apply(lambda x: 1 if x == 3 else 0)
        df['isFour'] = df['batsman_runs'].apply(lambda x: 1 if x == 4 else 0)
        df['isSix'] = df['batsman_runs'].apply(lambda x: 1 if x == 6 else 0)
        df['phase'] = df['over'].apply(lambda x: utils.phase(x))
        
        runs = pd.DataFrame(df.groupby(['bowler','match_id', 'phase'])['total_runs'].sum().reset_index()).groupby(['bowler', 'phase'])['total_runs'].sum().reset_index().rename(columns={'total_runs':'runs'})
        innings = pd.DataFrame(df.groupby(['bowler', 'phase'])['match_id'].apply(lambda x: len(list(np.unique(x)))).reset_index()).rename(columns = {'match_id':'innings'})
        balls = pd.DataFrame(df.groupby(['bowler', 'phase'])['match_id'].count()).reset_index().rename(columns = {'match_id':'balls'})
        dismissals = pd.DataFrame(df.groupby(['bowler', 'phase'])['isBowlerWk'].sum()).reset_index().rename(columns = {'isBowlerWk':'dismissals'})
        
        dots = pd.DataFrame(df.groupby(['bowler', 'phase'])['isDot'].sum()).reset_index().rename(columns = {'isDot':'dots'})
        #ones = pd.DataFrame(df.groupby(['bowler', 'phase'])['isOne'].sum()).reset_index().rename(columns = {'isOne':'ones'})
        #twos = pd.DataFrame(df.groupby(['bowler', 'phase'])['isTwo'].sum()).reset_index().rename(columns = {'isTwo':'twos'})
        #threes = pd.DataFrame(df.groupby(['bowler', 'phase'])['isThree'].sum()).reset_index().rename(columns = {'isThree':'threes'})
        fours = pd.DataFrame(df.groupby(['bowler', 'phase'])['isFour'].sum()).reset_index().rename(columns = {'isFour':'fours'})
        sixes = pd.DataFrame(df.groupby(['bowler', 'phase'])['isSix'].sum()).reset_index().rename(columns = {'isSix':'sixes'})
        
        df = pd.merge(innings, runs, on = ['bowler', 'phase']).merge(balls, on = ['bowler', 'phase']).merge(dismissals, on = ['bowler', 'phase']).merge(dots, on = ['bowler', 'phase']).merge(fours, on = ['bowler', 'phase']).merge(sixes, on = ['bowler', 'phase'])
        
        # Dot Percentage = Number of dots in total deliveries
        df['Dot%'] = df.apply(lambda x: utils.get_dot_percentage(x['dots'], x['balls'])*100, axis = 1)
        
        #boundary%
        df['Boundary%'] = df.apply(lambda x: utils.boundary_per_ball(x['balls'], (x['fours'] + x['sixes']))*100, axis = 1)
        
        # Average = Runs per wicket
        df['Avg'] = df.apply(lambda x: utils.runs_per_dismissal(x['runs'], x['dismissals']), axis = 1)
        
        # StrikeRate = Balls per wicket
        df['SR'] = df.apply(lambda x: utils.balls_per_dismissal(x['balls'], x['dismissals']), axis = 1)

        # Economy = runs per over
        df['Eco'] = df.apply(lambda x: utils.runs_per_ball(x['balls'], x['runs'])*6, axis = 1)    
        
        
        return df
    
    def plotPerformanceGraph(df,selected_player):        
        
        plt.figure(figsize = (12, 4))    
        df.groupby(['batting_team'])['is_wicket'].sum().sort_values().plot(kind = 'barh', color = 'g')
              
        title = selected_player+ ' - against all teams'
        plt.title(title)
        plt.xlabel('Wickets Taken')
        plt.ylabel('Opposition Teams')
        
        for i, v in enumerate(df.groupby(['batting_team'])['is_wicket'].sum().sort_values()):
            plt.text(v+.05 , i , str(v),
                    color = 'blue', fontweight = 'bold')
        st.pyplot(plt)
    
    
    def getSpecificDataFrame(df,bowler,start_year,end_year):
        df = df[df['Season'].between(start_year, end_year)]
        df = df[df.bowler == bowler]
        return df 
    
    #st.text(df.columns)    
    #st.text(df.head())
    
       
    


    
    bowler_list = comb_df['bowler'].unique()
    season_list = comb_df['Season'].unique()
    #st.write(comb_df)
    DEFAULT = 'Pick a player'
    bowler = utils.selectbox_with_default(st,'Select bowler',sorted(bowler_list),DEFAULT)
    start_year, end_year = st.select_slider('Season',options=season_list, value=(2008, 2022))
    
    if bowler != DEFAULT:                
        comb_df['isBowlerWk'] = comb_df.apply(lambda x: utils.is_wicket(x['player_dismissed'], x['dismissal_kind']), axis = 1)
        filtered_df = getSpecificDataFrame(comb_df,bowler,start_year,end_year)
        
        if filtered_df.empty:
            st.subheader('No Data Found!')
        if not filtered_df.empty:  
            plotPerformanceGraph(filtered_df,bowler)
           # st.write(filtered_df)
            player_df = playerStatistics(filtered_df)
            player_df.drop(['bowler'], axis=1, inplace=True) 
                  
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
    