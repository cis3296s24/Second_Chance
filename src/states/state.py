import pygame as pg

from src.constants import *

class State:
    """
    The State class represents all of the different states that the game
    can be in.
    
    :param img: An optional image to be displayed on the screen.
    """
    
    game = None
    manager = None
    
    def __init__(self, img=None, imgArr = None):
        self.bg_images = []
        self.screen = pg.display.get_surface()
        if img is not None:
            self.surface = pg.image.load(os.path.join(self.game.background_dir, img))
            self.surface = pg.transform.scale(self.surface, ((SCREEN_WIDTH, SCREEN_HEIGHT)))
        elif imgArr is not None:
            for i in range(1,6): 
                bg_image = pg.image.load(f"assets/backgrounds/plx-{i}.png").convert_alpha()
                bg_image = pg.transform.smoothscale(bg_image, self.screen.get_size())
                self.bg_images.append(bg_image)
                self.bg_width = self.bg_images[0].get_width()
        else:
            self.surface = pg.Surface() 
        
    def handle_events(self, events):
        for event in events:
            pass # Handle events here

    def update(self, events):
        pass

    def draw(self):
        self.screen.blit(self.surface, (0, 0))
    
    def draw_bg(self):
        for x in range(25):
                speed = 1
                for i in self.bg_images:
                    self.screen.blit(i, ((x * self.bg_width) - self.player.scroll * speed, 0))
                    speed += 0.2
