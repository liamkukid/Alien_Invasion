import pygame

from alien import Alien

class Aliens:
    def __init__(self, ai_game):
        self.aliens = pygame.sprite.Group()
        self.settings = ai_game.settings
        self.ai_game = ai_game
        self.screen = ai_game.screen

    def create_fleet(self):
        """Create the fleet of aliens."""
        alien = Alien(self.ai_game)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height

        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_possition, y_possition):
        new_alien = Alien(self)
        new_alien.x = x_possition
        new_alien.rect.x = x_possition
        new_alien.rect.y = y_possition
        self.aliens.add(new_alien)

    def update(self):
        self._check_fleet_edges()
        self.aliens.update()

    def draw(self):
        self.aliens.draw(self.screen)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def empty(self):
        self.aliens.empty()

    def is_bottom_was_touched(self):
        for alien in self.aliens:
            if alien.rect.bottom >= self.settings.screen_height:
                return True
        return False
                