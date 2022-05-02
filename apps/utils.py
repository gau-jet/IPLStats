import streamlit as st
import numpy as np 
import pandas as pd 
import math
import matplotlib.pyplot as plt
from apps import utils

def header(st):
    snippet = """
    <div style="display: flex; justify-content: space-between">
        <div>🡠 Check the sidebar for more apps</div>        
    </div>
    """
    st.markdown(snippet, unsafe_allow_html=True)

@st.cache(suppress_st_warning=True,ttl=3600,show_spinner=True)    
def return_df(f):    
    df = pd.read_csv(f)
    return df.copy()    

def replaceTeamNames(df):

    team_name_mappings = {'Delhi Daredevils':'Delhi Capitals','Deccan Chargers':'Sunrisers Hyderabad','Gujarat Lions':'Gujarat Titans','Kings XI Punjab':'Punjab Kings','Rising Pune Supergiants':'Rising Pune Supergiant','Pune Warriors':'Rising Pune Supergiant'} 
    
    for key, value in team_name_mappings.items():
        df['batting_team'] = df['batting_team'].str.replace(key,value)
        df['bowling_team'] = df['bowling_team'].str.replace(key,value)
        df['team1'] = df['team1'].str.replace(key,value)
        df['team2'] = df['team2'].str.replace(key,value)
        df['toss_winner'] = df['toss_winner'].str.replace(key,value)
        df['winner'] = df['winner'].str.replace(key,value)
    return df

def selectbox_with_default(st,text, values, default, sidebar=False):
        func = st.sidebar.selectbox if sidebar else st.selectbox
        return func(text, np.insert(np.array(values, object), 0, default))
        
def getSpecificDataFrame(df,key,value,start_year=None,end_year=None):
        if start_year:
            df = df[df['Season'].between(start_year, end_year)]
        df = df[df[key] == value]
        return df 

def getTopRecordsDF(df,key,order,maxrows):        
        df = df.sort_values(by=key,ascending = order).head(maxrows).reset_index()
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
        return math.inf 
    
def balls_per_boundary(balls, boundaries):
	if boundaries > 0:
		return balls/boundaries
	else:
		return math.inf
        
def boundary_per_ball(balls, boundaries):
    if boundaries > 0:
        return boundaries/balls
    else:
        #return 1/balls 
        return 0
        
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

def getMinBallsFilteredDataFrame(df,min_balls):        
        if (df.shape[0] >= min_balls):
            return df
        else:    
            return pd.DataFrame()            
            
def getMinBallsFilteredDF(df,min_balls):        
        df = df[df.Balls >= min_balls]
        return df
            
def getVenueStats(df,venue):
    
    df = df[df.venue == venue]    
    df['TossWinnerIsWinner'] = df.apply(lambda x: x['toss_winner'] == x['winner'], axis=1)    
    
    df['TeamBattingFirst'] = df.apply(lambda x: utils.getTeamBattingFirst(x['team1'] , x['team2'] , x['toss_winner'] , x['toss_decision']) , axis=1)
    df['TeamBattingSecond'] = df.apply(lambda x: utils.getTeamBattingSecond(x['team1'] , x['team2'] , x['toss_winner'] , x['toss_decision']) , axis=1)
    
    df['TeamBattingFirstWins'] = df.apply( lambda x : 1 if x['TeamBattingFirst'] == x['winner']  else 0 , axis=1)    
    df['TeamBattingSecondWins'] = df.apply( lambda x : 1 if x['TeamBattingSecond'] == x['winner'] else 0 , axis=1)    
    
    
    WinPercentage = pd.DataFrame(100 * df.groupby('venue')['TeamBattingFirstWins'].sum() / df.groupby('venue')['TeamBattingFirstWins'].count()).reset_index()
    #st.write(WinPercentage)
    WinPercentage.columns = ['venue', 'BattingFirst Win%']
    WinPercentage['BattingSecond Win%'] = (round(100 - WinPercentage['BattingFirst Win%'],2))
    WinPercentage['BattingFirst Win%'] = (round(WinPercentage['BattingFirst Win%'],2))
    
    avg_run_per_match = pd.DataFrame(df.groupby(['venue','inning']).total_runs.sum() / df.groupby('venue').id.nunique()).reset_index()
    avg_run_per_match.columns = ['venue', 'Inning','AvgRuns']
    avg_wkt_per_match = pd.DataFrame(df.groupby(['venue','inning']).is_wicket.sum() / df.groupby('venue').id.nunique()).reset_index()
    avg_wkt_per_match.columns = ['venue','Inning', 'AvgWkts']
    
    avg_run_per_match.drop(['venue'], axis=1, inplace=True) 
    avg_run_per_match_transposed = avg_run_per_match.T
    avg_wk_per_match_transposed = avg_wkt_per_match.T
    
    
    avg_run_per_match_transposed[0]['AvgRuns'] = (round(avg_run_per_match_transposed[0]['AvgRuns'],2))
    avg_run_per_match_transposed[1]['AvgRuns'] = (round(avg_run_per_match_transposed[1]['AvgRuns'],2))
    avg_wk_per_match_transposed[0]['AvgWkts'] = (round(avg_wk_per_match_transposed[0]['AvgWkts'],2))
    avg_wk_per_match_transposed[1]['AvgWkts'] = (round(avg_wk_per_match_transposed[1]['AvgWkts'],2))
    
   
    matches = pd.DataFrame(df.groupby('venue')['id'].apply(lambda x: len(list(np.unique(x)))).reset_index()).rename(columns = {'id':'NoofMatches'})
    matches.drop(['venue'], axis=1, inplace=True) 
    
    innings_stats_df = {
        'venue':[venue],
        'Matches': matches['NoofMatches'][0],
        'Avg Runs - 1st Innings': [avg_run_per_match_transposed[0]['AvgRuns']],
        'Avg Runs - 2nd Innings': [avg_run_per_match_transposed[1]['AvgRuns']],
        'Avg Wickets - 1st Innings': [avg_wk_per_match_transposed[0]['AvgWkts']],
        'Avg Wickets - 2nd Innings': [avg_wk_per_match_transposed[1]['AvgWkts']]
      }
      
    final_df = pd.DataFrame(data=innings_stats_df)
    
    #final_df = pd.merge(avg_run_per_match , avg_wkt_per_match, on = 'venue')
    
    final_df = pd.merge(final_df , WinPercentage, on = 'venue')
    final_df.drop(['venue'], axis=1, inplace=True) 
    
    return final_df

def getBowlingStyleWiseStats(df):
    new_df  = pd.DataFrame(df.groupby(['venue','bowling_style']).ball.count()).rename(columns = {'ball' : 'Balls'}).reset_index()
    new_df  = new_df .merge(pd.DataFrame(df.groupby(['venue','bowling_style']).total_runs.sum()).rename(columns = {'total_runs' : 'Runs'}) , on = ['venue', 'bowling_style'])
    new_df  = new_df .merge(pd.DataFrame(df.groupby(['venue','bowling_style']).is_wicket.sum()).rename(columns = {'is_wicket' : 'Wickets'}), on = ['venue', 'bowling_style'])
    new_df ['BallsPerWicket'] = (round(new_df ['Balls'] / new_df ['Wickets'],2))
    new_df ['RunsPerOver'] = (round(6 * new_df ['Runs'] / new_df ['Balls'],2))
    new_df.drop(['venue'], axis=1, inplace=True)
    new_df.rename(columns = {'bowling_style':'Bowling Style'}, inplace = True)
    return new_df
    
    
def getBowlingStatsforaVenue(df,venue):
    df = df[df.venue == venue]
    new_df = utils.getBowlingStyleWiseStats(df)    
    return new_df.sort_values(by = 'BallsPerWicket', ascending = True) 

def getHighestScore(df):
    runs = pd.DataFrame(df.groupby(['batsman','match_id'])['batsman_runs'].sum().reset_index()).groupby(['batsman','match_id'])['batsman_runs'].sum().reset_index().rename(columns={'batsman_runs':'Match_Runs'})
    return (runs.Match_Runs.max())

def getNoofThirties(df):
    
    runs = pd.DataFrame(df.groupby(['match_id'])['batsman_runs'].sum().reset_index()).rename(columns={'batsman_runs':'Match_Runs'})
    noofthirties= runs['Match_Runs'].apply(lambda x: 1 if x >=30 else 0).sum()
    return (noofthirties)    
    
def getNoofFifties(df):
    
    runs = pd.DataFrame(df.groupby(['match_id'])['batsman_runs'].sum().reset_index()).rename(columns={'batsman_runs':'Match_Runs'})
    nooffifties = runs['Match_Runs'].apply(lambda x: 1 if x >=50 and x <100 else 0).sum()    
    return (nooffifties)
    
def getNoof4Wickets(df):
    
    df = df[~df.dismissal_kind.isin(['run out', 'retired hurt', 'obstructing the field','NA'])]
    #df = df[df.venue == venue]     
    dismissals = pd.DataFrame(df.groupby(['Season','match_id'])['player_dismissed'].count()).reset_index().rename(columns = {'player_dismissed':'Dismissals'})
       
    noof4wks = dismissals['Dismissals'].apply(lambda x: 1 if x == 4 else 0).sum()
    return (noof4wks)
    
def getNoof5Wickets(df):
    df = df[~df.dismissal_kind.isin(['run out', 'retired hurt', 'obstructing the field','NA'])]
    dismissals = pd.DataFrame(df.groupby(['match_id'])['player_dismissed'].count()).reset_index().rename(columns = {'player_dismissed':'Dismissals'})
        
    noof5wks = dismissals['Dismissals'].apply(lambda x: 1 if x > 4 else 0).sum()
    return (noof5wks)    
    
def getNoofHundreds(df):
    
    runs = pd.DataFrame(df.groupby(['Season','match_id'])['batsman_runs'].sum().reset_index()).rename(columns={'batsman_runs':'Match_Runs'})
    noofhundreds = runs['Match_Runs'].apply(lambda x: 1 if x >=100 else 0).sum()
    
    return (noofhundreds)
    
def getPlayerStatistics(df,grpbyList):    
        
        df['isDot'] = df['batsman_runs'].apply(lambda x: 1 if x == 0 else 0)
        df['isOne'] = df['batsman_runs'].apply(lambda x: 1 if x == 1 else 0)
        df['isTwo'] = df['batsman_runs'].apply(lambda x: 1 if x == 2 else 0)
        df['isThree'] = df['batsman_runs'].apply(lambda x: 1 if x == 3 else 0)
        df['isFour'] = df['batsman_runs'].apply(lambda x: 1 if x == 4 else 0)
        df['isSix'] = df['batsman_runs'].apply(lambda x: 1 if x == 6 else 0)
        
      
        if ('phase' in grpbyList):
            df['phase'] = df['over'].apply(lambda x: utils.phase(x))
         
            
        runs = pd.DataFrame(df.groupby(grpbyList)['batsman_runs'].sum().reset_index()).groupby(grpbyList)['batsman_runs'].sum().reset_index().rename(columns={'batsman_runs':'Runs'})
        
        innings = pd.DataFrame(df.groupby(grpbyList)['match_id'].apply(lambda x: len(list(np.unique(x)))).reset_index()).rename(columns = {'match_id':'Innings'})
        balls = pd.DataFrame(df.groupby(grpbyList)['match_id'].count()).reset_index().rename(columns = {'match_id':'Balls'})
        
        bowler_dismissal_df = df[~df.dismissal_kind.isin(['run out', 'retired hurt', 'obstructing the field','NA'])]
        dismissals = pd.DataFrame(bowler_dismissal_df.groupby(grpbyList)['player_dismissed'].count()).reset_index().rename(columns = {'player_dismissed':'Dismissals'})
        
        dots = pd.DataFrame(df.groupby(grpbyList)['isDot'].sum()).reset_index().rename(columns = {'isDot':'dots'})
        ones = pd.DataFrame(df.groupby(grpbyList)['isOne'].sum()).reset_index().rename(columns = {'isOne':'ones'})
        twos = pd.DataFrame(df.groupby(grpbyList)['isTwo'].sum()).reset_index().rename(columns = {'isTwo':'twos'})
        threes = pd.DataFrame(df.groupby(grpbyList)['isThree'].sum()).reset_index().rename(columns = {'isThree':'threes'})
        fours = pd.DataFrame(df.groupby(grpbyList)['isFour'].sum()).reset_index().rename(columns = {'isFour':'Fours'})
        sixes = pd.DataFrame(df.groupby(grpbyList)['isSix'].sum()).reset_index().rename(columns = {'isSix':'Sixes'})
        
        df = pd.merge(innings, runs, on = grpbyList).merge(balls, on = grpbyList).merge(dismissals, on = grpbyList).merge(dots, on = grpbyList).merge(ones, on = grpbyList).merge(twos, on = grpbyList).merge(threes, on = grpbyList).merge(fours, on = grpbyList).merge(sixes, on = grpbyList)
        
        
        
        #st.table(df)
        if 'batsman' in df.columns:
            
            #StrikeRate
            df['SR'] = (round(df.apply(lambda x: 100*(x['Runs']/x['Balls']), axis = 1),2))

            #runs per innings
            df['RPI'] = (round(df.apply(lambda x: x['Runs']/x['Innings'], axis = 1),2))

            #balls per dismissals
            df['BPD'] = (round(df.apply(lambda x: utils.balls_per_dismissal(x['Balls'], x['Dismissals']), axis = 1),2))

            #balls per boundary
            df['BPB'] = (round(df.apply(lambda x: utils.balls_per_boundary(x['Balls'], (x['Fours'] + x['Sixes'])), axis = 1),2))

        if 'bowler' in df.columns:    
            
            
           
            # StrikeRate = Balls per wicket
            df['SR'] = (round(df.apply(lambda x: utils.balls_per_dismissal(x['Balls'], x['Dismissals']), axis = 1),2))

            # Economy = runs per over
            df['Eco'] = (round(df.apply(lambda x: utils.runs_per_ball(x['Balls'], x['Runs'])*6, axis = 1),2))
        
        # Average = Runs per wicket
        df['Avg'] = (round(df.apply(lambda x: utils.runs_per_dismissal(x['Runs'], x['Dismissals']), axis = 1),2))
        #boundary%
        df['Boundary%'] = (round(df.apply(lambda x: utils.boundary_per_ball(x['Balls'], (x['Fours'] + x['Sixes']))*100, axis = 1),2))
        df['Dot%'] = (round(df.apply(lambda x: utils.get_dot_percentage(x['dots'], x['Balls'])*100, axis = 1),2))
        
        df.drop(['dots','ones','twos','threes','Fours','Sixes'], axis=1, inplace=True)
        #df.drop(['dots','fours','sixes'], axis=1, inplace=True)    
              
        
        return df
        
       
def plotBarGraph(df,grpbyList,title,xKey,xlabel,ylabel):        
        
        plt.figure(figsize = (12, 4))    
        plt.style.use('dark_background')
        plt.tight_layout()
        df.groupby(grpbyList)[xKey].sum().sort_values().plot(kind = 'barh')
              
        
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        
        for i, v in enumerate(df.groupby(grpbyList)[xKey].sum().sort_values()):
            #plt.text(v+1 , i-.15 , str(v),
             #       color = 'blue', fontweight = 'bold')
            plt.text(v+0.05 , i-.15 , str(v),
                    color = 'blue', fontweight = 'bold')
        st.pyplot(plt)

def plotScatterGraph(df,key1,key2,xlabel,ylabel,player_type='batsman'):        
        
        plt.figure(figsize = (16, 10))
        plt.style.use('dark_background')
        plt.scatter(df[key1], df[key2],s=45)
        title = ylabel+' vs '+xlabel
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)


        annotations=list(df[player_type])
        #selected_players = ['A Kumble', 'SL Malinga', 'A Mishra', 'Sohail Tanvir', 'DW Steyn']

        for i, label in enumerate(annotations):
            #if label in selected_players:
            plt.annotate(label, (df[key1][i], df[key2][i]),(df[key1][i]+.07, df[key2][i]))
        
        st.pyplot(plt)