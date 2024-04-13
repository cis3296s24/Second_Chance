import pygame as pg
import os

from src.states.minigames.minigame import Minigame


class ReactionTime(Minigame):
    def __init__(self):
        instructions = \
            "The goal of this minigame is to wait for a keyboard button " \
            "that will appear on the screen, and then press that key on " \
            "your keyboard as quick as possible. If you are too slow, " \
            "you lose."

        img = "minigame1.jpg"

        super().__init__(
            instructions,
            img=os.path.join("minigames", img)
        )

    def handle_events(self, events):
        super().handle_events(events) # To enable pause menu access
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_o:
                    self.won = True

    def update(self, events):
        super().update(events)

    def draw(self):
        super().draw() # Draw minigame background
        self.screen.blit(
            self.get_text_surface("Just press 'o' to 'win' for now", "blue", 36), 
            (self.screen.get_width()/2, self.screen.get_height()/2)
        ) # TODO
        
