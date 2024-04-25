import os
import random

import pygame as pg

from src.states.minigames.minigame import Minigame
from src.utils.timer import Timer

# Define colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Set the dimensions of the game window
WIDTH = 800
HEIGHT = 600


class FlyingGreen(Minigame):
    """A minigame where you must click on a circle before time runs out."""

    def __init__(self):

        instructions = \
            "The goal of this minigame is to click the flying green circle before time runs out" \
            "You must left click it within 3 seconds in order to achieve your second chance."

        img = "stars.jpg"

        super().__init__(
            instructions,
            img=os.path.join("minigames", img)
        )

        self.timer = Timer()
        self.timer_text = self.get_text_surface(
            f"Time: {self.timer.get_time(ms=True)}", "white", 36)
        self.target_circle = TargetCircle()
        self.win_text = ""
        self.lose_text = ""

    def handle_events(self, events):
        super().handle_events(events)
        for event in events:

            if event.type == pg.MOUSEBUTTONDOWN:
                if self.target_circle.is_clicked(event.pos):
                    self.timer.pause()
                    # self.target_circle.pause()
                    self.won = True
            if self.timer.get_time(ms=True) >= 3000:  # 3 seconds timeout
                self.won = False  # Set to False when time runs out

    def update(self, events):
        super().update(events)
        self.timer_text = self.get_text_surface(
            f"Time: {self.timer.get_time(ms=True):.3f}",
            "white", 36)

        if self.timer.get_time(ms=True) > 3:  # 3 seconds timeout
            self.won = False  # Set to False when time runs out

        if self.won is not None and self.won:  # Check if the game is won
            self.timer.pause()
        elif self.won is False:  # Check if the game is lost
            self.timer.pause()

        self.target_circle.update()

    def draw(self):
        super().draw()  # Draw default background passed in as img parameter
        if (self.timer.is_running):
            self.screen.blit(self.timer_text, (self.screen.get_width() - 190, 20))
            self.target_circle.draw(self.screen)


class TargetCircle:
    """Represents the moving green circle that the player must click."""

    def __init__(self):
        self.radius = 20
        self.pos = [random.randint(self.radius, WIDTH - self.radius), random.randint(self.radius, HEIGHT - self.radius)]
        self.speed = 2
        self.direction = [random.choice([-1, 1]), random.choice([-1, 1])]

    def update(self):
        """Update the position of the circle."""

        self.pos[0] += self.speed * self.direction[0]
        self.pos[1] += self.speed * self.direction[1]

        # If the circle reaches the window boundaries, change direction
        if self.pos[0] <= self.radius or self.pos[0] >= WIDTH - self.radius:
            self.direction[0] *= -1
        if self.pos[1] <= self.radius or self.pos[1] >= HEIGHT - self.radius:
            self.direction[1] *= -1

    def draw(self, screen):
        """Draw the circle on the screen."""

        pg.draw.circle(screen, GREEN, (int(self.pos[0]), int(self.pos[1])), self.radius)

    def is_clicked(self, click_pos):
        """Checks if the circle is clicked.

        Args:
            click_pos: (x, y) position of where the mouse was clicked.

        Returns:
            bool: True if the user clicked within the circle's radius.
        """

        distance = ((self.pos[0] - click_pos[0]) ** 2 + (self.pos[1] - click_pos[1]) ** 2) ** 0.5
        return distance <= self.radius
