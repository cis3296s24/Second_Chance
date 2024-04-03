import pygame as pg

from ..state import State
from .menus import StartMenu

class TitleScreen(State):
    def __init__(self):
        super().__init__("background.png")
        
    def handle_events(self, events: list[pg.event.Event]):
        for event in events:
            if event.type != pg.KEYDOWN:
                return
            if event.key == pg.K_RETURN:
                self.manager.set_state(StartMenu)
