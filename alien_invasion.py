import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullets import Bullets
from aliens import Aliens

class AlienInvasion:
    """Overall class to manage game assets and behaviour."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.game_active = True
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        self.stats = GameStats(self)
        self.bullets = Bullets(self)
        self.ship = Ship(self)
        self.aliens = Aliens(self)

        self.aliens.create_fleet()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            
            if self.game_active:
                self.ship.update()
                self.bullets.update()
                self.aliens.update()
                self._check_collisions()

            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Responde to keypress and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.bullets.draw()
        self.ship.blitme()
        self.aliens.draw()
        pygame.display.flip()

    def _check_keydown_events(self, event):
        if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self.bullets.fire()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_collisions(self):
        self._check_bullet_alien_collisions()
        self._check_alien_ship_collisions()
        if self.aliens.is_bottom_was_touched():
            self._ship_hit()

    def _check_bullet_alien_collisions(self):        
        collisions = pygame.sprite.groupcollide(self.bullets.bullets, self.aliens.aliens, True, True)
        if not self.aliens.aliens:
            self.bullets.empty()
            self.aliens.create_fleet()

    def _check_alien_ship_collisions(self):
        if pygame.sprite.spritecollideany(self.ship, self.aliens.aliens):
            self._ship_hit()

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.bullets.empty()
            self.aliens.empty()
            self.aliens.create_fleet()
            self.ship.center_ship()

            sleep(0.5)
        else:
            self.game_active = False

if __name__ == '__main__':
    #Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
    