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
    
    def __init__(self, img=None):
        self.screen = pg.display.get_surface()
        if img is not None:
            self.surface = pg.image.load(os.path.join(self.game.background_dir, img))
            self.surface = pg.transform.scale(self.surface, ((SCREEN_WIDTH, SCREEN_HEIGHT)))
        else:
            self.surface = pg.Surface()
        
    def handle_events(self, events):
        for event in events:
            pass # Handle events here

    def update(self, events):
        pass

    def draw(self):
        self.screen.blit(self.surface, (0, 0))
