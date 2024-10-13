import pygame

from bullet import Bullet

class Bullets:

    def __init__(self, ai_game):
        self.bullets = pygame.sprite.Group()
        self.settings = ai_game.settings
        self.ai_game = ai_game

    def update(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def draw(self):
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

    def fire(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self.ai_game)
            self.bullets.add(new_bullet)

    def empty(self):
        self.bullets.empty()