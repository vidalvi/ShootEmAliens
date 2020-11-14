from game_components.ship import Ship
import pygame as pg
from pygame.sprite import Sprite


class ShipIndicator(Sprite):
    """A class that serves as indicator for the remaining ships before the game is over."""

    def __init__(self, game):
        super().__init__()

        self.ship = Ship(game)

        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        self.image = self.ship.img
        self.image_width, self.image_height = 12, 20
        self.image = pg.transform.scale(self.image, (self.image_width, self.image_height))
        self.rect = self.image.get_rect()
