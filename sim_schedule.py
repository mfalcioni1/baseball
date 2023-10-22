from pybaseball import schedule_and_record

def get_schedule(team_abbr, year):
    schedule = schedule_and_record(year, team_abbr)
    return schedule

if __name__ == '__main__':
    import game_sim as gs
    import lineup as lu
    # Example:
    team_abbr = 'PHI'
    year = 2020
    schedule = get_schedule(team_abbr, year)
    print(schedule)
    # convert list of dates to YYYY-MM-DD format
    dates = schedule['Date'].tolist()
    dates = [date.strftime('%Y-%m-%d') for date in dates]

    for date in dates:
        team_lineup, opp_lineup = lu.get_lineups(date, team_abbr)
        team = gs.Team(team_abbr, team_lineup)
        opp_team = gs.Team(opp_lineup)
        game = gs.Game(team, opp_team)
        game.simulate_game()