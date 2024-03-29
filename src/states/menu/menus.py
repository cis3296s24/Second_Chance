import pygame as pg

from ..state import State
from src.constants import *


class Menu(State):
    """A Menu is a type of state where the user can select from two or more
    options on the screen."""
    def __init__(self, options_img, options, header_text=None):
        super().__init__(options_img)
        self.font = pg.font.SysFont("georgia", 30)
        self.cursor_index = 0
        self.options_surface = pg.image.load(os.path.join(
            ASSETS_DIR, options_img))
    
        if header_text is not None:
            self.header_surface = self.font.render(header_text, False, "Black")

    def update_cursor(self):
        pass


class PlayMenu(Menu):
    def __init__(self):
        super().__init__("PlaYOpTiOns.png", options=["Play", "Options"])
        
    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                self.manager.set_state(OptionsMenu())
                

class OptionsMenu(Menu):
    def __init__(self):
        super().__init__("Options.png", ["Video", "Audio"])

    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                self.manager.set_state(PlayMenu())

    def update(self):
        pass


class SelectMode(Menu):
    def __init__(self):
        pass

    def handle_events(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass


class Party(Menu):
    def __init__(self):
        pass

    def handle_events(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass
