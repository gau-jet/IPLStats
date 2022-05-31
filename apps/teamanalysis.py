import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use( 'Agg')
from apps import utils

def app():
    utils.header()
        
    del_df = utils.return_df("data/deliveries.csv")
    match_df = utils.return_df("data/matches.csv")
    player_df = utils.return_df("data/Player Profile.csv")
    merged_df=utils.return_combined_matchdf(del_df,match_df)

    #merged_df = merged_df[['id' , 'inning' , 'batting_team' , 'bowling_team' , 'over' , 'ball' , 'total_runs' , 'is_wicket' , 'player_dismissed' , 'venue']]
    #merged_df = merged_df.replace(np.NaN, 0)
    #st.write(merged_df.head(10))
    
    with st.form("my_form"):    
        st.markdown("<h3 style='text-align: center; color: white;'>Team Records</h3>", unsafe_allow_html=True)
        team_list = sorted(merged_df['team1'].unique())
        venue_list = utils.getVenueList(merged_df)    
        season_list = utils.getSeasonList(merged_df)
    
    #team = st.selectbox('Select Team',sorted(team_list))
    
        DEFAULT_TEAM = 'Pick a team'
        team = utils.selectbox_with_default(st,'Select Team *',team_list,DEFAULT_TEAM)
        
        DEFAULT = 'ALL'
        venue = utils.selectbox_with_default(st,'Select Venue',sorted(venue_list),DEFAULT)
        start_year, end_year = st.select_slider('Season',options=season_list, value=(2008, 2022))
        submitted = st.form_submit_button("Show Stats")
        title_alignment= """   <style>  .css-1p05t8e {   border-width : 0    }    </style>   """
        st.markdown(title_alignment, unsafe_allow_html=True)
        
    if submitted:
        team_df = utils.getSeasonDataFrame(merged_df,start_year,end_year)
        
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
            
            teamstats_df = utils.getTeamStats(team_df,team)
            st.write("Played:",teamstats_df['Played'][0],'| Won:',teamstats_df['Won'][0],'| Lost:',teamstats_df['Lost'][0],"| Tied:",teamstats_df['Tied'][0],"| No Result:",teamstats_df['No Result'][0])
            grpbyList = ['batsman']
            #battingteam_df = utils.getSpecificDataFrame(team_df,'batting_team',team)
            
            if not battingteam_df.empty:
                batsmanstats_df = utils.getPlayerStatistics(battingteam_df,grpbyList)
            else:
                return
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