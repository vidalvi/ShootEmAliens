import pygame as pg
from pygame.sprite import Sprite


class AlienShip(Sprite):
    """A class representing a single space rock."""

    def __init__(self, game):
        """Initialize the space rock and set its starting position."""
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings

        # Load the space rock image and get its Rectangle attribute.
        self.image = pg.image.load(r'.\images\alien_ship.png')
        self.image = pg.transform.scale(self.image, (60, 35))
        self.rect = self.image.get_rect()

        # Place the space rock at the top-left of the screen with its width and height as spacing.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the space rock's exact horizontal position.
        self.x = float(self.rect.x)

    def hit_the_edge(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Move the alien right or left."""
        self.x += self.settings.alien_ship_speed * self.settings.fleet_direction
        self.rect.x = self.x
