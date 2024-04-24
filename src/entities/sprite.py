import pygame as pg


class Sprite(pg.sprite.Sprite):
    """A general sprite class to represent a drawable object with
    pygame.Surface and pygame.Rect attributes."""

    def __init__(self, surface: pg.Surface, rect: pg.Rect):
        super().__init__()
        self.surface = surface
        self.rect = rect
