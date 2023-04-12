import streamlit as st
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from apps import utils

def app():
    utils.header()
    #st.title('Batter Matchups')    
    series = utils.getSeries()
    table_header_str = f"""<h3 style='text-align: center; color: white;'>{series} - Batsman Matchups</h3>"""
    del_df = utils.load_deliveries_data()
    match_df = utils.load_match_data()
    player_df = utils.return_df("data/Player Profile.csv")
    

    merged_df = utils.return_combined_matchdf(del_df,match_df)   
    batting_merged_df = pd.merge(merged_df, player_df[['Player_Name','display_name','batting_style']], left_on='batsman', right_on='Player_Name', how='left')
    batting_merged_df.drop(['Player_Name'], axis=1, inplace=True)       
    comb_df = pd.merge(batting_merged_df, player_df[['Player_Name','bowling_style']], left_on='bowler', right_on='Player_Name', how='left')
    comb_df.drop(['Player_Name'], axis=1, inplace=True)
    

    #comb_df = comb_df[['id' , 'inning' , 'batting_team' , 'bowling_team' , 'over' , 'ball' , 'total_runs' , 'is_wicket' , 'player_dismissed' , 'venue']]
    #comb_df = comb_df.replace(np.NaN, 0)
    #st.write(comb_df.head(10))
    with st.form("my_form"): 
        st.markdown(table_header_str, unsafe_allow_html=True)
        bowling_type = comb_df['bowling_style'].dropna().unique()
        batsman_list = utils.getBatsmanList(comb_df)
        season_list = utils.getSeasonList(comb_df)
        start_season = min(season_list)
        end_season = max(season_list)
        #st.write(comb_df)
        
        DEFAULT_BATSMAN = 'Pick a player'
        batsman = utils.selectbox_with_default(st,'Select batsman *',batsman_list,DEFAULT_BATSMAN)
        DEFAULT = 'ALL'
        bowling_type = utils.selectbox_with_default(st,'Select bowler type',sorted(bowling_type),DEFAULT)
        col1, col2 = st.columns(2)
        with col1:
            start_year, end_year = st.select_slider('Season',options=season_list, value=(start_season, end_season))
        with col2:    
            min_balls = st.number_input('Min. Balls',min_value=10,value=20,format='%d')
        submitted = st.form_submit_button("Show Stats")
        title_alignment= """   <style>  .css-1p05t8e {   border-width : 0    }    </style>   """
        st.markdown(title_alignment, unsafe_allow_html=True)
        
    if submitted:       
        filtered_df = utils.getSeasonDataFrame(comb_df,start_year,end_year)
        if batsman != DEFAULT_BATSMAN:
            batsman_name = utils.getPlayerName(batsman,player_df)
            filtered_df = utils.getSpecificDataFrame(filtered_df,'batsman',batsman_name)    
        else:
            st.error('Please select batsman')
            return
        if bowling_type != DEFAULT:
            filtered_df = utils.getSpecificDataFrame(filtered_df,'bowling_style',bowling_type)     
        if not filtered_df.empty:
            filtered_df = utils.getMinBallsFilteredDataFrame(filtered_df,min_balls)
        #st.write(filtered_df)
        #return
        if filtered_df.empty:
            st.subheader('No Data Found!')
        if not filtered_df.empty:  
            
           # st.write(filtered_df)
            #grpbyList = 'bowler'
            filtered_df['isBowlerWk'] = filtered_df.apply(lambda x: utils.is_wicket(x['player_dismissed'], x['dismissal_kind']), axis = 1)
            player_df = utils.getPlayerStatistics(filtered_df,['bowler'])
            #st.table(player_df);            
            player_df.reset_index(drop=True,inplace=True)
            
            if not player_df.empty:
                sort_by_list = ['Runs']
                sort_asc_order = [False]
                topSRbatsman_df = utils.getTopRecordsDF(player_df,sort_by_list,sort_asc_order,10)
                #topSRbatsman_df = getTopRecordsDF(player_df,'Runs',10)
                
                grpbyList=['bowler']
                title = batsman_name+ ' - against bowlers'
                xKey = 'Runs'
                xlabel = 'Runs scored'
                ylabel = 'Bowler'
                #st.write(topSRbatsman_df)
                utils.plotBarGraph(topSRbatsman_df,grpbyList,title,xKey,xlabel,ylabel)
                #plotScatterGraph(topSRbatsman_df,'SR','Eco','StrikeRate','EconomyRate')            
            
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
            sort_by_list = ['Dismissals']
            sort_asc_order = [False]
            topSRbatsman_df = utils.getTopRecordsDF(player_df,sort_by_list,sort_asc_order,10)
            topSRbatsman_df.drop(['index','SR','Eco'], axis=1, inplace=True)
            st.subheader('Players who have dismissed the batsman most')
            st.table(topSRbatsman_df.style.format(precision=2))
            
            sort_by_list = ['Runs']
            sort_asc_order = [False]
            st.subheader('Players against which the batsman has scored most')
            topSRbatsman_df = utils.getTopRecordsDF(player_df,sort_by_list,sort_asc_order,10)
            topSRbatsman_df.drop(['index','SR','Eco'], axis=1, inplace=True)
            st.table(topSRbatsman_df.style.format(precision=2))