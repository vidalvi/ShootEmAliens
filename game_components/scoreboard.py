import json
import pygame.font as pg_font
from pygame.sprite import Group
from game_components.ship_indicator import ShipIndicator


class Scoreboard:
    def __init__(self, game):
        """Initialize score-keeping attributes."""
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.stats = game.stats

        # Font settings for scoring information.
        self.text_color = (249, 215, 28)
        self.font = pg_font.SysFont(None, 21)

        # Prepare the initial score image.
        self.prep_score()
        self.prep_high_score()
        self.prep_ship_indicator()

    def prep_score(self):
        score_str = f'SCORE: {self.stats.score}'
        self.score_img = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # Display the score at the top right of the screen
        self.score_rect = self.score_img.get_rect()
        self.score_rect.right = self.screen_rect.right - 5
        self.score_rect.top = 5

    def prep_high_score(self):
        high_score_str = f'HIGH SCORE: {self.stats.high_score}'
        self.high_score_img = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        # Display the score at the top right of the screen
        self.high_score_rect = self.high_score_img.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 5

    def prep_ship_indicator(self):
        self.remaining_ships = Group()
        for ship_num in range(self.stats.ships_left):
            ship = ShipIndicator(self.game)
            ship.rect.x = 5 + ship_num * ship.image_width
            ship.rect.y = 5
            self.remaining_ships.add(ship)

    def show_score(self):
        """Draw the score to the screen."""
        self.screen.blit(self.score_img, self.score_rect)
        self.screen.blit(self.high_score_img, self.high_score_rect)
        self.remaining_ships.draw(self.screen)

    def check_high_score(self):
        """Check and update high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
            with open(self.stats.saved_data_filename) as f:
                data_to_be_saved = json.load(f)
                data_to_be_saved["high_score"] = self.stats.score
            with open(self.stats.saved_data_filename, 'w') as f:
                json.dump(data_to_be_saved, f)
