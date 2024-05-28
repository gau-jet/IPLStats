import streamlit as st
import streamlit.components.v1 as components 
import pandas as pd
import numpy as np
from data.create_data import create_table
from apps import utils


def app():
    
    utils.header()
    st.title('T20 STATS')
    #st.markdown("### IPL TOOLS")
    st.write("This is a website devoted to Cricket statistics and analytics. This website covers stats for all seasons of IPL, Women T20 Challenge and International T20 matches.")
    #components.html("<div class='stMarkdown' style='width: 661px;'><h3>sample home page</h3></div>", width=600, height=20)
    #st.header("[IPL Tools](http://localhost:8501)")
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    col5, col6 = st.columns(2)
    col7, col8 = st.columns(2)
    col9, col10 = st.columns(2)
    series_name = st.query_params
    if series_name:        
        series = series_name['series']
    else:
        series = 'IPL'
        
    
    with col1:
        st.markdown  ("[Batting Records](?option=Batting+Records&series="+series+") <br>Check a batter's record by innings, phase, venue",True)
    with col2:
        st.markdown  ("[Bowling Records](?option=Bowling+Records&series="+series+") <br>Check a bowler's record by innings, phase, venue",True)
    with col3:
        st.markdown  ("[Overall Records](?option=Team+Records&series="+series+") <br>Check overall records by team",True)
    with col4:
        st.markdown  ("[Venue Records](?option=Venue+Records&series="+series+") <br>Check records at a given Venue",True)
    with col5:
        st.markdown  ("[Batter Comparison](?option=Batter+Comaprison&series="+series+") <br>Comparison of top batsmen across phases or against a bowling type",True)
    with col6:
        st.markdown  ("[Bowler Comparison](?option=Bowler+Comaprison&series="+series+") <br>Comparison of top bowlers across phases or against a batting style",True)
    with col7:
        st.markdown  ("[Batter Matchups](?option=Batter+Matchups&series="+series+") <br>Batman vs Bowling Style Matchup",True)
        st.markdown  ("[Team Matchups](?option=Team+Matchups&series="+series+") <br>Team Comparison",True)
    with col8:
        st.markdown  ("[Bowler Matchups](?option=Bowler+Matchups&series="+series+") <br>Bowler vs batting style Matchup",True)
        st.markdown  ("[Match Analysis](?option=Match+Analysis&series="+series+") <br>Win Percentage and Runs progresion chart of a match",True)
   # if series == 'IPL':
    #    with col9:
     #       st.markdown  ("[Win Predictor](?option=Win+Predictor) <br>Win Prediction Model during second innings of match",True)
     #   with col10:
     #       st.markdown  ("[Score Predictor](?option=Score+Predictor) <br>Score Prediction Model of a team",True)
    #components.html("<br>Prediction Model", width=300, height=10)
    #st.markdown("### Sample Data")
    #df = create_table()
    #st.write(df)

    #st.write('Navigate to `Data Stats` page to visualize the data')