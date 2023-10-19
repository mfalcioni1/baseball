from pybaseball import statcast, statcast_batter, batting_stats_bref

# Fetch Game Data
game_data = statcast('2023-10-17', '2023-10-17', team='PHI')

lineup = game_data['batter'].unique()

# Fetch Player Data
# pitch-by-pitch data
#player_data = statcast_batter(start_dt="2023-03-30", end_dt="2023-10-01", player_id=lineup[0])

all_batting = batting_stats_bref(2023)

all_batting[all_batting['mlbID'] == lineup[3]]