import pygame as pg

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.Surface((80, 20))
        self.image.fill("blue")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.should_debug = True # TODO
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, scroll):
        self.rect.x += scroll
        
    def debug(self, screen): # TODO
        text = f"""
            (x, y): {self.rect.x, self.rect.y}
        """
        font = pg.font.Font(None, 20).render(text, True, "blue")
        screen.blit(font, (0, screen.get_height() - 50))