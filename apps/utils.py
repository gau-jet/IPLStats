import streamlit as st
import numpy as np 
import pandas as pd 
import math
from apps import utils

def replaceTeamNames(df):

    team_name_mappings = {'Delhi Daredevils':'Delhi Capitals','Deccan Chargers':'Sunrisers Hyderabad','Gujarat Lions':'Gujarat Titans','Kings XI Punjab':'Punjab Kings','Rising Pune Supergiants':'Rising Pune Supergiant','Pune Warriors':'Rising Pune Supergiant'} 
    
    for key, value in team_name_mappings.items():
        df['batting_team'] = df['batting_team'].str.replace(key,value)
        df['bowling_team'] = df['bowling_team'].str.replace(key,value)
    return df

def selectbox_with_default(st,text, values, default, sidebar=False):
        func = st.sidebar.selectbox if sidebar else st.selectbox
        return func(text, np.insert(np.array(values, object), 0, default))
        
def getSpecificDataFrame(df,key,value,start_year,end_year):
        df = df[df['Season'].between(start_year, end_year)]
        df = df[df[key] == value]
        return df 

def phase(over):
    if over <= 6:
        return 'Powerplay'
    elif over <= 15:
        return 'Middle'
    else:
        return 'Death'    
        
def balls_per_dismissal(balls, dismissals):
    if dismissals > 0:
        return balls/dismissals
    else:
        return balls/1 
    
def balls_per_boundary(balls, boundaries):
	if boundaries > 0:
		return balls/boundaries
	else:
		return balls/1 
        
def balls_per_dismissal(balls, dismissals):
        if dismissals > 0:
            return balls/dismissals
        else:
            return balls/1 
    
def boundary_per_ball(balls, boundaries):
    if boundaries > 0:
        return boundaries/balls
    else:
        return 1/balls 
        
def get_dot_percentage(dots, balls):
    if balls > 0:
        return dots/balls
    else:
        return 0
    
def runs_per_ball(balls, runs_conceeded):
    if balls > 0:
        return runs_conceeded/balls
    else:
        return math.inf
    
def runs_per_dismissal(runs_conceeded, dismissals):
    if dismissals > 0:
        return runs_conceeded/dismissals
    else:
        return math.inf
        
def is_wicket(player_dismissed, dismissal_kind):
    if type(player_dismissed) != str:
        return 0
    elif ~(type(player_dismissed) != str) & (dismissal_kind not in ['run out', 'retired hurt', 'obstructing the field']):
        return 1
    else:
        return 0


def getTeamBattingFirst(t1, t2, toss_winner, toss_decision): 
    if (toss_decision == 'bat'): 
        return toss_winner
    else: 
        if (toss_winner == t1): 
            return t2
        else: 
            return t1

def getTeamBattingSecond(t1, t2, toss_winner, toss_decision): 
    if (toss_decision == 'field'): 
        return toss_winner
    else: 
        if (toss_winner == t1): 
            return t2
        else: 
            return t1
def getWinPercentforaVenue(df,venue):
    
    df = df[df.venue == venue]    
    df['TossWinnerIsWinner'] = df.apply(lambda x: x['toss_winner'] == x['winner'], axis=1)    
    
    df['TeamBattingFirst'] = df.apply(lambda x: utils.getTeamBattingFirst(x['team1'] , x['team2'] , x['toss_winner'] , x['toss_decision']) , axis=1)
    df['TeamBattingSecond'] = df.apply(lambda x: utils.getTeamBattingSecond(x['team1'] , x['team2'] , x['toss_winner'] , x['toss_decision']) , axis=1)
    df['TeamBattingFirstWins'] = df.apply( lambda x : 1 if x['TeamBattingFirst'] == x['winner'] else 0 , axis=1)
    df['TeamBattingSecondWins'] = df.apply( lambda x : 1 if x['TeamBattingSecond'] == x['winner'] else 0 , axis=1)
    #st.write(df)
    WinPercentage = pd.DataFrame(100 * df.groupby('venue')['TeamBattingFirstWins'].sum() / df.groupby('venue')['TeamBattingFirstWins'].count()).reset_index()
    #st.write(WinPercentage)
    WinPercentage.columns = ['venue', 'Win% BattingFirst']
    WinPercentage['Win% BattingSecond'] = (100 - WinPercentage['Win% BattingFirst'])
   
    
    avg_run_per_match = pd.DataFrame(df.groupby(['venue']).total_runs.sum() / df.groupby('venue').id.nunique()).reset_index()
    avg_run_per_match.columns = ['venue', 'AvgRuns']
    avg_wkt_per_match = pd.DataFrame(df.groupby(['venue']).is_wicket.sum() / df.groupby('venue').id.nunique()).reset_index()
    avg_wkt_per_match.columns = ['venue', 'AvgWkts']
    final_df = pd.merge(avg_run_per_match , avg_wkt_per_match, on = 'venue')
    
    final_df = pd.merge(final_df , WinPercentage, on = 'venue')
    final_df.drop(['venue'], axis=1, inplace=True) 
    return final_df
    
def getBowlingStatsforaVenue(df,venue):
    df = df[df.venue == venue]
    new_df  = pd.DataFrame(df.groupby(['venue','bowling_style']).is_wicket.sum()).rename(columns = {'is_wicket' : 'numWickets'}).reset_index()
    
    new_df  = new_df .merge(pd.DataFrame(df.groupby(['venue','bowling_style']).ball.count()).rename(columns = {'ball' : 'numBalls'}) , on = ['venue', 'bowling_style'])
    new_df  = new_df .merge(pd.DataFrame(df.groupby(['venue','bowling_style']).total_runs.sum()).rename(columns = {'total_runs' : 'numRuns'}) , on = ['venue', 'bowling_style'])
    new_df ['BallsPerWicket'] = new_df ['numBalls'] / new_df ['numWickets']
    new_df ['RunsPerOver'] = 6 * new_df ['numRuns'] / new_df ['numBalls']
    new_df.drop(['venue'], axis=1, inplace=True)
    return new_df.sort_values(by = 'BallsPerWicket', ascending = True) 
    
def playerBattingStatistics(df,grpbyList):    
        
        df['isDot'] = df['batsman_runs'].apply(lambda x: 1 if x == 0 else 0)
        df['isOne'] = df['batsman_runs'].apply(lambda x: 1 if x == 1 else 0)
        df['isTwo'] = df['batsman_runs'].apply(lambda x: 1 if x == 2 else 0)
        df['isThree'] = df['batsman_runs'].apply(lambda x: 1 if x == 3 else 0)
        df['isFour'] = df['batsman_runs'].apply(lambda x: 1 if x == 4 else 0)
        df['isSix'] = df['batsman_runs'].apply(lambda x: 1 if x == 6 else 0)
        
      
        if ('phase' in grpbyList):
            df['phase'] = df['over'].apply(lambda x: utils.phase(x))
         
            
        runs = pd.DataFrame(df.groupby(grpbyList)['batsman_runs'].sum().reset_index()).groupby(grpbyList)['batsman_runs'].sum().reset_index().rename(columns={'batsman_runs':'runs'})
        innings = pd.DataFrame(df.groupby(grpbyList)['match_id'].apply(lambda x: len(list(np.unique(x)))).reset_index()).rename(columns = {'match_id':'innings'})
        balls = pd.DataFrame(df.groupby(grpbyList)['match_id'].count()).reset_index().rename(columns = {'match_id':'balls'})
        dismissals = pd.DataFrame(df.groupby(grpbyList)['player_dismissed'].count()).reset_index().rename(columns = {'player_dismissed':'dismissals'})
        
        dots = pd.DataFrame(df.groupby(grpbyList)['isDot'].sum()).reset_index().rename(columns = {'isDot':'dots'})
        ones = pd.DataFrame(df.groupby(grpbyList)['isOne'].sum()).reset_index().rename(columns = {'isOne':'ones'})
        twos = pd.DataFrame(df.groupby(grpbyList)['isTwo'].sum()).reset_index().rename(columns = {'isTwo':'twos'})
        threes = pd.DataFrame(df.groupby(grpbyList)['isThree'].sum()).reset_index().rename(columns = {'isThree':'threes'})
        fours = pd.DataFrame(df.groupby(grpbyList)['isFour'].sum()).reset_index().rename(columns = {'isFour':'fours'})
        sixes = pd.DataFrame(df.groupby(grpbyList)['isSix'].sum()).reset_index().rename(columns = {'isSix':'sixes'})
    
           
        df = pd.merge(innings, runs, on = grpbyList).merge(balls, on = grpbyList).merge(dismissals, on = grpbyList).merge(dots, on = grpbyList).merge(ones, on = grpbyList).merge(twos, on = grpbyList).merge(threes, on = grpbyList).merge(fours, on = grpbyList).merge(sixes, on = grpbyList)
        
        #StrikeRate
        df['SR'] = df.apply(lambda x: 100*(x['runs']/x['balls']), axis = 1)

        #runs per innings
        df['RPI'] = df.apply(lambda x: x['runs']/x['innings'], axis = 1)

        #balls per dismissals
        df['BPD'] = df.apply(lambda x: utils.balls_per_dismissal(x['balls'], x['dismissals']), axis = 1)

        #balls per boundary
        df['BPB'] = df.apply(lambda x: utils.balls_per_boundary(x['balls'], (x['fours'] + x['sixes'])), axis = 1)
        
        return df