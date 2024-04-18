import pygame as pg
import os
import random

from src.states.minigames.minigame import Minigame
from src.utils.timer import Timer

from pygame.locals import * # To get all 


# Define colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Set the dimensions of the game window
WIDTH = 600
HEIGHT = 400

class FlyingGreen(Minigame):
    """Base class for a minigame."""

    def __init__(self):
      
        instructions = \
            "The goal of this minigame is to click the flying green circle before time runs out" \
            "You must left click it within 3 seconds in order to achieve your second chance." 
        
        img = "stars.jpg"

        super().__init__(
            instructions,
            img=os.path.join("minigames", img)
        )
        self.won = None
     
        self.timer = Timer()
        self.timer_text = self.get_text_surface(
            f"Time: {self.timer.get_time(ms=True)}", "white", 36)
        self.target_circle = TargetCircle(self.timer)
        self.win_text = ""
        self.lose_text = ""

    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.target_circle.is_clicked(event.pos):
                    self.won = True

    def update(self, events):
        super().update(events)
        self.timer_text = self.get_text_surface(
            f"Time: {self.timer.get_time(ms=True):.3f}",
            "white", 36)


        if self.won:
            self.timer.pause()
            self.win()
        elif self.timer.get_time(ms=True) >= 3000:  # 3 seconds timeout
            self.lose()

        self.target_circle.update()

    def draw(self):
        super().draw()  # Draw default background passed in as img parameter
        if(self.timer.is_running):
            self.screen.blit(self.timer_text, (self.screen.get_width() - 190, 20))
            self.target_circle.draw(self.screen)









class TargetCircle:
    """Represents the moving green circle that the player must click"""

    def __init__(self, timer):
        self.radius = 20
        self.pos = [random.randint(self.radius, WIDTH - self.radius), random.randint(self.radius, HEIGHT - self.radius)]
        self.speed = 2
        self.direction = [random.choice([-1, 1]), random.choice([-1, 1])]
        self.timer = timer

    def update(self):
        """Update the position of the circle"""
        self.pos[0] += self.speed * self.direction[0]
        self.pos[1] += self.speed * self.direction[1]

        # If the circle reaches the window boundaries, change direction
        if self.pos[0] <= self.radius or self.pos[0] >= WIDTH - self.radius:
            self.direction[0] *= -1
        if self.pos[1] <= self.radius or self.pos[1] >= HEIGHT - self.radius:
            self.direction[1] *= -1

    def draw(self, screen):
        """Draw the circle on the screen"""
        #if this
        if(self.timer.is_running):
            pg.draw.circle(screen, GREEN, (int(self.pos[0]), int(self.pos[1])), self.radius)

    def is_clicked(self, click_pos):
        """Check if the circle is clicked"""
        distance = ((self.pos[0] - click_pos[0]) ** 2 + (self.pos[1] - click_pos[1]) ** 2) ** 0.5
        return distance <= self.radius
