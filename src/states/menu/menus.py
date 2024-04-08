import pygame as pg
import pygame_menu

from src.states.state import State
from src.constants import *
from ..levels.level1_1 import Level1_1

from leaderboard import LeaderboardManager

# Not using relative import to handle circular import issue when importing TitleScreen
# TODO Fix this later
import src.states.menu.title_screen as ts

class StartMenu(State):
    def __init__(self):
        super().__init__("background.png") # Change to start menu background

        self.leaderboard = LeaderboardManager(self.game)
        
        self.main_menu()
        
    def handle_events(self, events):
        if self.menu.is_enabled():
            self.menu.update(events)
        
        for event in events:
            if event.type != pg.KEYDOWN:
                return
            if event.key == pg.K_ESCAPE:
                self.manager.set_state(ts.TitleScreen)
                
    def draw(self):
        self.menu.draw(self.screen)
    
    def main_menu(self):
        # Create menu
        self.menu = pygame_menu.Menu('Second Chance', SCREEN_WIDTH, SCREEN_HEIGHT, 
                                theme=pygame_menu.themes.THEME_BLUE)

        # Add buttons to the menu
        self.menu.add.button('Start Game', self.manager.set_state, Level1_1)
        self.menu.add.button("Instructions", self.instructions_menu)
        self.menu.add.button("Leaderboard", self.leaderboard_menu)
        self.menu.add.button("Options", self.options_menu)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)

    def instructions_menu(self):
        self.menu = pygame_menu.Menu('Instructions', SCREEN_WIDTH, SCREEN_HEIGHT, 
                                             theme=pygame_menu.themes.THEME_BLUE)

        # Add game instructions
        instructions_text = "To move, use left and right arrow keys, or a and d\nTo jump, use up arrow key, w, or spacebar\nTo attack, use left click or q"
        self.menu.add.label(instructions_text, max_char=-1, font_size=20)

        # Add back button
        self.menu.add.button('Back', self.main_menu)

    def leaderboard_menu(self):
        # Fetch and display the leaderboard
        leaderboard_data = self.leaderboard.fetch_leaderboard()
        self.menu = pygame_menu.Menu('Leaderboard', SCREEN_WIDTH, SCREEN_HEIGHT,
                                      theme=pygame_menu.themes.THEME_BLUE)

        # Add leaderboard entries to the menu
        if leaderboard_data:
            for i, (name, score) in enumerate(leaderboard_data.items(), start=1):
                entry_text = f"{i}. {name}: {score}"
                self.menu.add.label(entry_text, max_char=-1, font_size=20)
        else:
            self.menu.add.label("Leaderboard is empty", max_char=-1, font_size=20)

        # Add back button
        self.menu.add.button('Back', self.main_menu)


    def options_menu(self):
        # Create options menu
        self.menu = pygame_menu.Menu('Options', SCREEN_WIDTH, SCREEN_HEIGHT, theme=pygame_menu.themes.THEME_BLUE)

        # Add volume control buttons
        volume_label = self.menu.add.label('Volume: {}'.format(int(self.game.volume * 100)))
        volume_label.update_font({'size': 30})  # Set font size for the label

        self.menu.add.button('Increase Volume', self.game.increase_volume)
        self.menu.add.button('Decrease Volume', self.game.decrease_volume)

        # Add back button
        self.menu.add.button('Back', self.main_menu)
        
        
class PauseMenu(State):
    def __init__(self):
        super().__init__()
        self.menu = pygame_menu.Menu('Paused', 400, 300,
                                     theme=pygame_menu.themes.THEME_BLUE)
        self.menu.add.button('Return to game', self.manager.pop_state)
        self.menu.add.button('Options', self.hi, "Not implemented yet")
        self.menu.add.button("Quit game", self.manager.set_state, ts.TitleScreen, clear=True, accept_kwargs=True)

    def handle_events(self, events):
        self.menu.update(events)

    def draw(self):
        self.menu.draw(self.screen)

    # TODO remove, just displaying what's not implemented yet
    def hi(self, s):
        print(s)