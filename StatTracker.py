class StatTracker:

    def __init__(self):

        self.wins = {}
        self.losses = {}
        self.draws = {}
        self.total_games = 0
        self.aborts = 0
        self.rematch_streaks = {}

    def update(self, result, by, opponent):

        if result == 'win':
            self.wins[by] = self.wins.get(by, 0) + 1
            self.total_games += 1

        elif result == 'loss':
            
            self.losses[by] = self.losses.get(by, 0) + 1
            self.total_games += 1

        elif result == 'draw':
            self.draws[by] = self.draws.get(by, 0) + 1
            self.total_games += 1

        else:

            self.aborts += 1

        self.rematch_streaks[opponent] = self.rematch_streaks.get(opponent, 0) + 1

    def print_stats(self):

        print(str(self.wins))
        print("Win/Draw/Loss: " + str(sum(self.wins.values())) + "/" + str(sum(self.draws.values())) + "/" + str(sum(self.losses.values())))
        print(str(self.rematch_streaks))