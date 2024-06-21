import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent single alien"""

    def __init__(self, ai_game):
        """Initialize alien and set start point"""
        super().__init__()
        self.screen = ai_game.screen

        # Load lien image and set rect attribute
        self.image = pygame.image.load('./images/alien.bmp')
        self.rect = self.image.get_rect()

        # Start each new alien near top left screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store alien's exact horizontal pos
        self.x = float(self.rect.x)
