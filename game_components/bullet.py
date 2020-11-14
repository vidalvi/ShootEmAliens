import pygame as pg
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class to manage bullet fired from the ship."""

    def __init__(self, game):
        """Create a bullet at the ship's current position."""
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings

        self.image = pg.image.load(r'.\images\bullet.png')
        self.image = pg.transform.scale(self.image, (self.settings.bullet_width, self.settings.bullet_height))
        self.rect = self.image.get_rect()
        self.rect.midtop = game.ship.rect.midtop

        # Store the bullet's position as a decimal value.
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up the screen."""
        # Update the decimal position of the bullet.
        self.y -= self.settings.bullet_speed
        # Update the rect position.
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw bullet to the screen."""
        # pg.draw.rect(self.screen, self.color, self.rect)
        self.screen.blit(self.image, self.rect)
