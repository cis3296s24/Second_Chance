import pygame as pg
import os
import random

from src.states.minigames.minigame import Minigame
from src.utils.timer import Timer

from pygame.locals import *

class Reflexes(Minigame):
    """A minigame to test your reflexes"""

    def __init__(self):
        instructions = (
            "The goal of this minigame is to click on the three squares "
            "that will pop up on the screen in random locations after the "
            "countdown. You will have 3 seconds to click all 3 squares after "
            "they pop up on the screen."
        )

        img = "minigame3.jpg"

        super().__init__(
            instructions,
            img=os.path.join("minigames", img)
        )

        # Minigame specific attributes
        self.squares = []  # List to store square positions
        self.square_size = 50
        self.square_color = (255, 0, 0)  # Red color for squares
        self.num_squares = 3
        self.display_time = 5  # Time to display squares in seconds
        self.display_timer = 0  # Timer to track the display time
        self.clicked_squares = []  # List to store clicked squares
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont(None, 36)
        self.game_timer = 0
        self.timer = Timer()

    def handle_events(self, events):
        super().handle_events(events)  # To enable pause menu access
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                # Check if the click is inside any of the squares
                for square in self.squares:
                    if square.collidepoint(event.pos):
                        if square not in self.clicked_squares:
                            self.clicked_squares.append(square)

    def update(self, events):
        super().update(events)

        # Update game timer
        self.game_timer += self.clock.get_time()

        if self.display_timer <= 0 and len(self.squares) < self.num_squares:
            # Generate a new square if the display time is over and there are fewer than 3 squares
            self.generate_square()
            self.display_timer = self.display_time * 1000  # Reset the display timer

        self.display_timer -= self.clock.get_time()  # Update the display timer

        if len(self.clicked_squares) == self.num_squares:
            # If all squares are clicked, the player wins
            self.won = True
            self.win_text = ""

        if self.timer.get_time(ms=True) > 3:
            self.won = False

    def draw(self):
        super().draw()  # Draw minigame background

        # Draw squares
        for square in self.squares:
            if square not in self.clicked_squares:
                pg.draw.rect(self.screen, self.square_color, square)

    def generate_square(self):
        """Generate three squares at random positions on the screen."""
        for _ in range(self.num_squares - len(self.squares)):  # Generate until we have three squares
            while True:
                x = random.randint(0, self.screen.get_width() - self.square_size)
                y = random.randint(0, self.screen.get_height() - self.square_size)
                new_square = pg.Rect(x, y, self.square_size, self.square_size)
                if not any(new_square.colliderect(square) for square in self.squares):
                    self.squares.append(new_square)
                    break
