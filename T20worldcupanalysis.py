# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

data = pd.read_excel('/content/FullT20wc2024.xlsx')

data.head()

data.shape

# Initialize the batsman DataFrame with the specified columns

batsman_columns = {'ID':[],
                   'Player':[],
                   'Innings':[],
                   'Runs':[],
                   'Balls':[],
                   'Dots':[],
                   'Not Outs':[],
                   'Average':[],
                   'Strike Rate':[],
                   '4s':[],
                   '6s':[],
                   'Highscore':[],
                   '50':[],
                   '100':[]
                   }

batsman = pd.DataFrame(batsman_columns)

# Populate the 'ID' and 'Player' columns in the batsman DataFrame

unique_batsman = data['batter'].unique()
batsman['ID'] = range(1, len(unique_batsman) + 1)
batsman['Player'] = unique_batsman

# Calculate the number of innings played by each player

innings_counts = data.groupby('batter')['match_id'].nunique().reset_index()
innings_counts.columns = ['Player', 'Innings']
innings_dict = innings_counts.set_index('Player')['Innings'].to_dict()
batsman['Innings'] = batsman['Player'].map(innings_dict).fillna(0)

# Calculate the total runs scored by each player

runs_counts = data.groupby('batter')['runs_off_bat'].sum().reset_index()
runs_counts.columns = ['Player', 'Runs']
runs_dict = runs_counts.set_index('Player')['Runs'].to_dict()
batsman['Runs'] = batsman['Player'].map(runs_dict).fillna(0)

# Calculate the total balls faced by each player, excluding wides and no-balls

balls_counts = data.groupby('batter')['runs_off_bat'].count().reset_index()
balls_counts.columns = ['Player', 'Balls']
wides_counts = data[data['wides'] > 0].groupby('batter')['wides'].count().reset_index()
wides_counts.columns = ['Player', 'Wides']
balls_data = balls_counts.merge(wides_counts, on='Player', how='left')
balls_data = balls_data.fillna(0)
balls_data['ActualBalls'] = balls_data['Balls'] - balls_data['Wides']
balls_dict = balls_data.set_index('Player')['ActualBalls'].to_dict()
batsman['Balls'] = batsman['Player'].map(balls_dict).fillna(0)
batsman['Balls'] = batsman['Balls'].astype(int)

# Calculate the strike rate for each player

batsman['Strike Rate'] = (batsman['Runs'] / batsman['Balls'] * 100).round(2)

# Calculate the number of times each player got out and account for "retired hurt"

outs_counts = data.groupby('out_player')['match_id'].nunique().reset_index()
outs_counts.columns = ['Player', 'Out']
retd_hrt_counts = data[data['dismissal_type'] == 13].groupby('out_player')['match_id'].nunique().reset_index()
retd_hrt_counts.columns = ['Player', 'Retired Hurt']
not_outs = innings_counts.merge(outs_counts, on='Player', how='left').merge(retd_hrt_counts, on='Player', how='left')
not_outs['Not Outs'] = not_outs['Innings'] - not_outs['Out'] + not_outs['Retired Hurt']
not_outs_dict = not_outs.set_index('Player')['Not Outs'].to_dict()
batsman['Not Outs'] = batsman['Player'].map(not_outs_dict).fillna(0)
batsman['Not Outs'] = batsman['Not Outs'].astype(int)

# Calculate the batting average for each player

batsman['Average'] = (batsman['Runs'] / (batsman['Innings'] - batsman['Not Outs'])).round(2)

# Calculate the total number of fours hit by each player

fours_counts = data[data['runs_off_bat'] == 4].groupby('batter')['runs_off_bat'].count().reset_index()
fours_counts.columns = ['Player', 'fours']
fours_dict = fours_counts.set_index('Player')['fours'].to_dict()
batsman['4s'] = batsman['Player'].map(fours_dict).fillna(0)
batsman['4s'] = batsman['4s'].astype(int)

# Calculate the total number of sixes hit by each player

sixes_counts = data[data['runs_off_bat'] == 6].groupby('batter')['runs_off_bat'].count().reset_index()
sixes_counts.columns = ['Player', 'sixes']
sixes_dict = sixes_counts.set_index('Player')['sixes'].to_dict()
batsman['6s'] = batsman['Player'].map(sixes_dict).fillna(0)
batsman['6s'] = batsman['6s'].astype(int)

# Calculate the highest score for each player

high_score = data.groupby('batter')['batter_runs_cumulative'].max().reset_index()
high_score.columns = ['Player', 'Highscore']
high_score_dict = high_score.set_index('Player')['Highscore'].to_dict()
batsman['Highscore'] = batsman['Player'].map(high_score_dict).fillna(0)

# Calculate the number of fifties scored by each player

fifties_counts = data[data['batter_runs_cumulative'] > 50].groupby('out_player')['batter_runs_cumulative'].count().reset_index()
fifties_counts.columns = ['Player', 'Fifties']
fifties_dict = fifties_counts.set_index('Player')['Fifties'].to_dict()
batsman['50'] = batsman['Player'].map(fifties_dict).fillna(0)
batsman['50'] = batsman['50'].astype(int)

# Calculate the number of hundreds scored by each player

hundreds_counts = data[data['batter_runs_cumulative'] > 100].groupby('out_player')['batter_runs_cumulative'].count().reset_index()
hundreds_counts.columns = ['Player', 'Hundreds']
hundreds_dict = hundreds_counts.set_index('Player')['Hundreds'].to_dict()
batsman['100'] = batsman['Player'].map(hundreds_dict).fillna(0)
batsman['100'] = batsman['100'].astype(int)

# Calculate the boundary runs % scored by each player

boundary_runs = ((batsman['4s'] * 4) + (batsman['6s'] * 6))
batsman['Boundary Runs'] = boundary_runs.astype(int)
boundary_pct = (boundary_runs / batsman['Runs']) * 100
batsman['Boundary %'] = boundary_pct.round(2)

# Calculate the boundary rates by each player

boundary_rates = (batsman['Balls'] / (batsman['4s'] + batsman['6s']))
batsman['Boundary Rate'] = boundary_rates.round(2)
batsman['Boundary Rate'] = batsman['Boundary Rate'].replace(np.inf, 0)

# Calculate the Dot Balls by each player

dot_balls = data[data['runs_off_bat'] == 0].groupby('batter')['runs_off_bat'].count().reset_index()
dot_balls.columns = ['Player', 'Dot Balls']
dot_balls_dict = dot_balls.set_index('Player')['Dot Balls'].to_dict()
batsman['Dots'] = batsman['Player'].map(dot_balls_dict).fillna(0)
batsman['Dots'] = batsman['Dots'].astype(int)

# Calculate the Dot Ball% by each player

dot_ball_pct = (batsman['Dots'] / batsman['Balls']) * 100
batsman['Dot Ball %'] = dot_ball_pct.round(2)

# Calculate the Dot Rate by each player

dot_rate = (batsman['Balls'] / batsman['Dots'])
batsman['Dot Rate'] = dot_rate.round(2)
batsman['Dot Rate'] = batsman['Dot Rate'].replace(np.inf, 0)

# Calculate the Strike Rotation % by each player
strike_rotation = batsman['Runs'] - batsman['Boundary Runs']
batsman['Strike Rotation'] = strike_rotation.astype(int)
strike_rotation_pct = (batsman['Strike Rotation'] / batsman['Balls']) * 100
batsman['Strike Rotation %'] = strike_rotation_pct.round(2)

# Calculate the Dismissal Rate by each player

dismissal_rate = (batsman['Balls'] / (batsman['Innings'] - batsman['Not Outs']))
batsman['Dismissal Rate'] = dismissal_rate.round(2)
batsman['Dismissal Rate'] = batsman['Dismissal Rate'].replace(np.inf, 0)

batsman.head(250)
