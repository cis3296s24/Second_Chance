import pygame as pg


class Sprite(pg.sprite.Sprite):
    """A general sprite class to represent a drawable object or character.

    Args:
        surface (pygame.Surface): Surface of the sprite.
        rect (pygame.Rect): Rect of the sprite.
    """

    def __init__(self, surface: pg.Surface, rect: pg.Rect):
        super().__init__()
        self.surface = surface
        self.rect = rect
