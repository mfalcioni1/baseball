import random
import pandas as pd
from typing import Union

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
    def __init__(self, players: Union[list, pd.DataFrame]):
        # player can be a list of Player objects or a dataframe
        # if it is a dataframe then we create a list of Player objects
        if isinstance(players, pd.DataFrame):
            players = [Player(row['Name'], row['AB'], row['H'], row['2B'], row['3B'], 
                              row['HR'], row['BB'], row['SO'], row['SF'], row['SH'], 
                              row['GDP'], row['SB'], row['CS']) for _, row in players.iterrows()]
        else:
            assert all(isinstance(player, Player) for player in players), "players must be a list of Player objects"
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
    def __init__(self, team1: Team, team2: Team, iterations: int):
        self.team1 = team1
        self.team2 = team2
        self.iterations = iterations
        self.iteration_log = pd.DataFrame()

    def simulate_inning(self, inning):
        
        runs_team1 = self.team1.simulate_inning()
        self.team1.runs += runs_team1
        
        runs_team2 = self.team2.simulate_inning()
        self.team2.runs += runs_team2

    def simulate_game(self):
        all_iterations_data = []
        for iteration in range(self.iterations):
            self.team1.runs = 0
            self.team2.runs = 0
            for inning in range(9):  # A standard game has 9 innings
                self.simulate_inning(inning)

            while self.team1.runs == self.team2.runs:  # Extra innings if tied
                self.simulate_inning(inning)
                inning += 1

            iteration_data = {
                'Iteration': iteration + 1,
                f'{self.team1.name} Runs': self.team1.runs,
                f'{self.team2.name} Runs': self.team2.runs,
                'Winner': self.team1.name if self.team1.runs > self.team2.runs else self.team2.name
            }
            all_iterations_data.append(iteration_data)
        
        self.iteration_log = pd.DataFrame(all_iterations_data)
        
        average_score_team1 = self.iteration_log[f'{self.team1.name} Runs'].mean()
        average_score_team2 = self.iteration_log[f'{self.team2.name} Runs'].mean()
        
        return {self.team1.name: average_score_team1, self.team2.name: average_score_team2}, self.iteration_log

if __name__ == "__main__":
    import lineup as lu
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", help="The date of the game to simulate in the format YYYY-MM-DD", default='2023-10-17')
    parser.add_argument("-t", "--team", help="The three-letter abbreviation of the team to simulate", default='PHI')
    parser.add_argument("-s", "--sims", help="The number of simulations to run", type=int, default=100)
    args = parser.parse_args()

    date = args.date
    team_abbr = args.team
    sims = args.sims

    team_lineup, opp_lineup = lu.get_lineups(date, team_abbr)
    
    lineup1 = Lineup(team_lineup)
    lineup2 = Lineup(opp_lineup)
    team1 = Team(team_lineup["Tm"].iloc[0], lineup1)
    team2 = Team(opp_lineup["Tm"].iloc[0], lineup2)

    game = Game(team1, team2, sims)
    ave_scores, iter_log = game.simulate_game()
    print(ave_scores)
    print(iter_log['Winner'].value_counts())