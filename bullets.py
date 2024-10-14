import pygame

from bullet import Bullet

class Bullets:

    def __init__(self, ai_game):
        self.__bullets = pygame.sprite.Group()
        self.group = self.__bullets
        self.settings = ai_game.settings
        self.ai_game = ai_game

    def update(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.__bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.__bullets.copy():
            if bullet.rect.bottom <= 0:
                self.__bullets.remove(bullet)

    def draw(self):
        for bullet in self.__bullets.sprites():
            bullet.draw_bullet()

    def fire(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.__bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self.ai_game)
            self.__bullets.add(new_bullet)

    def empty(self):
        self.__bullets.empty()