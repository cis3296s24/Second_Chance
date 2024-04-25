import pygame as pg

class Portal(pg.sprite.Sprite):
    """Sprite class to represent a portal.

    Args:
        x (int): x position to spawn at.
        y (int): y position to spawn at.
        image_path (str): Full path to portal image.
        width (int): Width of portal image.
        height (int): Height of portal image.
    """
    
    def __init__(self, x, y, image_path, width, height):
        super().__init__()
        self.original_image = pg.image.load(image_path).convert_alpha()
        self.image = pg.transform.scale(self.original_image, (width, height))  # Scale the image to the desired size
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        """Draws the portal onto the screen.

        Args:
            screen (pygame.Surface): Screen to draw portal on.
        """
        screen.blit(self.image, self.rect)

    def update(self, scroll):
        """Updates the position of the portal.

        Args:
            scroll (int): Amount to update portal rect.
        """
        self.rect.x += scroll