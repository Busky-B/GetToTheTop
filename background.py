import pygame
class Background:
    def __init__(self, img_path, img_location):
        self.image = pygame.image.load(img_path)
        self.rect  = self.image.get_rect()
        self.rect.left, self.rect.top = img_location # formatted as [x, y]