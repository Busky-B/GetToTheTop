import pygame
class Player(pygame.sprite.Sprite):
    def __init__(self, rect) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = self.image.load("./assets/MascotBunnyCharacter/Bunny1/__Bunny1_Idle_000.png")
        self.rect = rect