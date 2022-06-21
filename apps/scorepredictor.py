import streamlit as st
import pickle
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor
from apps import utils

def app():
    utils.header()
     
    def replaceTeamNames(df):

        team_name_mappings = {'Delhi Daredevils':'Delhi Capitals','Deccan Chargers':'Sunrisers Hyderabad','Gujarat Lions':'Gujarat Titans','Kings XI Punjab':'Punjab Kings','Rising Pune Supergiants':'Rising Pune Supergiant','Pune Warriors':'Rising Pune Supergiant'} 
        
        for key, value in team_name_mappings.items():
            df['team1'] = df['team1'].str.replace(key,value)
            df['team2'] = df['team2'].str.replace(key,value)
            df['toss_winner'] = df['toss_winner'].str.replace(key,value)
            df['winner'] = df['winner'].str.replace(key,value)        
        return df
    
    deliveres = utils.load_match_data()
    series = utils.getSeries()
    
    if series == 'IPL':
        deliveres=replaceTeamNames(deliveres)
        rdf_regressor = pickle.load(open('data/IPL-Batting-score-xgboost.pkl','rb'))        
    elif series == 'T20I':
        rdf_regressor = pickle.load(open('data/T20I-Batting-score-xgboost.pkl','rb'))
    elif series == 'WT20':    
        rdf_regressor = pickle.load(open('data/WT20-Batting-score-xgboost.pkl','rb'))
    
    teams = sorted(deliveres['team1'].unique())
    venue = utils.getVenueList(deliveres)   
    
    #venue = deliveres['venue'].unique()
    
        
    st.title('Score Predictor')

    col1, col2 = st.columns(2)

    with col1:
        batting_team = st.selectbox('Select the batting team',sorted(teams))
    with col2:
        bowling_team = st.selectbox('Select the bowling team',sorted(teams),index=1)

    Venue = st.selectbox('Select Venue',sorted(venue))

    col3,col4,col5 = st.columns(3)

    with col3:
        runs = st.number_input('Current Score',min_value=0,format='%d')
    with col4:
        overs = st.number_input('Overs completed',min_value=5.0,step=0.1,format="%.1f")
    with col5:
        wickets = st.number_input('Wickets Fallen',min_value=0,format='%d')
    
    col6,col7 = st.columns(2)
    with col6:
        wickets_in_prev_5 = st.number_input('Runs scored in prev 5 overs',min_value=0,format='%d')
    with col7:
        runs_in_prev_5 = st.number_input('Wickets taken in prev 5 overs',min_value=0,format='%d')
        
    col8,col9 = st.columns(2)
    with col8:
        prev_30_dot_balls = st.number_input('No of Dots in prev 5 overs',min_value=0,format='%d')
    with col9:
        prev_30_boundaries = st.number_input('No of boundaries in prev 5 overs',min_value=0,format='%d')    

    if st.button('Predict Score'):
    
        input = pd.DataFrame(
        {'batting_team': [batting_team], 'bowling_team': [bowling_team], 'venue': Venue, 'current_score': [runs],
         'overs': [overs], 'current_wickets': [wickets], 'prev_30_runs': [runs_in_prev_5], 'prev_30_wickets': [wickets_in_prev_5], 'prev_30_dot_balls': [prev_30_dot_balls], 'prev_30_boundaries': [prev_30_boundaries]})
        
        rdf_regressor_score = rdf_regressor.predict(input)
       
        st.text(batting_team + " will score between " + str(int(rdf_regressor_score[0])-5) + " and " +  str(int(rdf_regressor_score[0])+5))
        
      
      