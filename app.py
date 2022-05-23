import streamlit as st
from multiapp import MultiApp
from apps import  home,batsmananalysis,bowleranalysis,teamanalysis,venueanalysis,battercomparison,bowlercomparison,battermatchups,bowlermatchups,teammatchups,predictwinpercent,scorepredictor # import your app modules here

app = MultiApp()

# Add all your application here
app.add_app("Home", home.app)
app.add_app("Batting Records", batsmananalysis.app)
app.add_app("Bowling Records", bowleranalysis.app)
app.add_app("Team Records", teamanalysis.app)
app.add_app("Venue Records", venueanalysis.app)
app.add_app("Batter Comparison", battercomparison.app)
app.add_app("Bowler Comparison", bowlercomparison.app)
app.add_app("Batter Matchups", battermatchups.app)
app.add_app("Bowler Matchups", bowlermatchups.app)
app.add_app("Team Matchups", teammatchups.app)
app.add_app("Win Predictor", predictwinpercent.app)
app.add_app("Score Predictor", scorepredictor.app)

# The main app
app.run()