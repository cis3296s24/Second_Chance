import pygame as pg

from src.states.state import State
from src.constants import *
from ..levels.level1_1 import Level1_1

# Not using relative import to handle circular import issue when importing TitleScreen
# TODO Fix this later
import src.states.menu.title_screen as ts

class StartMenu(State):
    def __init__(self):
        super().__init__("background.png") # Change to start menu background
        # Initialize menu here
        
    def handle_events(self, events):
        for event in events:
            if event.type != pg.KEYDOWN:
                return
            if event.key == pg.K_BACKSPACE:
                self.manager.set_state(ts.TitleScreen)
            if event.key == pg.K_RETURN:
                self.manager.set_state(Level1_1)
    
class OptionsMenu(State):
    def __init__(self):
        super().__init__()

    def handle_events(self, events):
        pass

    def update(self):
        pass
