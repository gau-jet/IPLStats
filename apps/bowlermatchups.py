import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from apps import utils

def app():
    utils.header()
    series = utils.getSeries()
    table_header_str = f"""<h3 style='text-align: center; color: white;'>{series} - Bowler Matchups</h3>"""
    del_df = utils.load_deliveries_data()
    match_df = utils.load_match_data()
    player_df = utils.return_df("data/Player Profile.csv")

    merged_df = pd.merge(del_df, match_df, on = 'id', how='left')
    merged_df.rename(columns = {'id':'match_id'}, inplace = True)    
    batting_merged_df = pd.merge(merged_df, player_df[['Player_Name','batting_style']], left_on='batsman', right_on='Player_Name', how='left')
    batting_merged_df.drop(['Player_Name'], axis=1, inplace=True)       
    comb_df = pd.merge(batting_merged_df, player_df[['Player_Name','display_name','bowling_style']], left_on='bowler', right_on='Player_Name', how='left')
    comb_df.drop(['Player_Name'], axis=1, inplace=True)
    
    comb_df=utils.replaceTeamNames (comb_df)
    season_list = utils.getSeasonList(comb_df)
    
    #st.text(df.columns)    
    #st.text(df.head())
    with st.form("my_form"):        
        st.markdown(table_header_str, unsafe_allow_html=True)
        batting_type = comb_df['batting_style'].dropna().unique()
        
        bowler_list = utils.getBatsmanList(comb_df)    
        
        start_season = min(season_list)
        
        DEFAULT_BOWLER = 'Pick a player'
        bowler = utils.selectbox_with_default(st,'Select bowler *',sorted(bowler_list),DEFAULT_BOWLER)
        DEFAULT = 'ALL'
        batting_type = utils.selectbox_with_default(st,'Select batting type',sorted(batting_type),DEFAULT)
        col1, col2 = st.columns(2)
        with col1:
            start_year, end_year = st.select_slider('Season',options=season_list, value=(start_season, 2022))
        with col2:    
            min_balls = st.number_input('Min. Balls',min_value=10,value=20,format='%d')
        submitted = st.form_submit_button("Show Stats")
        title_alignment= """   <style>  .css-1p05t8e {   border-width : 0    }    </style>   """
        st.markdown(title_alignment, unsafe_allow_html=True)
        
    if submitted:    
        
        filtered_df = utils.getSeasonDataFrame(comb_df,start_year,end_year)
        if bowler != DEFAULT_BOWLER:
            bowler_name = utils.getPlayerName(bowler,player_df)
            filtered_df = utils.getSpecificDataFrame(filtered_df,'bowler',bowler_name)
        else:
            st.error('Please select bowler')
            return
        if batting_type != DEFAULT:
            filtered_df = utils.getSpecificDataFrame(filtered_df,'batting_style',batting_type)
        if not filtered_df.empty:
            filtered_df = utils.getMinBallsFilteredDataFrame(filtered_df,min_balls)      
        #st.write(filtered_df)
        #return
        if filtered_df.empty:
            st.subheader('No Data Found!')
        if not filtered_df.empty:  
            filtered_df['isBowlerWk'] = filtered_df.apply(lambda x: utils.is_wicket(x['player_dismissed'], x['dismissal_kind']), axis = 1)    
            #st.write(filtered_df)
            #return
            #player_df = utils.playerBattingComparisonStatistics(filtered_df)
            player_df = utils.getPlayerStatistics(filtered_df,['batsman'])
            player_df.reset_index(drop=True,inplace=True)
            
            sort_by_list = ['Dismissals','Runs']
            sort_asc_order = [False,False]
            topSRbowlers_df = utils.getTopRecordsDF(player_df,sort_by_list,sort_asc_order,20)
            
            #plotScatterGraph(topSRbowlers_df,'SR','Eco','StrikeRate','EconomyRate')
            #topbowlers_df = getTopRecordsDF(player_df,'dismissals',15)
            utils.plotScatterGraph(topSRbowlers_df,'Boundary%','Dot%','Boundary Ball %','Dot Ball %')
            
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
            #st.subheader('Bowler Comparison Stats')
            topSRbowlers_df.drop(['index','Boundary%','Dot%'], axis=1, inplace=True)
            st.subheader('Batsman dismissed most by bowler')
            st.table(topSRbowlers_df.head(10).style.format(precision=2))
            sort_by_list = ['Runs']
            sort_asc_order = [False]
            st.subheader('Players who have scored most runs against bowler')
            topRunsbatsman_df = utils.getTopRecordsDF(player_df,sort_by_list,sort_asc_order,10)
            topRunsbatsman_df.drop(['index','Boundary%','Dot%'], axis=1, inplace=True)
            st.table(topRunsbatsman_df.style.format(precision=2))
    