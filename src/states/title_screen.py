import pygame as pg

from .state import State
from .menu.menus import PlayMenu

class TitleScreen(State):
    def __init__(self):
        super().__init__("TitleScreen.png")
        
    def handle_events(self, event: pg.event.Event):
        if event.type != pg.KEYDOWN:
            return
        
        if event.key == pg.K_RETURN:
            self.manager.set_state(PlayMenu())
