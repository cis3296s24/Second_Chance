import pygame as pg

from ..state import State
from .menus import StartMenu

class TitleScreen(State):
    def __init__(self):
        super().__init__("background.png")

        # Load background music
        pg.mixer.music.load('assets/music/titlescreenmusic.mp3')
        # Set initial volume
        self.volume = 0.5  # Initial volume level (between 0 and 1)
        pg.mixer.music.set_volume(self.volume)
        pg.mixer.music.play(-1)  # Start playing background music on a loop
        
    def handle_events(self, events: list[pg.event.Event]):
        for event in events:
            if event.type != pg.KEYDOWN:
                return
            if event.key == pg.K_RETURN:
                self.manager.set_state(StartMenu)

    def draw(self):
        super().draw()
        self.screen.blit(
            pg.font.Font(None, 36).render("Press 'Enter' to start", True, "black"),
            (self.screen.get_width()/2, self.screen.get_height()-100)   
        )