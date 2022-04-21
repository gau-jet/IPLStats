import numpy as np 
import pandas as pd 
import math

def replaceTeamNames(df):

    team_name_mappings = {'Delhi Daredevils':'Delhi Capitals','Deccan Chargers':'Sunrisers Hyderabad','Gujarat Lions':'Gujarat Titans','Kings XI Punjab':'Punjab Kings','Rising Pune Supergiants':'Rising Pune Supergiant','Pune Warriors':'Rising Pune Supergiant'} 
    
    for key, value in team_name_mappings.items():
        df['batting_team'] = df['batting_team'].str.replace(key,value)
        df['bowling_team'] = df['bowling_team'].str.replace(key,value)
    return df

def selectbox_with_default(st,text, values, default, sidebar=False):
        func = st.sidebar.selectbox if sidebar else st.selectbox
        return func(text, np.insert(np.array(values, object), 0, default))

def phase(over):
    if over <= 6:
        return 'Powerplay'
    elif over <= 15:
        return 'Middle'
    else:
        return 'Death'    
        
def balls_per_dismissal(balls, dismissals):
    if dismissals > 0:
        return balls/dismissals
    else:
        return balls/1 
    
def balls_per_boundary(balls, boundaries):
	if boundaries > 0:
		return balls/boundaries
	else:
		return balls/1 
        
def balls_per_dismissal(balls, dismissals):
        if dismissals > 0:
            return balls/dismissals
        else:
            return balls/1 
    
def boundary_per_ball(balls, boundaries):
    if boundaries > 0:
        return boundaries/balls
    else:
        return 1/balls 
        
def get_dot_percentage(dots, balls):
    if balls > 0:
        return dots/balls
    else:
        return 0
    
def runs_per_ball(balls, runs_conceeded):
    if balls > 0:
        return runs_conceeded/balls
    else:
        return math.inf
    
def runs_per_dismissal(runs_conceeded, dismissals):
    if dismissals > 0:
        return runs_conceeded/dismissals
    else:
        return math.inf
        
def is_wicket(player_dismissed, dismissal_kind):
    if type(player_dismissed) != str:
        return 0
    elif ~(type(player_dismissed) != str) & (dismissal_kind not in ['run out', 'retired hurt', 'obstructing the field']):
        return 1
    else:
        return 0