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

    def update(self, events):
        super().update(events) # To check if instructions are enabled

    def draw(self):
        super().draw() # Draw minigame background
