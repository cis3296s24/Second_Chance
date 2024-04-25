import pygame as pg


class Platform(pg.sprite.Sprite):
    """Sprite class to represent a platform.

    Args:
        x (int): x position to spawn at.
        y (int): y position to spawn at.
    """

    def __init__(self, x, y):
        super().__init__()
        self.image = pg.Surface((80, 20))
        self.image.fill("blue")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        """Draws the platform onto the screen.

        Args:
            screen (pygame.Surface): Screen to draw platform on.
        """
        screen.blit(self.image, self.rect)

    def update(self, scroll):
        """Updates the position of the platform.

        Args:
            scroll (int): Amount to update platform rect.
        """
        self.rect.x += scroll
