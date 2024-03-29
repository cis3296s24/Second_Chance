from .title_screen import TitleScreen
from .state import State

class StateManager:
    """Responsible for updating the state of the game."""
    
    def __init__(self):
        self.set_state(TitleScreen())

    def set_state(self, state: State):
        self.state = state
        self.state.manager = self
