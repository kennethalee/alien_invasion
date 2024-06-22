class GameStats:
    """Track stats for Alien Invasion"""

    def __init__(self, ai_game):
        """Initialize statistics"""
        self.settings = ai_game.settings
        self.reset_stats()

        # High score (never reset)
        self.high_score = 0

    def reset_stats(self):
        """Initialize statsw that can change during game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
