import pygame as pg
import pygame_menu

import src.states.menu.menus as menu
from src.states.state import State
from src.utils.timer import Timer
import src.states.menu.title_screen as ts

class Minigame(State):
    """Base class for a minigame."""

    def __init__(self, instructions: str, img=None):
        super().__init__(img)
        
        self.instructions = instructions
        self.instructions_enabled = True
        self.won = None
        self.countdown_over = False

        self.level = self.manager.get_prev_state()
        self.minigame_state = self # The current minigame state
        self.timer = Timer()
        self.timer_text = self.get_text_surface(
            f"Time: {self.timer.get_time(ms=True)}", "white", 36)


    def handle_events(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:    
                if event.key == pg.K_ESCAPE:
                    self.manager.set_state(menu.PauseMenu(self.timer), save_prev=True)

    def update(self, events):
        self.timer_text = self.get_text_surface(
            f"Time: {self.timer.get_time(ms=True):.3f}",
            "white", 36)
        
        if self.instructions_enabled: # Only run the instructions once
            self.manager.set_state(MinigameInstructions(self.instructions), save_prev=True)
            self.instructions_enabled = False
            
        if self.won: 
            self.win()
        elif self.won == False:
            self.lose()
            
    def draw(self):
        super().draw()  # Draw default background passed in as img parameter
        self.screen.blit(self.timer_text, (self.screen.get_width() - 190, 20))
        
    def win(self):
        """
        Sets the minigame to the `WinScreen` state when the player wins, which
        then returns the player to the previous state before they entered the 
        minigame.
        """
        
        if self.level:
            self.level.player.health = self.level.player.max_health
            # Put player back on the last tile before they fell
            self.level.player.rect.midbottom = self.level.player.last_ground_pos.midtop
            # TODO Make player invincible upon re-entering level state
            # TODO Save minigame time somewhere
            
            # Get the current state, which should be the minigame
            self.manager.set_state(
                menu.WinScreen(self.level, self.minigame_state.win_text, self.level.timer), save_prev=True
            )
        else:
            self.manager.set_state(
            menu.MinigameMenu_WinScreen(menu.StartMenu, self.minigame_state), 
            save_prev=True, 
            clear=True
        )
        
    def lose(self):
        """
        Returns the player to the title screen or start menu, depending on
        the previous state before the minigame started.
        """
        
        if self.level:
            """Go back to title screen."""
            self.manager.set_state(
                menu.LoseScreen(ts.TitleScreen, self.minigame_state), 
                save_prev=True, 
                clear=True
            )
        else:
            self.manager.set_state(
            menu.LoseScreen(menu.StartMenu, self.minigame_state), 
            save_prev=True, 
            clear=True
        )

class MinigameInstructions(State):
    """
    State that holds and displays a pygame_menu.Menu object, to not interfere
    with base Minigame class.
    
    Args:
        instructions (str): Instructions to display on the menu.
    """

    def __init__(self, instructions: str):
        super().__init__()
        self.menu = self.create_menu(instructions)

    def handle_events(self, events):
        if self.menu.is_enabled:
            self.menu.update(events)

        for event in events:
            if event.type != pg.KEYDOWN:
                return
            if event.key == pg.K_ESCAPE:
                self.manager.set_state(menu.PauseMenu, save_prev=True)

    def draw(self):
        if self.menu.is_enabled():
            self.menu.draw(self.screen) # pygame_menu needs self.screen parameter for some reason

    def create_menu(self, instructions: str):
        """Creates a `pygame.menu.Menu` object to display the instructions.

        Args:
            instructions (str): Instructions to display on the menu.

        Returns:
            `pygame.menu.Menu`: The menu object.
        """
        
        menu = pygame_menu.Menu('Instructions', 600, 350,
                                theme=pygame_menu.themes.THEME_BLUE)

        menu.add.label(instructions, max_char=-1, font_size=25, wordwrap=True)
        menu.add.button('Okay', self.manager.set_state, Countdown)

        return menu


class Countdown(State):
    """State to display a countdown before the minigame starts.

    Args:
        img (str, optional): Name of image to pass to super() constructor. 
            Defaults to None.
            
    Attributes:
        prev_state (State): Previous state to draw to the screen.
        minigame_timer (Timer): Timer from the minigame to be resumed by this 
            state.
        timer (Timer): Timer used to update the text surface after every 
            second.
    """

    def __init__(self, img=None):
        super().__init__(img)
        self.prev_state = self.manager.get_prev_state()
        self.minigame_timer = self.prev_state.timer
        self.timer = Timer(start_time=1, start=True)
        self.text = self.get_text_surface(str(3), "white", font_size=72)
        self.pos = (self.screen.get_width() / 2, self.screen.get_height() / 2)

    def update(self, events):
        text = ""
        time = self.timer.get_time()

        if time > 3.5:
            self.manager.pop_state() # Go back to minigame
            self.minigame_timer.start()
            self.prev_state.countdown_over = True
        elif time > 2:
            text = "GO!"
            self.pos = ((self.screen.get_width() / 2)-40, self.pos[1]) # Readjust when it displays GO
        elif 2 >= time >= 0: 
            text = str(int(time+1)) # A bad way to make this display normally

        self.text = self.get_text_surface(text, "white", font_size=72)

    def draw(self):
        self.prev_state.draw()
        self.screen.blit(self.text, self.pos)
