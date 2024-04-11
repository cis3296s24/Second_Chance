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

        self.volume = 0.5 # Initial volume level (between 0 and 1)
        
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
        volume_label = self.menu.add.label('Volume: {}'.format(int(self.volume * 100)))
        volume_label.update_font({'size': 30})  # Set font size for the label

        self.menu.add.button('Increase Volume', self.increase_volume)
        self.menu.add.button('Decrease Volume', self.decrease_volume)

        # Add back button
        self.menu.add.button('Back', self.main_menu)

    def increase_volume(self):
        self.volume = min(self.volume + 0.1, 1.0)  # Increase self.volume by 0.1, but ensure it doesn't exceed 1.0
        pg.mixer.music.set_volume(self.volume)

    def decrease_volume(self):
        self.volume = max(self.volume - 0.1, 0.0)  # Decrease self.volume by 0.1, but ensure it doesn't go below 0.0
        pg.mixer.music.set_volume(self.volume)
        
        
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
        

class UsernamePrompt(State):
    def __init__(self):
        super().__init__()
        self.input_rect = pg.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 12, 200, 24)
        self.font = pg.font.Font(None, 24)
        self.active = False
        self.text_prompt = self.font.render("Enter your username: ", True, (255, 255, 255))
        self.text_prompt_rect = self.text_prompt.get_rect(midbottom=self.input_rect.topleft)
        self.username = self.game.username
    
    def handle_events(self, events):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.input_rect.collidepoint(event.pos):
                    self.active = not self.active
                else:
                    self.active = False
            if event.type == pg.KEYDOWN:
                if self.active:
                    if event.key == pg.K_RETURN:
                        self.game.username = self.username # Set username in Game object
                        self.manager.set_state(StartMenu)
                        return
                    elif event.key == pg.K_BACKSPACE:
                        self.username = self.username[:-1]
                    else:
                        self.username += event.unicode
    
    def update(self, events):
        # Render the username directly inside the input rectangle
        self.text_surface = self.font.render(self.username, True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=self.input_rect.center)
    
    def draw(self):
        self.screen.fill((30, 30, 30))
        pg.draw.rect(self.screen, (255, 255, 255), self.input_rect, 2)
        self.screen.blit(self.text_prompt, self.text_prompt_rect)
        self.screen.blit(self.text_surface, self.text_rect)