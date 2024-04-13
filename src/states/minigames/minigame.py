import pygame as pg
import pygame_menu
import time

import src.states.menu.menus as menu
from src.states.state import State


class Minigame(State):
    """Base class for a minigame."""

    def __init__(self, instructions: str, img=None):
        super().__init__(img)
        self.instructions = instructions
        self.instructions_enabled = True

    def handle_events(self, events):
        for event in events:
            if event.type != pg.KEYDOWN:
                return
            if event.key == pg.K_ESCAPE:
                self.manager.set_state(menu.PauseMenu, save_prev=True)

    def update(self, events):
        if self.instructions_enabled:
            self.manager.set_state(MinigameInstructions(self.instructions), save_prev=True)
            self.instructions_enabled = False

    def draw(self):
        super().draw()  # Draw default background passed in as img parameter

class MinigameInstructions(State):
    """State that holds and displays a pygame_menu.Menu object, to not interfere
    with base Minigame class.
    """

    def __init__(self, instructions: str):
        super().__init__()
        self.menu = self.create_menu(instructions)

    def handle_events(self, events):
        if self.menu.is_enabled:
            self.menu.update(events)

        for event in events:
            if event.type != pg.KEYDOWN:
                return
            if event.key == pg.K_ESCAPE:
                self.manager.set_state(menu.PauseMenu, save_prev=True)

    def draw(self):
        if self.menu.is_enabled():
            self.menu.draw(self.screen) # pygame_menu needs self.screen parameter for some reason

    def create_menu(self, instructions: str):
        menu = pygame_menu.Menu('Instructions', 600, 350,
                                theme=pygame_menu.themes.THEME_BLUE)

        menu.add.label(instructions, max_char=-1, font_size=25, wordwrap=True)
        menu.add.button('Okay', self.manager.set_state, Countdown)

        return menu


class Countdown(State):
    """State to display a countdown before the minigame starts.
    TODO Preferable behavior is to display countdown on top of current minigame state.
    """

    def __init__(self, img=None):
        super().__init__(img)
        self.text = self.get_text_surface(str(3), "white", font_size=72)
        self.pos = (self.screen.get_width() / 2, self.screen.get_height() / 2)
        self.start_time = time.time() - 1  # initialize starting time
        self.elapsed_time = 0

    def update(self, events):
        self.elapsed_time = time.time() - self.start_time
        text = ""

        if self.elapsed_time > 5.5:
            self.manager.pop_state() # Go back to minigame
        elif self.elapsed_time > 4:
            text = "GO!"
            self.pos = ((self.screen.get_width() / 2)-40, self.pos[1]) # Readjust when it displays GO
        elif 4 >= self.elapsed_time >= 1:
            text = str(int(self.elapsed_time))

        self.text = self.get_text_surface(text, "white", font_size=72)

    def draw(self):
        self.screen.fill("black")
        self.screen.blit(self.text, self.pos)
