import pygame as pg
import sys

from constants import *
from states.state_manager import StateManager
from states.state import State

class Game:
    """The Game class contains the main game loop.
    """
    
    def __init__(self):
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pg.time.Clock()
        self.manager = StateManager()
        self.running = True
        # Associate all States created afterward with this game object instance
        # and the game's state manager
        setattr(State, "game", self)
        setattr(State, "manager", self.manager)

    def run(self):
        while self.running:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.K_ESCAPE:
                    self.running = False

            self.manager.state.handle_events(events)
            self.manager.state.update()
            self.manager.state.draw()
            pg.display.update()
            self.clock.tick(FRAME_RATE)
            
    def load_assets(self):
        pass
            
if __name__ == "__main__":
    pg.init()
    g = Game()
    g.run()
    pg.quit()
    sys.exit()
