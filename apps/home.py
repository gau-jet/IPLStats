import streamlit as st
import streamlit.components.v1 as components 
import pandas as pd
import numpy as np
from data.create_data import create_table

def app():
    st.title('IPL TOOLS')
    #st.markdown("### IPL TOOLS")
    st.write("This is a home page for all IPL related stats.")
    #components.html("<div class='stMarkdown' style='width: 661px;'><h3>sample home page</h3></div>", width=600, height=20)
    #st.header("[IPL Tools](http://localhost:8501)")
    #st.markdown  ("[Win Predictor](predictwinpercent.py) <br>Prediction Model",True)
    
    #components.html("<br>Prediction Model", width=300, height=10)
    #st.markdown("### Sample Data")
    #df = create_table()
    #st.write(df)

    #st.write('Navigate to `Data Stats` page to visualize the data')