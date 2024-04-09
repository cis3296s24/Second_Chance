import pygame as pg
import sys

from src.constants import *
from src.states.state_manager import StateManager
from src.states.state import State

class Game:
    """The Game class contains the main game loop.
    """
    
    def __init__(self):
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pg.time.Clock()
        self.running = True
        
        # Load background music
        pg.mixer.music.load('assets/music/TestSong.mp3')
        # Set initial volume
        self.volume = 0.5  # Initial volume level (between 0 and 1)
        pg.mixer.music.set_volume(self.volume)
        pg.mixer.music.play(-1)  # Start playing background music on a loop
        pg.display.set_caption("Second Chance")
        
        self.load_assets()
        
        # Associate all States created afterward with this game object instance
        # and the game's state manager
        setattr(State, "game", self)
        self.manager = StateManager()
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
            self.manager.state.update(events)
            self.manager.state.draw()
            pg.display.update()
            self.clock.tick(FRAME_RATE)
            
    def load_assets(self):
        self.assets_dir = os.path.join("assets")
        self.character_dir = os.path.join(self.assets_dir, "characters")
        self.background_dir = os.path.join(self.assets_dir, "backgrounds")
        self.resources_dir = os.path.join("resources")
        self.csvs_dir = os.path.join("csvs")
        self.tiles_dir = os.path.join("tiles")

            
    def increase_volume(self):
        self.volume = min(self.volume + 0.1, 1.0)  # Increase self.volume by 0.1, but ensure it doesn't exceed 1.0
        pg.mixer.music.set_volume(self.volume)

    def decrease_volume(self):
        self.volume = max(self.volume - 0.1, 0.0)  # Decrease self.volume by 0.1, but ensure it doesn't go below 0.0
        pg.mixer.music.set_volume(self.volume)
            
if __name__ == "__main__":
    pg.init()
    g = Game()
    g.run()
    pg.quit()
    sys.exit()
    