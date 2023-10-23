import pandas as pd
from pybaseball import statcast, batting_stats_bref

def get_lineups(date, team_abbr):
    # Fetch Game Data
    game_data = statcast(date, date) #this call needs to be improved, inefficient when there are many games.

    game_data = game_data[(game_data['home_team'] == team_abbr) | (game_data['away_team'] == team_abbr)]

    # Determine Opposing Team
    if game_data['home_team'].iloc[0] == team_abbr:
        team_data = game_data[game_data['inning_topbot'] == 'Bot']
        opp_team_data = game_data[game_data['inning_topbot'] == 'Top']
    else:
        team_data = game_data[game_data['inning_topbot'] == 'Top']
        opp_team_data = game_data[game_data['inning_topbot'] == 'Bot']

    # Fetch Player Data
    year = int(date[:4])
    all_batting = batting_stats_bref(year)

    def process_lineup(team_data):
        # Process Lineup
        lineup_df = (team_data[['batter', "at_bat_number"]]
                     .sort_values(by='at_bat_number')
                     .drop_duplicates(subset='batter', keep='first')
                     .head(9)  # Get the first 9 batters
                    )

        # Merge Lineup and Player Data
        lineup_with_player_data = pd.merge(
            lineup_df,
            all_batting,
            left_on='batter',
            right_on='mlbID',
            how='inner'
        )
        return lineup_with_player_data

    # Process both lineups
    lineup_with_player_data = process_lineup(team_data)
    opp_lineup_with_player_data = process_lineup(opp_team_data)

    return lineup_with_player_data, opp_lineup_with_player_data

if __name__ == '__main__':
    # Example:
    date = '2023-10-17'
    team_abbr = 'PHI'
    team_lineup, opp_lineup = get_lineups(date, team_abbr)
    print(team_lineup)
    print(opp_lineup)
