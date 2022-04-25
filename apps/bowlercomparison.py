import streamlit as st
#import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from apps import utils

def app():
    
    st.title('Bowler Matchups')    
    
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
    
          
    def playerStatistics(df):    
        
        df['isDot'] = df['batsman_runs'].apply(lambda x: 1 if x == 0 else 0)
        #df['isOne'] = df['batsman_runs'].apply(lambda x: 1 if x == 1 else 0)
        #df['isTwo'] = df['batsman_runs'].apply(lambda x: 1 if x == 2 else 0)
        #df['isThree'] = df['batsman_runs'].apply(lambda x: 1 if x == 3 else 0)
        df['isFour'] = df['batsman_runs'].apply(lambda x: 1 if x == 4 else 0)
        df['isSix'] = df['batsman_runs'].apply(lambda x: 1 if x == 6 else 0)
        
        
        runs = pd.DataFrame(df.groupby(['bowler','match_id'])['total_runs'].sum().reset_index()).groupby(['bowler'])['total_runs'].sum().reset_index().rename(columns={'total_runs':'runs'})
        innings = pd.DataFrame(df.groupby(['bowler'])['match_id'].apply(lambda x: len(list(np.unique(x)))).reset_index()).rename(columns = {'match_id':'innings'})
        balls = pd.DataFrame(df.groupby(['bowler'])['match_id'].count()).reset_index().rename(columns = {'match_id':'balls'})
        dismissals = pd.DataFrame(df.groupby(['bowler'])['isBowlerWk'].sum()).reset_index().rename(columns = {'isBowlerWk':'dismissals'})
        
        dots = pd.DataFrame(df.groupby(['bowler'])['isDot'].sum()).reset_index().rename(columns = {'isDot':'dots'})
        #ones = pd.DataFrame(df.groupby(['bowler'])['isOne'].sum()).reset_index().rename(columns = {'isOne':'ones'})
        #twos = pd.DataFrame(df.groupby(['bowler'])['isTwo'].sum()).reset_index().rename(columns = {'isTwo':'twos'})
        #threes = pd.DataFrame(df.groupby(['bowler'])['isThree'].sum()).reset_index().rename(columns = {'isThree':'threes'})
        fours = pd.DataFrame(df.groupby(['bowler'])['isFour'].sum()).reset_index().rename(columns = {'isFour':'fours'})
        sixes = pd.DataFrame(df.groupby(['bowler'])['isSix'].sum()).reset_index().rename(columns = {'isSix':'sixes'})
        
        df = pd.merge(innings, runs, on = ['bowler']).merge(balls, on = ['bowler']).merge(dismissals, on = ['bowler']).merge(dots, on = ['bowler']).merge(fours, on = ['bowler']).merge(sixes, on = ['bowler'])
        
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
    
    def plotScatterGraph(df,key1,key2,xlabel,ylabel):        
        
        plt.figure(figsize = (9, 4))
        plt.style.use('dark_background')
        plt.scatter(df[key1], df[key2],s=45)
        title = ylabel+' vs '+xlabel
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)


        annotations=list(df['bowler'])
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
       
    batting_type = comb_df['batting_style'].dropna().unique()
    
    season_list = comb_df['Season'].unique()
    #st.write(comb_df)
    
    DEFAULT = 'Pick a batting type'
    batting_type = utils.selectbox_with_default(st,'Select batting type',sorted(batting_type),DEFAULT)
    start_year, end_year = st.select_slider('Season',options=season_list, value=(2008, 2022))
    min_balls = st.number_input('Min. Balls',min_value=100,format='%d')
        
    if batting_type != DEFAULT:       
        comb_df['isBowlerWk'] = comb_df.apply(lambda x: utils.is_wicket(x['player_dismissed'], x['dismissal_kind']), axis = 1)
        filtered_df = utils.getSpecificDataFrame(comb_df,'batting_style',batting_type,start_year,end_year)      
        #st.write(filtered_df)
        #return
        if filtered_df.empty:
            st.subheader('No Data Found!')
        if not filtered_df.empty:  
            
           # st.write(filtered_df)
            player_df = playerStatistics(filtered_df)
            player_df = getMinBallsFilteredDataFrame(player_df,min_balls)
            player_df.reset_index(drop=True,inplace=True)
            topSRbowlers_df = getTopRecordsDF(player_df,'dismissals',15)
            #st.write(topSRbowlers_df)
            plotScatterGraph(topSRbowlers_df,'SR','Eco','StrikeRate','EconomyRate')
            #topbowlers_df = getTopRecordsDF(player_df,'dismissals',15)
            plotScatterGraph(topSRbowlers_df,'Boundary%','Dot%','Boundary Ball %','Dot Ball %')
            
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
            st.subheader('Bowler Comparison Stats')
            st.dataframe(player_df.sort_values('dismissals',ascending = False))
            
    