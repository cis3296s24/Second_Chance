import pygame as pg

from src.constants import *
from src.utils.timer import Timer

class State:
    """
    The State class represents all of the different states that the game
    can be in.
    
    :param img: An optional image to be displayed on the screen.
    """
    
    game = None
    manager = None
    
    def __init__(self, img=None):
        self.screen = pg.display.get_surface()
        if img is not None:
            self.surface = pg.image.load(os.path.join(self.game.background_dir, img))
            self.surface = pg.transform.scale(self.surface, ((SCREEN_WIDTH, SCREEN_HEIGHT)))
        else:
            self.surface = pg.Surface((0, 0)) 
        
    def handle_events(self, events):
        for event in events:
            pass # Handle events here

    def update(self, events):
        pass

    def draw(self):
        self.screen.blit(self.surface, (0, 0))
        
    def get_text_surface(self, text: str, color: str, font_size: int, antialias=True):
        """Helper function to return a pygame.font.Font object."""
        return pg.font.Font(None, font_size).render(text, antialias, color)


class TimedState(State):
    """A TimedState is a state that automatically ends after a certain amount 
    of time."""
    
    def __init__(self, time: int, next_state: State, clear=False, timer=None, img=None):
        """
        :param time: Amount of time in seconds before this state ends.
        :param next_state: The next state to switch to after this state ends.
        :param clear: Parameter passed to StateManager
        :param timer: Timer from another state so that this state can resume
            it. This leads to coupling, but oh well for now.
        """
        super().__init__(img)
        self._time = time
        self._timer = Timer(start=True)
        self.next_state = next_state
        self.clear = clear
        self.passed_timer = timer
        
    def update(self, events):
        if self._timer.get_time(ms=True) >= self._time:
            if self.passed_timer is not None:
                self.passed_timer.resume()
            self.manager.set_state(self.next_state, clear=self.clear)