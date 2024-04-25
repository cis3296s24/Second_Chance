import pygame as pg


class Tile(pg.sprite.Sprite):
    def __init__(self, image, x, y, tile_type):
        super().__init__()
        self.image = pg.image.load(f"assets/tiles/{tile_type}.png")
        self.image = image
        self.rect = self.image.get_rect(x=x, y=y)

    def update(self, scroll):
        self.rect.x += scroll

    def debug(self, screen):
        pg.draw.rect(screen, (255, 255, 255), self.rect, 2)
