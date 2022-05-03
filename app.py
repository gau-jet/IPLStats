import streamlit as st
from multiapp import MultiApp
from apps import  home,batsmananalysis,bowleranalysis,teamanalysis,venueanalysis,battercomparison,bowlercomparison,battermatchups,bowlermatchups,predictwinpercent,scorepredictor # import your app modules here

app = MultiApp()

# Add all your application here
app.add_app("Home", home.app)
app.add_app("Batting Records", batsmananalysis.app)
app.add_app("Bowling Records", bowleranalysis.app)
app.add_app("Team Analysis", teamanalysis.app)
app.add_app("Venue Analysis", venueanalysis.app)
app.add_app("Batter Comparison", battercomparison.app)
app.add_app("Bowler Comparison", bowlercomparison.app)
app.add_app("Batter Matchups", battermatchups.app)
app.add_app("Bowler Matchups", bowlermatchups.app)
app.add_app("Win Predictor", predictwinpercent.app)
app.add_app("Score Predictor", scorepredictor.app)

# The main app
app.run()