import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullets import Bullets
from aliens import Aliens
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    """Overall class to manage game assets and behaviour."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.game_active = False
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        self.play_button = Button(self, "Play")

        self.stats = GameStats(self)
        self.bullets = Bullets(self)
        self.ship = Ship(self)
        self.aliens = Aliens(self)
        self.sb = Scoreboard(self)

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.bullets.draw()
        self.ship.blitme()
        self.aliens.draw()
        self.sb.show_score()
        if not self.game_active:
            self.play_button.draw_button()

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
        elif event.key == pygame.K_p:
            self._play()

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
        collisions = pygame.sprite.groupcollide(self.bullets.group, self.aliens.group, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens.group:
            self.bullets.empty()
            self.aliens.create_fleet()
            self.settings.increase_speed()

    def _check_alien_ship_collisions(self):
        if pygame.sprite.spritecollideany(self.ship, self.aliens.group):
            self._ship_hit()

    def _ship_hit(self):
        if self.stats.ships_left > 1:
            self.stats.ships_left -= 1
            self._reset()
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)
    
    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self._play()
            self.settings.initialize_dynamic_settings()

    def _play(self):
        self.stats.reset_stats()
        self.game_active = True
        self._reset()
        self.sb.prep_score()
        pygame.mouse.set_visible(False)

    def _reset(self):
            self.bullets.empty()
            self.aliens.empty()
            self.aliens.create_fleet()
            self.ship.center_ship()

if __name__ == '__main__':
    #Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
    