import streamlit as st
import pickle
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from apps import utils

def app():
    utils.header(st)
    teams = ['Sunrisers Hyderabad',
     'Mumbai Indians',
     'Royal Challengers Bangalore',
     'Kolkata Knight Riders',
     'Kings XI Punjab',
     'Chennai Super Kings',
     'Rajasthan Royals',
     'Delhi Capitals',
     'Gujarat Titans',
     'Lucknow Super Giants'     
     ]
    
    deliveres = pd.read_csv("data/IPL Matches 2008-2022.csv")


    venue = deliveres['venue'].unique()
    
    dt_regressor = pickle.load(open('Batting-score-dt_regressor-model.pkl','rb'))    
    rdf_regressor = pickle.load(open('Batting-score-rdf_regressor-model.pkl','rb'))
    
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
        comb = pd.DataFrame(pd.np.empty((0, 69)))
        comb.columns = ['inning', 'over', 'ball', 
        'current_score', 'current_wickets',
       'prev_30_runs', 'prev_30_wickets', 'prev_30_dot_balls',
       'prev_30_boundaries', 'batting_team_Chennai Super Kings',
       'batting_team_Delhi Capitals', 'batting_team_Gujarat Titans',
       'batting_team_Kochi Tuskers Kerala',
       'batting_team_Kolkata Knight Riders',
       'batting_team_Lucknow Super Giants', 'batting_team_Mumbai Indians',
       'batting_team_Punjab Kings', 'batting_team_Rajasthan Royals',
       'batting_team_Rising Pune Supergiant',
       'batting_team_Royal Challengers Bangalore',
       'batting_team_Sunrisers Hyderabad', 'bowling_team_Chennai Super Kings',
       'bowling_team_Delhi Capitals', 'bowling_team_Gujarat Titans',
       'bowling_team_Kochi Tuskers Kerala',
       'bowling_team_Kolkata Knight Riders',
       'bowling_team_Lucknow Super Giants', 'bowling_team_Mumbai Indians',
       'bowling_team_Punjab Kings', 'bowling_team_Rajasthan Royals',
       'bowling_team_Rising Pune Supergiant',
       'bowling_team_Royal Challengers Bangalore',
       'bowling_team_Sunrisers Hyderabad', 'venue_Barabati Stadium',
       'venue_Brabourne Stadium', 
       'venue_Buffalo Park', 'venue_De Beers Diamond Oval',
       'venue_Dr DY Patil Sports Academy',       
       'venue_Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium',
       'venue_Dubai International Cricket Stadium', 'venue_Eden Gardens',
       'venue_Feroz Shah Kotla', 'venue_Green Park',
       'venue_Himachal Pradesh Cricket Association Stadium',
       'venue_Holkar Cricket Stadium',
       'venue_JSCA International Stadium Complex', 'venue_Kingsmead',
       'venue_M Chinnaswamy Stadium', 'venue_M.Chinnaswamy Stadium',
       'venue_MA Chidambaram Stadium',
       'venue_Maharashtra Cricket Association Stadium',       
       'venue_Narendra Modi Stadium', 'venue_Nehru Stadium',
       'venue_New Wanderers Stadium', 'venue_Newlands',
       'venue_OUTsurance Oval',
       'venue_Punjab Cricket Association IS Bindra Stadium, Mohali',       
       'venue_Rajiv Gandhi International Stadium, Uppal',
       'venue_Sardar Patel Stadium, Motera',
       'venue_Saurashtra Cricket Association Stadium',
       'venue_Sawai Mansingh Stadium',
       'venue_Shaheed Veer Narayan Singh International Stadium',
       'venue_Sharjah Cricket Stadium', 'venue_Sheikh Zayed Stadium',
       'venue_St George''s Park', 'venue_Subrata Roy Sahara Stadium',
       'venue_SuperSport Park',
       'venue_Vidarbha Cricket Association Stadium, Jamtha',
       'venue_Wankhede Stadium']
        input = pd.DataFrame(columns = comb.columns)
        oversdata=str(overs)
        over,ball = ([int(x)]  for x in oversdata.split(".",1))
        
        input.at[ 0, 'inning'] = 1
        input['over'] = over
        input['ball'] = ball
        input['current_score'] = runs
        input['current_wickets'] = wickets
        input['prev_30_runs'] = runs_in_prev_5
        input['prev_30_wickets'] = wickets_in_prev_5
        input['prev_30_dot_balls'] = prev_30_dot_balls
        input['prev_30_boundaries'] = prev_30_boundaries
        input['venue_' + Venue] = 1
        input['batting_team_' +  batting_team ] = 1
        input['bowling_team_' +  bowling_team ] = 1

        input = input.replace(np.nan,0)
        
        
        rdf_regressor_score = str(rdf_regressor.predict(input));
        dt_regressor_score = str(dt_regressor.predict(input));
        b="[]"
        for char in b:
            
            rdf_regressor_score = rdf_regressor_score.replace(char, "")
            dt_regressor_score = dt_regressor_score.replace(char, "")
        
        
        rdf_regressor_score = rdf_regressor_score.split(".")
        dt_regressor_score = dt_regressor_score.split(".")
        
        st.subheader(batting_team + " will score")
        
        st.text("Random Forest method: "+ rdf_regressor_score[0])
        st.text("Decision Tree method: " + dt_regressor_score[0])