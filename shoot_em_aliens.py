import os
import sys
from time import sleep
import pygame as pg

from game_components.settings import Settings
from game_components.ship import Ship
from game_components.bullet import Bullet
from game_components.alien_ship import AlienShip
from game_components.game_stats import GameStats
from game_components.button import Button
from game_components.scoreboard import Scoreboard
from game_components.ship_indicator import ShipIndicator


class ShootEmAliens:
    def __init__(self):
        """Overall class to manage game assets and behavior."""
        pg.init()

        self.settings = Settings()

        self.screen = pg.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pg.display.set_caption("Shoot 'em Aliens!")

        # Create an instance to store game statistics.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pg.sprite.Group()
        self.fleet = pg.sprite.Group()

        self.remaining_ships = pg.sprite.Group()
        self.ship_indicator = ShipIndicator(self)

        pg.display.set_icon(self.ship.img)

        self._create_fleet()
        self.play_button = Button(self, 'PLAY')

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_event()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_fleet()

            self._update_screen()

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)

        # for bullet in self.bullets.sprites():
        #     bullet.draw_bullet()
        self.bullets.draw(self.screen)
        self.fleet.draw(self.screen)
        self.ship.blit_me()
        self.remaining_ships.draw(self.screen)
        self.sb.show_score()

        if not self.stats.game_active:
            self.play_button.draw_button()

        pg.display.flip()

    def _check_event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pg.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        if event.key == pg.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pg.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pg.K_SPACE:
            self._fire_bullet()
        elif event.key == pg.K_ESCAPE:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pg.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pg.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks PLAY button."""

        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game statistics
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_ship_indicator()

            # Reset the game settings.
            self.settings.initialize_dynamic_settings()

            # Get rid of remaining alien ships and bullets.
            self.bullets.empty()
            self.fleet.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor after pressing play button.
            pg.mouse.set_visible(False)

    def _fire_bullet(self):
        """Create an instance of Bullet to fire and add it to Bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update the position of the bullets and remove bullets that have disappeared."""
        # Update position of bullets.
        self.bullets.update()

        # Remove the bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_ship_collisions()

    def _check_bullet_alien_ship_collisions(self):
        """Check for bullet and alien ship collisions and remove them. """
        # Remove the alien ship if a bullet hits.
        collision = pg.sprite.groupcollide(self.bullets, self.fleet, True, True)
        if collision:
            self.stats.score += self.settings.point
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.fleet:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

    def _create_fleet(self):
        """Create fleet of alien ships."""
        # Create an alien ship to gather its size.
        alien_ship = AlienShip(self)
        alien_ship_width, alien_ship_height = alien_ship.rect.size

        # Calculates the number of alien ships in a row.
        available_space_x = self.settings.screen_width - (2 * alien_ship_width)
        num_alien_ship_x = available_space_x // (2 * alien_ship_width)

        # Calculates the rows of alien ships.
        available_space_y = self.settings.screen_height - self.ship.rect.height - (3 * alien_ship_height)
        num_rows_alien_ships = available_space_y // (2 * alien_ship_height)

        for alien_ship_row in range(num_rows_alien_ships):
            for alien_ship_num in range(num_alien_ship_x):
                self._create_alien_ship(alien_ship_num, alien_ship_row)

    def _create_alien_ship(self, alien_ship_num, alien_ship_row):
        """Create an individual alien ship."""
        alien_ship = AlienShip(self)
        alien_ship_width, alien_ship_height = alien_ship.rect.size

        # Set the horizontal position of alien ship.
        alien_ship.x = alien_ship_width * (1 + (2 * alien_ship_num))
        alien_ship.rect.x = alien_ship.x

        # Set the vertical position of the ship.
        alien_ship.rect.y = alien_ship_height * (1 + (2 * alien_ship_row))

        self.fleet.add(alien_ship)

    def _update_fleet(self):

        self._check_fleet_edges()
        self.fleet.update()

        # Look for ship and alien ship collisions.
        if pg.sprite.spritecollideany(self.ship, self.fleet):
            print('Ship hit!')
            self._losing_ship_response()

        # Look for aliens hitting the bottom of the screen.
        self._check_alien_ship_hits_bottom()

    def _check_fleet_edges(self):
        """Check if any of the alien ships in the fleet hit the edges of the screen."""

        for alien in self.fleet.sprites():
            if alien.hit_the_edge():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change its direction."""

        for alien_ship in self.fleet.sprites():
            alien_ship.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _losing_ship_response(self):
        """Response when an alien ship hits the ship or reaches bottom of the screen."""

        if self.stats.ships_left > 0:
            # Decrement the ships left.
            self.stats.ships_left -= 1
            self.sb.prep_ship_indicator()

            # Remove the remaining bullets and alien ships.
            self.bullets.empty()
            self.fleet.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(1.0)

        else:
            self.stats.game_active = False
            pg.mouse.set_visible(True)

    def _check_alien_ship_hits_bottom(self):
        """Check if any alien ship hits the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien_ship in self.fleet:
            if alien_ship.rect.bottom >= screen_rect.bottom:
                # Treat as if the ship got hit.
                self._losing_ship_response()
                break


if __name__ == '__main__':
    position = 5, 30
    os.environ['SDL_VIDEO_WINDOW_POS'] = f'{position[0]},{position[1]}'
    my_game = ShootEmAliens()
    my_game.run_game()
