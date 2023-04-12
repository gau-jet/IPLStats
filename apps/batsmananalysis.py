import streamlit as st
import pandas as pd
from apps import utils


def app():
    utils.header()
    #st.title('Batting Records')    
    series = utils.getSeries()
    table_header_str = f"""<h3 style='text-align: center; color: white;'>{series} - Batting Records</h3>"""
    del_df = utils.load_deliveries_data()
    match_df = utils.load_match_data()
    player_df = utils.load_player_data()
        
    comb_df=utils.return_combined_matchdf(del_df,match_df)
      
    merged_df = pd.merge(comb_df, player_df, left_on='batsman', right_on='Player_Name', how='left')
    comb_df = merged_df
    with st.form("my_form"):     
        st.markdown(table_header_str, unsafe_allow_html=True)
        batsman_list = utils.getBatsmanList(comb_df)
        season_list = utils.getSeasonList(comb_df)
        start_season = min(season_list)
        end_season = max(season_list)
        venue_list = utils.getVenueList(comb_df)
        team_list = sorted(comb_df['team1'].unique())
        
        #st.write(comb_df)
        DEFAULT = 'Pick a player'
        
        DEFAULT_ALL = 'ALL'
        batsman = utils.selectbox_with_default(st,'Select batsman *',batsman_list,DEFAULT)
        venue = utils.selectbox_with_default(st,'Select venue',venue_list,DEFAULT_ALL)
        opposition = utils.selectbox_with_default(st,'Select opposition',team_list,DEFAULT_ALL)
        start_year, end_year = st.select_slider('Season',options=season_list, value=(start_season, end_season))
        submitted = st.form_submit_button("Show Stats")
        title_alignment= """   <style>  .css-1p05t8e {   border-width : 0    }    </style>   """
        st.markdown(title_alignment, unsafe_allow_html=True)
        
    if submitted:         
        filtered_df = utils.getSeasonDataFrame(comb_df,start_year,end_year)
        if batsman != DEFAULT:
            batsman_name = utils.getPlayerName(batsman,player_df)
            filtered_df = utils.getSpecificDataFrame(filtered_df,'batsman',batsman_name)       
        else:
            st.error('Please select batsman')
            return
            
        if filtered_df.empty:
            st.subheader('No Data Found!')
        if not filtered_df.empty:  
            
            if venue != DEFAULT_ALL: 
                filtered_df = utils.getSpecificDataFrame(filtered_df,'venue',venue)
            
            if opposition != DEFAULT_ALL: 
                filtered_df = utils.getSpecificDataFrame(filtered_df,'bowling_team',opposition)
            #st.write(filtered_df)
            #return
            if not filtered_df.empty:
                grpbyList = ['batsman','phase']
                playerphase_df = utils.getPlayerStatistics(filtered_df,grpbyList)
                grpbyList = ['batsman','inning']
                playerinning_df = utils.getPlayerStatistics(filtered_df,grpbyList)
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
                st.write("Innings:",player_df['Innings'][0],'| Runs:',player_df['Runs'][0],'| Outs:',player_df['Dismissals'][0],"| Avg:",player_df['Avg'][0],"| SR:",player_df['SR'][0],"| HS:",highestscore,"| 30s:",noof30s,"| 50s:",noof50s,"| 100s:",noof100s)
                st.subheader('Perfomance across different phases of a game')
               
                #st.write(playerphase_df['SR'])
                #return
                playerphase_df.drop(['batsman'], axis=1, inplace=True)
                         
                st.table(playerphase_df.style.format(precision=2))
                
                st.subheader('Perfomance across Innings of a game')
               
                #st.write(playerphase_df['SR'])
                #return
                playerinning_df.drop(['batsman','Innings'], axis=1, inplace=True)
                   
                st.table(playerinning_df.head(2).style.format(precision=2))
                
                #st.table(playerphase_df.style.set_properties(**{'text-align': 'right'}, axis=1)) ## doesnot work
                st.write('* BPD -> Balls per dismissal, \t\t BPB -> Balls per boundary')
                
                if opposition != DEFAULT_ALL: 
                    grpbyList=['bowler']
                    title = batsman+ ' - against all bowlers'
                    xKey = 'batsman_runs'
                    xlabel = 'Runs scored'
                    ylabel = 'Bowlers'
                
                else:
                    grpbyList=['bowling_team']
                    title = batsman+ ' - against all teams'
                    xKey = 'batsman_runs'
                    xlabel = 'Runs scored'
                    ylabel = 'Opposition Teams'
                
                utils.plotBarGraph(filtered_df,grpbyList,title,xKey,xlabel,ylabel)
            else:
                st.subheader('No Data Found!')