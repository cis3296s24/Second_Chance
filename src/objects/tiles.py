import pygame as pg

class Tile(pg.sprite.Sprite):
    """Sprite class to represent a tile.

    Args:
        image (pygame.Surface): Surface of the tile.
        x (int): x position to spawn tile.
        y (int): y position to spawn tile.
        tile_type (int): Type of tile used to load the corresponding tile image.
    """
    
    def __init__(self, image, x, y, tile_type):
        super().__init__()
        self.image = pg.image.load(f"assets/tiles/{tile_type}.png")
        self.image = image
        self.rect = self.image.get_rect(x=x, y=y)
        
    def update(self, scroll):
        """Updates the position of the tile.

        Args:
            scroll (int): Amount to update tile rect.
        """
        self.rect.x += scroll

    def _debug(self, screen):
        pg.draw.rect(screen, (255, 255, 255), self.rect, 2)