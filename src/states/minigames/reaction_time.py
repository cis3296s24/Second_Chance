import os
import random

import pygame as pg

from src.states.minigames.minigame import Minigame
from src.utils.timer import Timer


class ReactionTime(Minigame):
    """A minigame to test your reaction time."""

    def __init__(self):
        instructions = \
            "The goal of this minigame is to wait for a letter from a-z " \
            "to appear on the screen. You must press that key on " \
            "your keyboard as quick as possible. If you don't press the key " \
            "within 3 seconds after it has appeared, you lose."

        img = "minigame1.jpg"

        super().__init__(
            instructions,
            img=os.path.join("minigames", img)
        )

        # Minigame specific attributes
        self.reaction_timer = Timer()
        self.reaction_time = 0
        self.reaction_timer_started = False
        self.random_key = self.generate_random_key()
        self.random_key_name = pg.key.name(self.random_key)
        self.random_start_time = random.uniform(2, 6)
        self.key_display_text = self.get_text_surface(f"Press {self.random_key_name}", "green", 72)
        self.win_text = ""
        self.lose_text = ""

    def handle_events(self, events):
        super().handle_events(events)  # To enable pause menu access
        for event in events:
            if event.type == pg.KEYDOWN:

                # Win condition
                if event.key == self.random_key and self.reaction_timer.is_running:
                    self.reaction_timer.pause()
                    # The Minigame superclass handles this win condition when
                    # it calls its update() method, so we only need to set
                    # self.won = True and let the superclass deal with it.
                    self.won = True
                    self.win_text = f"Your reaction time was: {self.reaction_time}"

    def update(self, events):
        super().update(events)

        # Start reaction timer once random amount of time has passed
        if not self.reaction_timer_started:
            if self.timer.get_time(ms=True) >= self.random_start_time:
                self.reaction_timer.start()
                self.reaction_timer_started = True

        # Update reaction timer text
        if self.reaction_timer.is_running:
            self.reaction_time = self.reaction_timer.get_time(ms=True)
            self.reaction_timer_text = self.get_text_surface(
                f"Reaction timer: {self.reaction_time:.3f}", "white", 36)
            # The user loses if the elapsed time is greater than 3 seconds
            if self.reaction_timer.get_time(ms=True) > 3:
                self.won = False

    def draw(self):
        super().draw()  # Draw minigame background

        # Draw text
        if self.reaction_timer.is_running:
            self.screen.blit(self.reaction_timer_text, (20, 20))
            self.screen.blit(self.key_display_text,
                             ((self.screen.get_width() / 2) - 50, self.screen.get_height() / 2)
                             )

    def generate_random_key(self):
        """Generates a random lowercase key from a-z.

        Returns:
            int: A random number representing a pygame.KEY constant.
        """
        return random.choice([getattr(pg.locals, f'K_{chr(key)}') for key in range(ord('a'), ord('z') + 1)])

    def get_timer(self):
        """Returns the reaction timer."""
        return self.reaction_timer
