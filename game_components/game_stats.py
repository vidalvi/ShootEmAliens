import json


class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, game):
        """Initialize statistics."""
        self.settings = game.settings
        self.reset_stats()
        self.game_active = False
        self.saved_data_filename = r'.\saved_files\saved_data.json'
        self._get_high_score()

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0

    def _get_high_score(self):
        try:
            with open(self.saved_data_filename) as f:
                pass
        except FileNotFoundError:
            data_to_be_saved = {'high_score': 0, }
            with open(self.saved_data_filename, 'w') as f:
                json.dump(data_to_be_saved, f)
        finally:
            with open(self.saved_data_filename) as f:
                self.high_score = json.load(f).get('high_score')
