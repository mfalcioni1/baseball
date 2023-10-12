import random

import random

class Player:
    def __init__(self, 
                 name: str, 
                 ab: int, 
                 h: int, 
                 b_1: int,
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

class Game:
    def __init__(self, lineup):
        self.lineup = lineup
    
    def simulate_game(self):
        total_runs = 0
        for inning in range(9):  # A standard game has 9 innings
            runs = self.lineup.simulate_inning()
            total_runs += runs
            print(f"Inning {inning + 1}: {runs} runs, Total: {total_runs} runs")
        return total_runs

if __name__ == "__main__":
    # Creating players with name and statistics
    player1 = Player("Player1", 300, 90, 60, 20, 5, 5, 30, 50, 5, 5, 5, 10, 5)
    player2 = Player("Player2", 310, 93, 63, 20, 5, 5, 32, 48, 5, 5, 5, 11, 5)
    player3 = Player("Player3", 320, 96, 66, 20, 5, 5, 34, 46, 5, 5, 5, 12, 5)
    player4 = Player("Player4", 330, 99, 69, 20, 5, 5, 36, 44, 5, 5, 5, 13, 5)
    player5 = Player("Player5", 340, 102, 72, 20, 5, 5, 38, 42, 5, 5, 5, 14, 5)
    player6 = Player("Player6", 350, 105, 75, 20, 5, 5, 40, 40, 5, 5, 5, 15, 5)
    player7 = Player("Player7", 360, 108, 78, 20, 5, 5, 42, 38, 5, 5, 5, 16, 5)
    player8 = Player("Player8", 370, 111, 81, 20, 5, 5, 44, 36, 5, 5, 5, 17, 5)
    player9 = Player("Player9", 380, 114, 84, 20, 5, 5, 46, 34, 5, 5, 5, 18, 5)

    # Creating a lineup
    lineup = Lineup([player1, player2, player3, player4, player5, player6, player7, player8, player9])

    # Simulating a game
    game = Game(lineup)
    total_runs = game.simulate_game()

    print(f"\nTotal runs scored in the game: {total_runs}")
