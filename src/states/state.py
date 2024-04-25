import pygame as pg

from src.constants import *
from src.utils.timer import Timer


class State:
    """
    The State class represents all of the different states that the game
    can be in.
    
    Note: 
        If you want to create another state, that state should inherit from 
            this class. You should not manually instantiate a state.

    Args:
        img (str, optional): Name of the image to load from the game's 
            background images directory. Defaults to None.
        
    Attributes:
        game (Game): The main `Game` object.
        manager (StateManager): The `Game` object's state manager.
        screen (pygame.Surface): The screen to draw to.
        surface (pygame.Surface): The surface to display a background image.
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
        """All input events from are handled here.
        
        Note:
            Every state that inherits from this class needs to implement the
                loop to process input events. `pygame.menu.Menu` objects 
                require the entire list of events to update, so this is a 
                workaround for that for now.

        Args:
            events (list[pygame.event.Event]): List of events.
        """
        for event in events:
            pass  # Handle events here

    def update(self, events):
        """_summary_
        
        Note:
            Some other states needed to use the `events` list, so that's the
                only reason why they are passed in here.

        Args:
            events (list[pygame.event.Event]): List of events.
        """
        pass

    def draw(self):
        """Draws the `surface` image onto the screen."""
        self.screen.blit(self.surface, (0, 0))

    def get_text_surface(self, text: str, color: str, font_size: int, antialias=True):
        """Helper method to return a pygame.Surface object for displaying text."""
        return pg.font.Font(None, font_size).render(text, antialias, color)


class TimedState(State):
    """A TimedState is a state that automatically ends after a certain amount of time.

    Args:
        time (int): Amount of time in seconds before this state ends.
        next_state (State): The next state to switch to after this state 
            ends.
        clear (bool, optional): Parameter passed to StateManager. 
            Defaults to False.
        timer (Timer, optional): Timer from another state so that this
            state can resume it. Defaults to None.
        img (str, optional): Background image to pass to the `State` 
            superclass. Defaults to None.
    
    Attributes:
        _timer (Timer): Used by the update method to end the state when it's 
            time.
    """

    def __init__(self, time: int, next_state: State, clear=False, timer=None, img=None):
        super().__init__(img)
        self._time = time
        self._timer = Timer(start=True)
        self.next_state = next_state
        self.clear = clear
        self.passed_timer = timer

    def update(self, events):
        """
        Switches to the next state if enough time has passed. Also resumes the
        timer that was passed into the constructor (usually for the minigame 
        timer).
        """
        if self._timer.get_time(ms=True) >= self._time:
            if self.passed_timer is not None:
                self.passed_timer.resume()
            self.manager.set_state(self.next_state, clear=self.clear)
