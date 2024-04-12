from .menu.title_screen import TitleScreen
from .state import State

class StateManager:
    """Responsible for updating the state of the game."""

    def __init__(self):
        """Create state stack and initialize game state to the title screen."""
        self.state_stack = []
        self.state = None
       
        self.set_state(TitleScreen)

    def set_state(self, state, save_prev=False, clear=False):
        """Sets the current game state to another state.

        :param state: The class name of the state to switch to.
        :param save_prev: Whether to save the previous state to the state stack.
        :param clear: Whether to clear the state stack after changing state.
        """
        if save_prev and self.state is not None:
            self.state_stack.append(self.state)

        # If an instance of State was passed, set current state to that instance. 
        # Otherwise, instantiate it here.
        self.state = state if isinstance(state, State) else state()

        if clear:
            self.state_stack.clear()

        # TODO remove these print statements
        print(f"\n{self.state.__class__.__name__}")  # Show current state
        print([state.__class__.__name__ for state in self.state_stack]) # Show state stack

    def pop_state(self):
        """If there is at least one state saved in the state stack, pop that
        state from the state stack and set it as the current state.
        """
        if len(self.state_stack) >= 1:
            prev_state = self.state_stack.pop()
            self.set_state(prev_state)

 
