import pygame as pg
import os
import random

from src.states.minigames.minigame import Minigame

from pygame.locals import *


class Memory(Minigame):
    """A minigame to test your memory."""

    def __init__(self):
        instructions = (
            "The goal of this minigame is to memorize the 5-character "
            "string that will appear and then disappear after 5 seconds. "
            "A text box will pop up and you will have to enter a 5-character "
            "string into it. You win the game if the 5-character "
            "string you entered matches the 5-character string that appeared "
            "on the screen."
        )

        img = "minigame2.jpg"

        super().__init__(
            instructions,
            img=os.path.join("minigames", img)
        )

        # Minigame specific attributes
        self.generated_string = ""
        self.input_string = ""
        self.input_rect = pg.Rect(200, 282, 200, 36)  # Adjusted position to center vertically
        self.input_active = False
        self.font = pg.font.SysFont(None, 36)
        self.generated_text_surf = None
        self.display_time = 10  # Time to display the generated string in seconds
        self.display_timer = 0  # Timer to track the display time
        self.is_string_currently_displayed = False
        self.was_string_displayed_yet = False
        self.clock = pg.time.Clock()
            
    def handle_events(self, events):
        super().handle_events(events) # To enable pause menu access
        for event in events:
            if event.type == pg.KEYDOWN and self.input_active:
                if event.key == pg.K_RETURN:
                    self.check_win_condition()
                elif event.key == pg.K_BACKSPACE:
                    self.input_string = self.input_string[:-1]
                else:
                    self.input_string += event.unicode

    def update(self, events):
        super().update(events)
        if not self.was_string_displayed_yet:
            self.generated_string = self.generate_random_string()
            self.generated_text_surf = self.font.render(self.generated_string, True, (255, 255, 255))
            self.was_string_displayed_yet = True
            self.is_string_currently_displayed = True
            self.display_timer = self.display_time * 1000  # Convert seconds to milliseconds
        elif self.was_string_displayed_yet:
            self.display_timer -= self.clock.tick()  # Update the timer
            if self.display_timer <= 0:
                self.generated_text_surf = None
                self.is_string_currently_displayed = False
                self.input_active = True

    def draw(self):
        super().draw() # Draw minigame background

        # Render and display generated string
        if self.generated_text_surf:
            self.screen.blit(self.generated_text_surf, ((self.screen.get_width() - self.generated_text_surf.get_width()) / 2, 200))

        # Draw input box if the generated string has disappeared
        if not self.is_string_currently_displayed and self.was_string_displayed_yet:
            pg.draw.rect(self.screen, (255, 255, 255), self.input_rect, 2)
            input_text_surf = self.font.render(self.input_string, True, (255, 255, 255))
            self.screen.blit(input_text_surf, (self.input_rect.x + 5, self.input_rect.y + 5))

    def generate_random_string(self):
        """Generates a random 5-character string."""
        characters = "abcdefghijklmnopqrstuvwxyz0123456789"
        return ''.join(random.choice(characters) for _ in range(5))

    def check_win_condition(self):
        """Checks if the input string matches the generated string."""
        if self.input_string == self.generated_string:
            self.won = True
            self.win_text = "You remembered the string!"
        else:
            self.won = False
