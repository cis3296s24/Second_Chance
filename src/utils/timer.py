import pygame as pg


class Timer:
    """
    A helpful class to represent an in-game timer that counts up. This 
    timer can be paused, resumed, and reset.

    Args:
        start_time (int, optional): The starting time of the timer in seconds. 
            Defaults to 0.
        start (bool, optional):  Whether or not the timer should start on 
            instantiation. Defaults to False.
            
    Attributes:
        start_time (int): The starting time of the timer in seconds. 
        paused_time (float): The time when this timer was paused.
        is_running (bool): Whether the timer is currently running or not.
        color (str): The color of the timer's text to display
        screen (pygame.Surface): The screen to draw to.
    """
    
    def __init__(self, start_time=0, start=False):
        self.start_time = start_time
        self.paused_time = self.start_time
        self.is_running = False
        self.color = "white"
        self.screen = pg.display.get_surface()
        if start:
            self.start()

    def start(self):
        """Starts the timer."""
        if not self.is_running:
            self.start_time = pg.time.get_ticks()
            self.is_running = True

    def pause(self):
        """Pauses the timer."""
        if self.is_running:
            self.paused_time += pg.time.get_ticks() - self.start_time
            self.is_running = False

    def resume(self):
        """Resumes the timer."""
        if not self.is_running:
            self.start_time = pg.time.get_ticks()
            self.is_running = True

    def reset(self):
        """Resets the timer."""
        self.start_time = 0
        self.paused_time = 0
        self.is_running = False

    def get_time_milliseconds(self):
        """Returns the elapsed time in milliseconds."""
        if self.is_running:
            time = self.paused_time + pg.time.get_ticks() - self.start_time
        else:
            time = self.paused_time

        return time
            
    def get_time(self, ms=False):
        """Returns the elapsed time in seconds (by default).

        Args:
            ms (bool, optional): Whether or not to also include 3 decimal 
                precision. Defaults to False.

        Returns:
            int | float: The time in seconds or seconds with 3 decimal 
                precision.
        """
        if ms: # Seconds with 3 decimal precision
            return self.get_time_milliseconds() / 1000
        else: # Seconds
            return self.get_time_milliseconds() // 1000
    
    def display_time(self, font, pos=(0, 0)):
        """Draws the elapsed time onto the screen.

        Args:
            font (pg.font.Font): Font object to render.
            pos (tuple, optional): (x, y) position to display surface. Defaults
                to (0, 0).
        """
        elapsed_time = self.get_time_milliseconds() // 1000
        text_surface = font.render("Elapsed time: " + elapsed_time, True, self.color)
        self.screen.blit(text_surface, pos)
