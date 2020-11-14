import pygame as pg


class Settings:
    def __init__(self):
        """Initialize the game's static settings."""
        # Screen Settings
        self.bg_color = (0, 0, 0)
        self.screen_width = 600
        self.screen_height = 700

        # Ship Settings
        self.ship_speed = 1.0
        self.ship_limit = 3

        # Bullet Settings
        self.bullet_speed = 1.5
        self.bullet_height = 25
        self.bullet_width = 15
        self.bullets_allowed = 3

        # Alien Ship Settings
        self.fleet_drop_speed = 10

        # How quickly the game speeds up.
        self.speedup_scale = 1.1

        # Score Settings
        self.point = 1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.alien_ship_speed = 0.5

        # fleet_direction of 1 means right while -1 means left
        self.fleet_direction = 1

    def increase_speed(self):
        self.alien_ship_speed *= self.speedup_scale
