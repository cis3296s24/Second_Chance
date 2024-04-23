import pygame as pg

class Portal(pg.sprite.Sprite):
    def __init__(self, x, y, image_path, width, height):
        super().__init__()
        self.original_image = pg.image.load(image_path).convert_alpha()
        self.image = pg.transform.scale(self.original_image, (width, height))  # Scale the image to the desired size
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, scroll):
        self.rect.x += scroll