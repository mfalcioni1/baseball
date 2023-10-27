from pybaseball import schedule_and_record
from datetime import datetime
import pandas as pd

def get_schedule(team_abbr, year):
    schedule = schedule_and_record(year, team_abbr)
    return schedule

def parse_date(date_str, year):
    if '(' in date_str:
        # If date string contains '(', it's a double-header
        date_part, game_part = date_str.rsplit(' ', 1)
        game_number = int(game_part.strip('()'))
    else:
        # Otherwise, it's a regular game
        date_part = date_str
        game_number = 1  # Assume game 1 for regular games

    # Parse the date part into the desired format
    date_part = f'{year} {date_part}'
    date_object = datetime.strptime(date_part, '%Y %A, %b %d')
    formatted_date = date_object.strftime('%Y-%m-%d')

    return formatted_date, game_number

if __name__ == '__main__':
    import game_sim as gs
    import lineup as lu
    # Example:
    team_abbr = 'PHI'
    year = 2020
    schedule = get_schedule(team_abbr, year)
    print(schedule)
    schedule[['Date', 'Game_Number']] = schedule['Date'].apply(lambda x: parse_date(x, year)).apply(pd.Series)
    # 2020-08-09 PHI is a double-header
    sim_result = pd.DataFrame()
    for _, game in schedule.iterrows():
        team_lineup, opp_lineup = lu.get_lineups(game['Date'], team_abbr)
        obj_tl = gs.Lineup(team_lineup)
        obj_ol = gs.Lineup(opp_lineup)
        team = gs.Team(game['Tm'], obj_tl)
        opp_team = gs.Team(game['Opp'], obj_ol)
        game_obj = gs.Game(team, opp_team, 100)
        ave_scores, iter_log = game_obj.simulate_game()
        # Convert simulation result dictionary to DataFrame
        tm = game['Tm']
        opp = game['Opp']
        df = pd.DataFrame({'Date': [game['Date']],
                           'Tm': [tm], 
                           'Opp': [opp], 
                           'Tm_ave_score': [ave_scores[tm]['Average Score']],
                           'Tm_sd_score': [ave_scores[tm]['Standard Deviation']],
                           'Tm_win_prob': [ave_scores[tm]['Win Probability']],
                           'Opp_ave_score': [ave_scores[opp]['Average Score']],
                           'Opp_sd_score': [ave_scores[opp]['Standard Deviation']]})
        
        sim_result = pd.concat([sim_result, df], ignore_index=True)
