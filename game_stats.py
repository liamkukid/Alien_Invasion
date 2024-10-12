class GameStats:
    def __init__(self, ai_game):
        self.settigs = ai_game.settings
        self.reset_stats()

    def reset_stats(self):
        self.ships_left = self.settigs.ship_limit