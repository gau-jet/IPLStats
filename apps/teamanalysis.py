import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use( 'Agg')
from apps import utils

def app():
    utils.header(st)
    st.title('Team Records')    
    
    del_df = utils.return_df("data/IPL Ball-by-Ball 2008-2022.csv")
    match_df = utils.return_df("data/IPL Matches 2008-2022.csv")
    player_df = utils.return_df("data/Player Profile.csv")
    comb_df = pd.merge(del_df, match_df, on = 'id', how='left')
    comb_df.rename(columns = {'id':'match_id'}, inplace = True)
    
    comb_df=utils.replaceTeamNames(comb_df)

    #comb_df = comb_df[['id' , 'inning' , 'batting_team' , 'bowling_team' , 'over' , 'ball' , 'total_runs' , 'is_wicket' , 'player_dismissed' , 'venue']]
    #comb_df = comb_df.replace(np.NaN, 0)
    #st.write(comb_df.head(10))
    
    
    team_list = sorted(comb_df['team1'].unique())
    venue_list = comb_df['venue'].unique()    
    season_list = utils.getSeasonList(comb_df)
    
    #team = st.selectbox('Select Team',sorted(team_list))
    
    DEFAULT_TEAM = 'Pick a team'
    team = utils.selectbox_with_default(st,'Select Team',team_list,DEFAULT_TEAM)
    
    DEFAULT = 'Pick a venue'
    venue = utils.selectbox_with_default(st,'Select Venue',sorted(venue_list),DEFAULT)
    start_year, end_year = st.select_slider('Season',options=season_list, value=(2008, 2022))
    
    if st.button('Show Stats'):
        team_df = utils.getSeasonDataFrame(comb_df,start_year,end_year)
        
        if venue == DEFAULT:
            venue = None
        else:
            team_df = utils.getSpecificDataFrame(team_df,'venue',venue)
        
        if not team == DEFAULT_TEAM:    
            battingteam_df = utils.getSpecificDataFrame(team_df,'batting_team',team)
            bowlingteam_df = utils.getSpecificDataFrame(team_df,'bowling_team',team)
        else:
            battingteam_df = team_df
            bowlingteam_df = team_df
        
        
        if not team_df.empty:
            grpbyList = ['batsman']
            #battingteam_df = utils.getSpecificDataFrame(team_df,'batting_team',team)
            
            batsmanstats_df = utils.getPlayerStatistics(battingteam_df,grpbyList)
            
            if not batsmanstats_df.empty:
                    sort_by_list = ['Runs']
                    sort_asc_order = [False]
                    topbatsmanstats_df = utils.getTopRecordsDF(batsmanstats_df,sort_by_list,sort_asc_order,5)
            
            grpbyList = ['bowler']
            #bowlingteam_df = utils.getSpecificDataFrame(team_df,'bowling_team',team)
            bowlertats_df = utils.getPlayerStatistics(bowlingteam_df,grpbyList)
            if not bowlertats_df.empty:
                    sort_by_list = ['Dismissals']
                    sort_asc_order = [False]
                    topbowlertats_df = utils.getTopRecordsDF(bowlertats_df,sort_by_list,sort_asc_order,10)
            
            
            #title = 'Top Batsman for the team'
            #xKey = 'batsman'
            #xlabel='Innings'
            #ylabel='Runs'
            #utils.plotStackBarGraph(topbatsmanstats_df,title,xKey,xlabel,ylabel)
            grpbyList=['batsman']
            title = 'Top batsman'
            xKey = 'Runs'
            xlabel = 'Runs'
            ylabel = 'Batsman'
            
            utils.plotBarGraph(topbatsmanstats_df,grpbyList,title,xKey,xlabel,ylabel)
            
            grpbyList=['bowler']
            title = 'Top Bowlers'
            xKey = 'Dismissals'
            xlabel = 'Dismissals'
            ylabel = 'Bowlers'
            
            utils.plotBarGraph(topbowlertats_df,grpbyList,title,xKey,xlabel,ylabel)
        else:
            st.subheader('No Data Found!')