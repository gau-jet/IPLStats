import streamlit as st
import pandas as pd
from apps import utils

def app():
    utils.header()
    series = utils.getSeries()
    table_header_str = f"""<h3 style='text-align: center; color: white;'>{series} - Venue Records</h3>"""
        
    del_df = utils.load_deliveries_data()
    match_df = utils.load_match_data()
    player_df = utils.return_df("data/Player Profile.csv")
    comb_df=utils.return_combined_matchdf(del_df,match_df)

    #comb_df = comb_df[['id' , 'inning' , 'batting_team' , 'bowling_team' , 'over' , 'ball' , 'total_runs' , 'is_wicket' , 'player_dismissed' , 'venue']]
    #comb_df = comb_df.replace(np.NaN, 0)
    #st.write(comb_df.head(10))
    with st.form("my_form"):
        st.markdown(table_header_str, unsafe_allow_html=True)
        DEFAULT = 'Pick a venue'
        
        venue_list = utils.getVenueList(comb_df)
        season_list = utils.getSeasonList(comb_df)
        start_season = min(season_list)
        end_season = max(season_list)
        venue = utils.selectbox_with_default(st,'Select venue *',venue_list,DEFAULT)
        start_year, end_year = st.select_slider('Season',options=season_list, value=(start_season, end_season))
        submitted = st.form_submit_button("Show Stats")
        title_alignment= """   <style>  .css-1p05t8e {   border-width : 0    }    </style>   """
        st.markdown(title_alignment, unsafe_allow_html=True)
        
    if submitted:
        if venue == DEFAULT:
            st.error('Please select venue')
            return
        filtered_df = utils.getSeasonDataFrame(comb_df,start_year,end_year)
        match_filtered_df = utils.getSeasonDataFrame(match_df,start_year,end_year)
        
        if not filtered_df.empty:
            filtered_df = utils.getSpecificDataFrame(filtered_df,'venue',venue)
            match_filtered_df = utils.getSpecificDataFrame(match_filtered_df,'venue',venue)
            if not filtered_df.empty:    
                #Code to be optimized remove venue param 
                InningsWinDF = utils.getPerInningsWinCount(match_filtered_df,venue)        
                VenueStatsDF = utils.getVenueStats(filtered_df,venue)
                        
                final_df = pd.merge(VenueStatsDF , InningsWinDF, on = 'venue')
                final_df.drop(['venue'], axis=1, inplace=True) 
                hide_dataframe_row_index = """
                            <style>                        
                            .row_heading.level0 {display:none}
                            .blank {display:none}
                            
                            </style>
                            """

                # Inject CSS with Markdown
                st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
                
                st.write("Matches:",final_df['Matches'][0],'| 1st Inns Avg score:',final_df['Avg Runs - 1st Innings'][0],'| 1st Inns Avg wks:',final_df['Avg Wickets - 1st Innings'][0],"| 2nd Inns Avg score:",final_df['Avg Runs - 2nd Innings'][0],"| 2nd Inns Avg wks:",final_df['Avg Wickets - 2nd Innings'][0],"| Bat 1st Wins:",final_df['Batting 1st-Wins'][0],"| Bat 2nd Wins:",final_df['Batting 2nd-Wins'][0])
                comb_df = pd.merge(filtered_df, player_df[['Player_Name','bowling_style']], left_on='bowler', right_on='Player_Name', how='left')
                comb_df.drop(['Player_Name'], axis=1, inplace=True)
                
                bowlingstats_df = utils.getBowlingStatsforaVenue(comb_df,venue)        
                st.subheader('Bowling Style Comparison')
                
                st.table(bowlingstats_df.style.format(precision=2))
            else:
                    st.subheader('No Data Found!')
        else:
                    st.subheader('No Data Found!')