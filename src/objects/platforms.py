import pygame as pg

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.Surface((80, 20))
        self.image.fill("blue")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, scroll):
        self.rect.x += scroll