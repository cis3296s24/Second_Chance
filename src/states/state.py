import pygame as pg

from src.constants import *

class State:
    def __init__(self, img=None):
        self.screen = pg.display.get_surface()
        if img is not None:
            self.surface = pg.image.load(os.path.join(ASSETS_DIR, img))
            self.surface = pg.transform.scale(self.surface, ((SCREEN_WIDTH, SCREEN_HEIGHT)))

    # TODO change_state()

    def handle_events(self, event):
        pass

    def update(self):
        pass

    def draw(self):
        self.screen.blit(self.surface, (0, 0))
