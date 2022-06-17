import streamlit as st
import pandas as pd
import numpy as np
from apps import utils

def app():
    utils.header()
    series = utils.getSeries()
    table_header_str = f"""<h3 style='text-align: center; color: white;'>{series} - Bowling Records</h3>"""
    
    del_df = utils.load_deliveries_data()
    match_df = utils.load_match_data()
    player_df = utils.load_player_data()
    
    comb_df=utils.return_combined_matchdf(del_df,match_df)
    merged_df = pd.merge(comb_df, player_df, left_on='bowler', right_on='Player_Name', how='left')
    comb_df = merged_df

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
        df['Dot%'] = (round(df.apply(lambda x: utils.get_dot_percentage(x['dots'], x['balls'])*100, axis = 1),2))
        
        #boundary%
        df['Boundary%'] = (round(df.apply(lambda x: utils.boundary_per_ball(x['balls'], (x['fours'] + x['sixes']))*100, axis = 1),2))
        
        # Average = Runs per wicket
        df['Avg'] = (round(df.apply(lambda x: utils.runs_per_dismissal(x['runs'], x['dismissals']), axis = 1),2))
        
        # StrikeRate = Balls per wicket
        df['SR'] = (round(df.apply(lambda x: utils.balls_per_dismissal(x['balls'], x['dismissals']), axis = 1),2))

        # Economy = runs per over
        df['Eco'] = (round(df.apply(lambda x: utils.runs_per_ball(x['balls'], x['runs'])*6, axis = 1),2))
        
        
        return df
    
    with st.form("my_form"):   
        st.markdown(table_header_str, unsafe_allow_html=True)
        bowler_list = utils.getBowlerList(comb_df)
        season_list = utils.getSeasonList(comb_df)
        venue_list = utils.getVenueList(comb_df)
        team_list = sorted(comb_df['team1'].unique())
        
        #st.write(comb_df)
        DEFAULT = 'Pick a player'
        DEFAULT_ALL = 'ALL'
        bowler = utils.selectbox_with_default(st,'Select bowler *',bowler_list,DEFAULT)
        venue = utils.selectbox_with_default(st,'Select venue',venue_list,DEFAULT_ALL)
        opposition = utils.selectbox_with_default(st,'Select opposition',team_list,DEFAULT_ALL)
        start_season = min(season_list)
        start_year, end_year = st.select_slider('Season',options=season_list, value=(start_season, 2022))
        submitted = st.form_submit_button("Show Stats")
        title_alignment= """   <style>  .css-1p05t8e {   border-width : 0    }    </style>   """
        st.markdown(title_alignment, unsafe_allow_html=True)
        
    if submitted:                
        comb_df['isBowlerWk'] = comb_df.apply(lambda x: utils.is_wicket(x['player_dismissed'], x['dismissal_kind']), axis = 1)
        bowler_name = utils.getPlayerName(bowler,player_df)
        filtered_df = utils.getSeasonDataFrame(comb_df,start_year,end_year)
        if bowler != DEFAULT:
            filtered_df = utils.getSpecificDataFrame(filtered_df,'bowler',bowler_name)    
        else:
             st.error('Please select bowler')
             return
        if not filtered_df.empty:  
            if venue != DEFAULT_ALL: 
                filtered_df = utils.getSpecificDataFrame(filtered_df,'venue',venue)
            if opposition != DEFAULT_ALL: 
                filtered_df = utils.getSpecificDataFrame(filtered_df,'batting_team',opposition)
            if not filtered_df.empty:
               # st.write(filtered_df)
                grpbyList = ['bowler','inning']
                playerinning_df = utils.getPlayerStatistics(filtered_df,grpbyList)
                
                playerphase_df = playerStatistics(filtered_df)
                player_df = utils.getPlayerStatistics(filtered_df,['bowler'])
                playerphase_df.drop(['bowler'], axis=1, inplace=True) 
                
                noof4wks = utils.getNoof4Wickets(filtered_df)
                noof5wks = utils.getNoof5Wickets(filtered_df)
                #return
                #player_df.drop(['bowler'], axis=1, inplace=True)       
                # CSS to inject contained in a string
                hide_dataframe_row_index = """
                            <style>                        
                            .row_heading.level0 {display:none}
                            .blank {display:none}
                            
                            </style>
                            """

                # Inject CSS with Markdown
                st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
                st.write("Inn:",player_df['Innings'][0],"| Balls:",player_df['Balls'][0],'| Runs:',player_df['Runs'][0],"| Wks:",player_df['Dismissals'][0],"| Dot %:",player_df['Dot%'][0],"| Boundary %:",player_df['Boundary%'][0],"| 4W:",noof4wks,"| 5W:",noof5wks)
                st.subheader('Perfomance across different phases of a game')            
                st.table(playerphase_df.style.format(precision=2))
                
                st.subheader('Perfomance across Innings of a game')
               
                playerinning_df.drop(['bowler'], axis=1, inplace=True)
                         
                st.table(playerinning_df.style.format(precision=2))
                
                if opposition != DEFAULT_ALL: 
                    grpbyList=['batsman']
                    title = bowler+ ' - against all batsman'
                    xKey = 'is_wicket'
                    xlabel = 'Wickets taken'
                    ylabel = 'Batsman'
                    #st.write(filtered_df.head(10))
                
                else:
                    grpbyList=['batting_team']
                    title = bowler+ ' - against all teams'
                    xKey = 'is_wicket'
                    xlabel = 'Wickets taken'
                    ylabel = 'Opposition Teams'
                
                utils.plotBarGraph(filtered_df,grpbyList,title,xKey,xlabel,ylabel)
                
            else:
                st.subheader('No Data Found!')
        else:
            st.subheader('No Data Found!')