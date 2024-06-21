import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class to manage bullets"""

    def __init__(self, ai_game):
        """Create bullet object at ship's current pos"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Create bullet rect at (0,0), set correct pos
        self.rect = pygame.Rect(
            0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Store bullet pos as float
        self.y = float(self.rect.y)

    def update(self):
        """Move bullet up to screen"""
        # Update bulet pos
        self.y -= self.settings.bullet_speed
        # Update rect pos
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw bullet to screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
