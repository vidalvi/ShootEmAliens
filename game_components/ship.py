import pygame as pg


class Ship:

    def __init__(self, game):
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the appearance of the ship.
        self.img = pg.image.load(r'.\images\spaceship.png')
        self.img = pg.transform.scale(self.img, (30, 50))
        self.rect = self.img.get_rect()

        self.settings = game.settings

        # Set the starting position of the ship to the center at the bottom of the screen.
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

        # Flags for movement of the ship.
        self.moving_right = False
        self.moving_left = False

    def blit_me(self):
        self.screen.blit(self.img, self.rect)

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x

    def center_ship(self):
        """Place the ship in the bottom-center of the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
