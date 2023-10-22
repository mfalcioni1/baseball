import random
import pandas as pd

class Player:
    def __init__(self, 
                 name: str, 
                 ab: int, 
                 h: int, 
                 b_2: int,
                 b_3: int,
                 hr: int,
                 bb: int,
                 so: int,
                 sf: int,
                 sh: int,
                 gdp: int,
                 sb: int,
                 cs: int):
        """
        A class representing a baseball player.

        Args:
        name (str): The name of the player.
        ab (int): The number of at-bats the player has had.
        h (int): The number of hits the player has had.
        b_1 (int): The number of singles the player has hit.
        b_2 (int): The number of doubles the player has hit.
        b_3 (int): The number of triples the player has hit.
        hr (int): The number of home runs the player has hit.
        bb (int): The number of walks the player has received.
        so (int): The number of times the player has struck out.
        sf (int): The number of sacrifice flies the player has hit.
        sh (int): The number of sacrifice hits the player has hit.
        gdp (int): The number of ground into double plays the player has hit into.
        sb (int): The number of stolen bases the player has successfully made.
        cs (int): The number of times the player has been caught stealing.

        Attributes:
        name (str): The name of the player.
        BA (float): The batting average of the player.
        SLG (float): The slugging percentage of the player.
        B1 (float): The percentage of hits that are singles for the player.
        B2 (float): The percentage of hits that are doubles for the player.
        B3 (float): The percentage of hits that are triples for the player.
        HR (float): The percentage of hits that are home runs for the player.
        OBP (float): The on-base percentage of the player.
        SO (float): The percentage of at-bats that result in a strikeout for the player.
        SF (float): The percentage of at-bats that result in a sacrifice fly for the player.
        SH (float): The percentage of at-bats that result in a sacrifice hit for the player.
        GDP (float): The percentage of at-bats that result in a ground into double play for the player.
        SB (float): The percentage of times the player successfully steals a base.
        CS (float): The percentage of times the player is caught stealing a base.
        """
        b_1 = h - b_2 - b_3 - hr
        self.name = name
        self.BA = h / ab
        self.SLG = (h + b_1 + 2 * b_2 + 3 * b_3 + 4 * hr) / ab
        self.B1 = b_1 / h
        self.B2 = b_2 / h
        self.B3 = b_3 / h
        self.HR = hr / h
        self.OBP = (h + bb) / (ab + bb)
        self.SO = so / ab
        self.SF = sf / ab
        self.SH = sh / ab
        self.GDP = gdp / ab
        self.SB = sb / (h + bb)
        self.CS = cs / (h + bb)

    def at_bat(self):
        """
        Simulates an at-bat for the player.

        Returns:
        str: The result of the at-bat, which can be one of "single", "double", "triple", "home run", "walk", or "out".
        """
        r = random.random() # an at-bat is a random event
        if r < self.BA:
            h_t = random.random()
            if h_t < self.B1:
                return "single"
            elif h_t < self.B1 + self.B2:
                return "double"
            elif h_t < self.B1 + self.B2 + self.B3:
                return "triple"
            else:
                return "home run"
        elif r < self.OBP:
            return "walk"
        else:
            return "out" # this need to be adjusted for productive outs
class Lineup:
    def __init__(self, players):
        self.players = players
    
    def simulate_inning(self):
        outs = 0
        runs = 0
        bases = [None, None, None]  # Represents the three bases: 1st, 2nd, and 3rd

        for player in self.players:
            if outs < 3:
                result = player.at_bat()
                if result == "out":
                    outs += 1
                elif result == "single":
                    # Move runners for a single
                    if bases[2] is not None:
                        runs += 1
                        bases[2] = None
                    if bases[1] is not None:
                        bases[2] = bases[1]
                        bases[1] = None
                    if bases[0] is not None:
                        bases[1] = bases[0]
                    bases[0] = player
                elif result == "double":
                    # Move runners for a double
                    if bases[2] is not None:
                        runs += 1
                        bases[2] = None
                    if bases[1] is not None:
                        runs += 1
                        bases[1] = None
                    if bases[0] is not None:
                        bases[2] = bases[0]
                        bases[0] = None
                    bases[1] = player
                elif result == "triple":
                    # Move runners for a triple
                    for i in range(3):
                        if bases[i] is not None:
                            runs += 1
                            bases[i] = None
                    bases[2] = player
                elif result == "home run":
                    # Move runners for a home run
                    for i in range(3):
                        if bases[i] is not None:
                            runs += 1
                            bases[i] = None
                    runs += 1  # The batter also scores
                elif result == "walk":
                    # Move runners for a walk
                    if bases[2] is None and bases[1] is not None and bases[0] is not None:
                        runs += 1
                    elif bases[1] is None and bases[0] is not None:
                        bases[2] = bases[1]
                    elif bases[0] is None:
                        bases[1] = bases[0]
                    bases[0] = player

        return runs

class Team:
    def __init__(self, name, lineup: Lineup):
        self.name = name
        self.lineup = lineup
        self.runs = 0

    def simulate_inning(self):
        return self.lineup.simulate_inning()

class Game:
    def __init__(self, team1: Team, team2: Team):
        self.team1 = team1
        self.team2 = team2
        self.team1.runs = 0
        self.team2.runs = 0

    def simulate_game(self):
        for inning in range(9):  # A standard game has 9 innings
            self.simulate_inning(inning)
        
        while self.team1.runs == self.team2.runs:  # Extra innings if tied
            self.simulate_inning(inning)
            inning += 1
        
        # Print or return the final score and winning team
        if self.team1.runs > self.team2.runs:
            winner = self.team1.name
        else:
            winner = self.team2.name
        
        print(f"Final Score: {self.team1.name} {self.team1.runs}, {self.team2.name} {self.team2.runs}")
        print(f"Winner: {winner}")
        return pd.DataFrame({'Team': [self.team1.name, self.team2.name], 'Runs': [self.team1.runs, self.team2.runs]})
    
    def simulate_inning(self, inning):
        print(f"Inning {inning + 1}:")
        
        runs_team1 = self.team1.simulate_inning()
        self.team1.runs += runs_team1
        print(f"{self.team1.name} scored {runs_team1} runs. Total: {self.team1.runs} runs")
        
        runs_team2 = self.team2.simulate_inning()
        self.team2.runs += runs_team2
        print(f"{self.team2.name} scored {runs_team2} runs. Total: {self.team2.runs} runs\n")

if __name__ == "__main__":
    import lineup as lu
    import argparse
    parser = argparse.ArgumentParser()
    #parser.add_argument("date", help="The date of the game to simulate in the format YYYY-MM-DD")
    #parser.add_argument("team", help="The three-letter abbreviation of the team to simulate")
    parser.add_argument("-s", "--sims", help="The number of simulations to run", type=int, default=10)
    args = parser.parse_args()

    #date = args.date
    #team_abbr = args.team
    sims = args.sims

    date = '2023-10-17'
    team_abbr = 'PHI'
    team_lineup, opp_lineup = lu.get_lineups(date, team_abbr)

    lineup_l_1 = []
    for row in team_lineup.iterrows():
        row = row[1]
        lineup_l_1.append(Player(row['Name'], row['AB'], row['H'], row['2B'], row['3B'], 
                                 row['HR'], row['BB'], row['SO'], row['SF'], row['SH'], 
                                 row['GDP'], row['SB'], row['CS']))
    lineup_l_2 = []
    for row in opp_lineup.iterrows():
        row = row[1]
        lineup_l_2.append(Player(row['Name'], row['AB'], row['H'], row['2B'], row['3B'], 
                                 row['HR'], row['BB'], row['SO'], row['SF'], row['SH'], 
                                 row['GDP'], row['SB'], row['CS']))
    
    lineup1 = Lineup(lineup_l_1)
    lineup2 = Lineup(lineup_l_2)
    team1 = Team(team_lineup["Tm"][0], lineup1)
    team2 = Team(opp_lineup["Tm"][0], lineup2)

    sim_res = []
    for i in range(sims):
        game = Game(team1, team2)
        sim_res.append(game.simulate_game())
    
    # return average score
    sim_res = pd.concat(sim_res)
    sim_res = sim_res.groupby('Team').mean()
    print(sim_res)