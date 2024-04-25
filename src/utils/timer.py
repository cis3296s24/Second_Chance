import pygame as pg


class Timer:
    """A helpful class to represent an in-game timer that counts up.
    This timer can be paused, resumed, and reset."""

    def __init__(self, start_time=0, start=False):
        """_summary_

        :param start_time: The starting time of the timer in seconds, defaults
            to 0
        :param start: Whether or not the timer should start on instantiation, 
            defaults to False
        """
        self.start_time = start_time
        self.paused_time = self.start_time
        self.is_running = False
        self.color = "white"
        self.screen = pg.display.get_surface()
        if start:
            self.start()

    def handle_events(self, events):
        """This method is called if you want to control the timer in-game 
        through key presses."""
        for event in events:
            if event.type != pg.KEYDOWN:
                return

            if event.key == pg.K_SPACE:
                self.pause() if self.is_running else self.resume()
            elif event.key == pg.K_BACKSPACE:
                self.reset() if self.is_running else self.resume()
            elif event.key == pg.K_RETURN:
                self.start()

    def start(self):
        if not self.is_running:
            self.start_time = pg.time.get_ticks()
            self.is_running = True

    def pause(self):
        if self.is_running:
            self.paused_time += pg.time.get_ticks() - self.start_time
            self.is_running = False

    def resume(self):
        if not self.is_running:
            self.start_time = pg.time.get_ticks()
            self.is_running = True

    def reset(self):
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
        """Returns the elapsed time in seconds."""
        if ms:  # Seconds with 3 decimal precision
            return self.get_time_milliseconds() / 1000
        else:  # Seconds
            return self.get_time_milliseconds() // 1000

    def display_time(self, font, pos=(0, 0)):
        elapsed_time = self.get_time_milliseconds() // 1000
        text_surface = font.render("Elapsed time: " + elapsed_time, True, self.color)
        self.screen.blit(text_surface, pos)
