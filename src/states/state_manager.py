from .title_screen import TitleScreen
from .state import State

class StateManager:
    """Responsible for updating the state of the game."""
    
    def __init__(self):
        """Initialize game state to the title screen."""
        self.set_state(TitleScreen)

    def set_state(self, state: State):
        """Sets the current game state to another state.

        :param state: The class name for the state to switch to.
        """
        self.state = state()
